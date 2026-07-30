#!/usr/bin/env python3
"""Context graph tooling: validate, index, audit.

Python 3 standard library only. No pip install, no network, no model calls.
Graph maintenance must never cost tokens -- that is what makes it affordable
to actually maintain.

All rules come from ontology/schema.json. Nothing is hardcoded here, so
extending the ontology is a JSON edit rather than a code change.

    python3 scripts/graph.py validate [path ...]
    python3 scripts/graph.py index
    python3 scripts/graph.py audit
"""

import argparse
import datetime as dt
import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SCHEMA_PATH = os.path.join(ROOT, "ontology", "schema.json")
GRAPH_DIR = os.path.join(ROOT, "graph")
GENERATED_DIR = os.path.join(ROOT, "generated")

# Content-leakage patterns are checked here. Secret patterns are checked
# everywhere (see SECRET_SCAN_SKIP).
SUBSTRATE_DIRS = ("graph", "context", "papers", "voice", "outputs")
SECRET_SCAN_SKIP = (".git", "stock", "generated", "node_modules")

ID_RE = re.compile(r"^[a-z][a-z0-9]*:[a-z][a-z0-9-]*$")
SLUG_RE = re.compile(r"^[a-z][a-z0-9-]*$")


# --------------------------------------------------------------------------
# Minimal YAML subset parser
#
# Supports exactly what the ontology uses: scalars, inline lists, block lists,
# nested maps, and lists of maps. Deliberately not a general YAML parser --
# a constrained grammar we fully control beats a dependency.
# --------------------------------------------------------------------------

class ParseError(Exception):
    pass


def _scalar(raw):
    raw = raw.strip()
    if not raw:
        return None
    # Strip trailing comments only on unquoted values (URLs contain '#').
    if raw[0] not in "\"'[":
        hash_pos = raw.find(" #")
        if hash_pos != -1:
            raw = raw[:hash_pos].strip()
    if len(raw) >= 2 and raw[0] == raw[-1] and raw[0] in "\"'":
        return raw[1:-1]
    if raw.startswith("[") and raw.endswith("]"):
        inner = raw[1:-1].strip()
        if not inner:
            return []
        return [_scalar(p) for p in _split_inline(inner)]
    low = raw.lower()
    if low in ("true", "false"):
        return low == "true"
    if low in ("null", "~"):
        return None
    if re.fullmatch(r"-?\d+", raw):
        return int(raw)
    return raw


def _split_inline(inner):
    """Split an inline list on commas that are not inside quotes."""
    parts, buf, quote = [], "", None
    for ch in inner:
        if quote:
            if ch == quote:
                quote = None
            buf += ch
        elif ch in "\"'":
            quote = ch
            buf += ch
        elif ch == ",":
            parts.append(buf)
            buf = ""
        else:
            buf += ch
    if buf.strip():
        parts.append(buf)
    return parts


def _indent(line):
    return len(line) - len(line.lstrip(" "))


def _parse_block(lines, i, indent):
    """Parse a mapping or sequence at the given indent. Returns (value, i)."""
    if i >= len(lines):
        return None, i
    if lines[i].lstrip().startswith("- "):
        return _parse_seq(lines, i, indent)
    return _parse_map(lines, i, indent)


def _parse_seq(lines, i, indent):
    items = []
    while i < len(lines):
        line = lines[i]
        if not line.strip() or line.lstrip().startswith("#"):
            i += 1
            continue
        if _indent(line) < indent or not line.lstrip().startswith("- "):
            break
        content = line.lstrip()[2:]
        # A list item that is itself a mapping: "- title: x" with more keys
        # on following lines at deeper indent.
        if ":" in content and not content.strip().startswith("http"):
            key, _, rest = content.partition(":")
            if SLUG_RE.match(key.strip().replace("_", "-")):
                item_indent = _indent(line) + 2
                sub = {key.strip(): _scalar(rest)}
                i += 1
                while i < len(lines):
                    nxt = lines[i]
                    if not nxt.strip():
                        i += 1
                        continue
                    if _indent(nxt) < item_indent or nxt.lstrip().startswith("- "):
                        break
                    k2, _, v2 = nxt.strip().partition(":")
                    sub[k2.strip()] = _scalar(v2)
                    i += 1
                items.append(sub)
                continue
        items.append(_scalar(content))
        i += 1
    return items, i


def _parse_map(lines, i, indent):
    out = {}
    while i < len(lines):
        line = lines[i]
        if not line.strip() or line.lstrip().startswith("#"):
            i += 1
            continue
        cur = _indent(line)
        if cur < indent:
            break
        if line.lstrip().startswith("- "):
            break
        if ":" not in line:
            raise ParseError("expected 'key: value', got: %s" % line.strip())
        key, _, rest = line.strip().partition(":")
        key = key.strip()
        rest = rest.strip()
        if rest:
            out[key] = _scalar(rest)
            i += 1
        else:
            # Nested block on following lines at deeper indent.
            j = i + 1
            while j < len(lines) and not lines[j].strip():
                j += 1
            if j < len(lines) and _indent(lines[j]) > cur:
                value, j = _parse_block(lines, j, _indent(lines[j]))
                out[key] = value
                i = j
            else:
                out[key] = None
                i += 1
    return out, i


def parse_frontmatter(text):
    """Return (data, body). Raises ParseError if frontmatter is absent/bad."""
    if not text.startswith("---"):
        raise ParseError("no YAML frontmatter (file must start with '---')")
    lines = text.split("\n")
    end = None
    for idx in range(1, len(lines)):
        if lines[idx].strip() == "---":
            end = idx
            break
    if end is None:
        raise ParseError("frontmatter is not closed with '---'")
    data, _ = _parse_map(lines[1:end], 0, 0)
    return data, "\n".join(lines[end + 1:])


# --------------------------------------------------------------------------
# Loading
# --------------------------------------------------------------------------

def load_schema():
    with open(SCHEMA_PATH, encoding="utf-8") as fh:
        return json.load(fh)


def entity_files():
    found = []
    for dirpath, dirnames, filenames in os.walk(GRAPH_DIR):
        dirnames[:] = sorted(d for d in dirnames if not d.startswith("."))
        for name in sorted(filenames):
            if name.endswith(".md") and not name.startswith("_"):
                found.append(os.path.join(dirpath, name))
    return sorted(found)


def rel_path(path):
    return os.path.relpath(path, ROOT).replace(os.sep, "/")


class Issue:
    def __init__(self, level, path, message):
        self.level = level
        self.path = path
        self.message = message

    def __str__(self):
        tag = "ERROR" if self.level == "error" else "warn "
        return "%s %s: %s" % (tag, self.path, self.message)


# --------------------------------------------------------------------------
# Validation
# --------------------------------------------------------------------------

def parse_date(value):
    if isinstance(value, dt.date):
        return value
    try:
        return dt.date.fromisoformat(str(value))
    except (ValueError, TypeError):
        return None


def load_entities(schema, issues):
    entities = {}
    by_path = {}
    for path in entity_files():
        rp = rel_path(path)
        with open(path, encoding="utf-8") as fh:
            text = fh.read()
        try:
            data, body = parse_frontmatter(text)
        except ParseError as exc:
            issues.append(Issue("error", rp, str(exc)))
            continue
        if not isinstance(data, dict):
            issues.append(Issue("error", rp, "frontmatter did not parse to a mapping"))
            continue
        data["_path"] = rp
        data["_body"] = body
        data["_text"] = text
        eid = data.get("id")
        if eid in entities:
            issues.append(Issue(
                "error", rp,
                "duplicate id '%s' (also in %s)" % (eid, entities[eid]["_path"])))
        elif eid:
            entities[eid] = data
        by_path[rp] = data
    return entities, by_path


def check_identity(data, schema, issues):
    rp = data["_path"]
    eid = data.get("id")
    etype = data.get("type")

    if not eid:
        issues.append(Issue("error", rp, "missing required field 'id'"))
        return
    if not ID_RE.match(str(eid)):
        issues.append(Issue("error", rp, "id '%s' must match type:slug (lowercase kebab)" % eid))
        return
    prefix, _, slug = str(eid).partition(":")
    if etype and prefix != etype:
        issues.append(Issue("error", rp, "id prefix '%s' does not match type '%s'" % (prefix, etype)))
    expected = os.path.basename(rp)[:-3]
    if slug != expected:
        issues.append(Issue(
            "error", rp,
            "id slug '%s' does not match filename '%s.md'" % (slug, expected)))
    if etype in schema["types"]:
        want_dir = schema["types"][etype]["dir"]
        if os.path.dirname(rp) != want_dir:
            issues.append(Issue(
                "error", rp, "type '%s' belongs in %s/" % (etype, want_dir)))


def check_fields(data, schema, issues):
    rp = data["_path"]
    etype = data.get("type")
    if etype not in schema["types"]:
        issues.append(Issue(
            "error", rp,
            "unknown type '%s' (known: %s)" % (etype, ", ".join(sorted(schema["types"])))))
        return
    spec = schema["types"][etype]

    for field in schema["common_required"]:
        if data.get(field) in (None, "", []):
            issues.append(Issue("error", rp, "missing required field '%s'" % field))

    status = data.get("status")
    if status is not None and status not in spec["status"]:
        issues.append(Issue(
            "error", rp,
            "status '%s' invalid for %s (allowed: %s)" % (status, etype, ", ".join(spec["status"]))))

    domain = data.get("domain")
    if domain is not None and domain not in schema["domains"]:
        issues.append(Issue("error", rp, "unknown domain '%s'" % domain))

    for field in ("priority", "contact_cadence"):
        allowed = spec.get(field)
        value = data.get(field)
        if allowed and value is not None and value not in allowed:
            issues.append(Issue(
                "error", rp,
                "%s '%s' invalid (allowed: %s)" % (field, value, ", ".join(allowed))))

    for field in ("updated", "review_by", "last_contact", "next_ping_due",
                  "key_deadline", "target_date", "stage_entered", "decided_on",
                  "revisit_by", "captured_on", "published"):
        if data.get(field) is not None and parse_date(data[field]) is None:
            issues.append(Issue(
                "error", rp, "%s '%s' is not an ISO date (YYYY-MM-DD)" % (field, data[field])))


def check_sensitivity(data, schema, issues):
    rp = data["_path"]
    rules = schema["spine_rules"]
    levels = schema["sensitivity_levels"]
    sens = data.get("sensitivity")

    if sens is not None:
        if sens not in levels:
            issues.append(Issue("error", rp, "unknown sensitivity '%s'" % sens))
        else:
            max_idx = levels.index(rules["max_sensitivity"])
            if levels.index(sens) > max_idx:
                if sens in rules.get("warn_sensitivity", []):
                    issues.append(Issue(
                        "warn", rp,
                        "sensitivity %s above the T1/T2 spine limit -- consider a pointer stub" % sens))
                else:
                    issues.append(Issue(
                        "error", rp,
                        "sensitivity %s must not live in this repo; keep it in its secure home "
                        "and reference it with raw_location/raw_sensitivity" % sens))

    classes = data.get("data_class") or []
    if isinstance(classes, str):
        classes = [classes]
    for cls in classes:
        if cls not in schema["data_classes"]:
            issues.append(Issue("error", rp, "unknown data_class '%s'" % cls))
        elif cls in rules["forbidden_data_classes"]:
            issues.append(Issue("error", rp, "data_class '%s' must never be in the spine" % cls))

    raw_loc = data.get("raw_location")
    if raw_loc and not str(raw_loc).startswith(("local:", "vault:", "tenant:")):
        issues.append(Issue(
            "warn", rp,
            "raw_location should be prefixed local:/vault:/tenant: so it cannot be mistaken "
            "for a path in this repo"))


def check_relations(data, entities, schema, issues):
    rp = data["_path"]
    rel = data.get("rel")
    if rel is None:
        return
    if not isinstance(rel, dict):
        issues.append(Issue("error", rp, "'rel' must be a mapping of edge -> [ids]"))
        return
    for edge, targets in sorted(rel.items()):
        if edge not in schema["edges"]:
            issues.append(Issue(
                "error", rp,
                "unknown edge '%s' (allowed: %s)" % (edge, ", ".join(schema["edges"]))))
        if targets is None:
            continue
        if isinstance(targets, str):
            targets = [targets]
        for target in targets:
            if target not in entities:
                issues.append(Issue(
                    "error", rp, "dangling edge %s -> '%s' (no such entity)" % (edge, target)))


def check_deliverables(data, schema, issues):
    rp = data["_path"]
    items = data.get("deliverables")
    if not items:
        return
    spec = schema["deliverable_fields"]
    if not isinstance(items, list):
        issues.append(Issue("error", rp, "'deliverables' must be a list"))
        return
    for idx, item in enumerate(items):
        where = "deliverables[%d]" % idx
        if not isinstance(item, dict):
            issues.append(Issue("error", rp, "%s must be a mapping" % where))
            continue
        for field in spec["required"]:
            if item.get(field) in (None, ""):
                issues.append(Issue("error", rp, "%s missing '%s'" % (where, field)))
        for field in ("type", "status", "share"):
            value = item.get(field)
            if value is not None and value not in spec[field]:
                issues.append(Issue(
                    "error", rp,
                    "%s %s '%s' invalid (allowed: %s)" % (where, field, value, ", ".join(spec[field]))))
        if item.get("date") is not None and parse_date(item["date"]) is None:
            issues.append(Issue("error", rp, "%s date is not an ISO date" % where))
        if item.get("sent_on") and not item.get("sent_to"):
            issues.append(Issue("warn", rp, "%s has sent_on but no sent_to" % where))


def check_freshness(data, schema, issues, today):
    rp = data["_path"]
    stale = schema["staleness"]
    status = data.get("status")

    # An overdue review is a work signal, not a structural defect. Making it an
    # error would leave CI permanently red on real data, and a permanently red
    # check gets ignored. validate() answers "is the graph well-formed"; audit()
    # and /weekly answer "is the work on track".
    for field in ("review_by", "target_date", "key_deadline"):
        date = parse_date(data.get(field)) if data.get(field) else None
        if date and date < today:
            issues.append(Issue(
                "warn", rp,
                "%s %s passed %d days ago -- move it or do it" % (
                    field, date.isoformat(), (today - date).days)))

    if status in stale.get("exempt_statuses", []):
        return
    if status in stale.get("active_statuses", []):
        updated = parse_date(data.get("updated")) if data.get("updated") else None
        if updated:
            age = (today - updated).days
            if age > stale["stale_after_days"]:
                issues.append(Issue(
                    "warn", rp,
                    "status '%s' but not updated in %d days" % (status, age)))


def check_orphans(entities, issues):
    inbound = set()
    for data in entities.values():
        rel = data.get("rel") or {}
        if isinstance(rel, dict):
            for targets in rel.values():
                if isinstance(targets, str):
                    targets = [targets]
                for target in targets or []:
                    inbound.add(target)
    for eid, data in sorted(entities.items()):
        rel = data.get("rel") or {}
        has_out = bool(rel) and any(rel.values())
        if not has_out and eid not in inbound:
            issues.append(Issue(
                "warn", data["_path"],
                "orphan -- no inbound or outbound edges; link it or remove it"))


def check_leakage(schema, issues):
    patterns = {k: re.compile(v) for k, v in schema["leakage_patterns"].items()
                if not k.startswith("_")}
    allow = {k: v for k, v in schema["leakage_allow_fields"].items()
             if not k.startswith("_")}
    secret_keys = [k for k in patterns if k.startswith("secret_")]

    for dirpath, dirnames, filenames in os.walk(ROOT):
        dirnames[:] = sorted(
            d for d in dirnames
            if d not in SECRET_SCAN_SKIP and not d.startswith("."))
        for name in sorted(filenames):
            if not name.endswith((".md", ".json", ".yaml", ".yml", ".txt", ".html")):
                continue
            path = os.path.join(dirpath, name)
            rp = rel_path(path)
            if rp.startswith("ontology/") or rp.startswith("scripts/"):
                continue  # these legitimately describe the patterns
            in_substrate = rp.split("/")[0] in SUBSTRATE_DIRS
            try:
                with open(path, encoding="utf-8") as fh:
                    lines = fh.read().split("\n")
            except (UnicodeDecodeError, OSError):
                continue
            for lineno, line in enumerate(lines, 1):
                for key, rx in patterns.items():
                    is_secret = key in secret_keys
                    if not is_secret and not in_substrate:
                        continue
                    if not rx.search(line):
                        continue
                    field = line.strip().partition(":")[0].strip().lstrip("- ")
                    if field in allow.get(key, []):
                        continue
                    issues.append(Issue(
                        "error", "%s:%d" % (rp, lineno),
                        "possible %s leak -- '%s' must not be in the spine" % (
                            key.replace("_", " "), key)))


def validate(schema, today, paths=None):
    issues = []
    entities, _ = load_entities(schema, issues)

    selected = None
    if paths:
        selected = {os.path.relpath(os.path.abspath(p), ROOT).replace(os.sep, "/")
                    for p in paths}

    for eid in sorted(entities):
        data = entities[eid]
        if selected is not None and data["_path"] not in selected:
            continue
        check_identity(data, schema, issues)
        check_fields(data, schema, issues)
        check_sensitivity(data, schema, issues)
        check_relations(data, entities, schema, issues)
        check_deliverables(data, schema, issues)
        check_freshness(data, schema, issues, today)

    if selected is None:
        check_orphans(entities, issues)
        check_leakage(schema, issues)

    return entities, issues


# --------------------------------------------------------------------------
# Index generation
# --------------------------------------------------------------------------

def one_line_summary(data):
    for para in data.get("_body", "").split("\n\n"):
        text = " ".join(para.split())
        if text and not text.startswith("#"):
            return text[:160]
    return ""


def build_index_payload(entities, today):
    records = []
    for eid in sorted(entities):
        data = entities[eid]
        stage_entered = parse_date(data.get("stage_entered")) if data.get("stage_entered") else None
        record = {
            "id": eid,
            "type": data.get("type"),
            "title": data.get("title"),
            "status": data.get("status"),
            "domain": data.get("domain"),
            "sensitivity": data.get("sensitivity"),
            "path": data["_path"],
            "summary": one_line_summary(data),
        }
        for field in ("owner", "priority", "next_action", "review_by", "updated",
                      "target_date", "key_deadline", "keywords", "workspace_url",
                      "notion_url", "raw_location"):
            if data.get(field) not in (None, "", []):
                record[field] = data[field]
        if stage_entered:
            record["days_in_stage"] = (today - stage_entered).days
        if data.get("deliverables"):
            record["deliverables"] = data["deliverables"]
        if data.get("rel"):
            record["rel"] = data["rel"]
        records.append(record)
    return {"generated_on": today.isoformat(), "count": len(records), "entities": records}


def write_index(payload, entities, today):
    os.makedirs(GENERATED_DIR, exist_ok=True)

    with open(os.path.join(GENERATED_DIR, "index.json"), "w", encoding="utf-8") as fh:
        json.dump(payload, fh, indent=2, sort_keys=True, ensure_ascii=False)
        fh.write("\n")

    lines = [
        "# Index",
        "",
        "Generated by `scripts/graph.py index` on %s. Do not hand-edit." % today.isoformat(),
        "",
        "Read this file to find entities, then read only the 3-6 you need.",
        "Never read `graph/` in bulk.",
        "",
    ]
    by_domain = {}
    for record in payload["entities"]:
        by_domain.setdefault(record.get("domain") or "unassigned", []).append(record)
    for domain in sorted(by_domain):
        lines.append("## %s" % domain)
        lines.append("")
        lines.append("| id | title | type | status | path |")
        lines.append("|---|---|---|---|---|")
        for record in sorted(by_domain[domain], key=lambda r: (r["type"] or "", r["id"])):
            lines.append("| `%s` | %s | %s | %s | `%s` |" % (
                record["id"], record.get("title") or "", record.get("type") or "",
                record.get("status") or "", record["path"]))
        lines.append("")
    with open(os.path.join(GENERATED_DIR, "INDEX.md"), "w", encoding="utf-8") as fh:
        fh.write("\n".join(lines))

    # Open loops: anything with a next action, soonest review first.
    loops = [r for r in payload["entities"] if r.get("next_action")]

    def loop_key(record):
        date = record.get("review_by") or record.get("target_date") or record.get("key_deadline")
        return (parse_date(date) or dt.date(2999, 1, 1), record["id"])

    out = [
        "# Open loops",
        "",
        "Generated %s. Everything with a next action, soonest date first." % today.isoformat(),
        "This is the chief-of-staff entry point -- start here, not in `graph/`.",
        "",
        "| due | id | next action | status | domain |",
        "|---|---|---|---|---|",
    ]
    for record in sorted(loops, key=loop_key):
        date = record.get("review_by") or record.get("target_date") or record.get("key_deadline") or ""
        parsed = parse_date(date) if date else None
        flag = " **OVERDUE**" if parsed and parsed < today else ""
        out.append("| %s%s | `%s` | %s | %s | %s |" % (
            date or "--", flag, record["id"], record.get("next_action") or "",
            record.get("status") or "", record.get("domain") or ""))
    out.append("")
    with open(os.path.join(GENERATED_DIR, "OPEN-LOOPS.md"), "w", encoding="utf-8") as fh:
        fh.write("\n".join(out))

    return len(payload["entities"]), len(loops)


# --------------------------------------------------------------------------
# Commands
# --------------------------------------------------------------------------

def report(issues):
    errors = [i for i in issues if i.level == "error"]
    warns = [i for i in issues if i.level == "warn"]
    for issue in sorted(warns, key=lambda i: (i.path, i.message)):
        print(issue)
    for issue in sorted(errors, key=lambda i: (i.path, i.message)):
        print(issue)
    return errors, warns


def cmd_validate(args, schema, today):
    entities, issues = validate(schema, today, args.paths)
    errors, warns = report(issues)
    print("\n%d entities | %d errors | %d warnings" % (len(entities), len(errors), len(warns)))
    return 1 if errors else 0


def cmd_index(args, schema, today):
    entities, issues = validate(schema, today)
    errors = [i for i in issues if i.level == "error"]
    if errors and not args.force:
        report(issues)
        print("\nRefusing to index with %d errors. Fix them, or pass --force." % len(errors))
        return 1
    payload = build_index_payload(entities, today)
    count, loops = write_index(payload, entities, today)
    print("Indexed %d entities, %d open loops -> generated/" % (count, loops))
    return 0


def cmd_audit(args, schema, today):
    entities, issues = validate(schema, today)
    errors, warns = report(issues)

    print("\n--- audit %s ---" % today.isoformat())
    by_type, by_domain, by_status = {}, {}, {}
    for data in entities.values():
        by_type[data.get("type")] = by_type.get(data.get("type"), 0) + 1
        by_domain[data.get("domain")] = by_domain.get(data.get("domain"), 0) + 1
        by_status[data.get("status")] = by_status.get(data.get("status"), 0) + 1
    print("entities: %d" % len(entities))
    print("by type:   " + ", ".join("%s=%d" % kv for kv in sorted(by_type.items(), key=lambda x: str(x[0]))))
    print("by domain: " + ", ".join("%s=%d" % kv for kv in sorted(by_domain.items(), key=lambda x: str(x[0]))))

    papers = [d for d in entities.values() if d.get("type") == "paper"]
    if papers:
        print("\npapers by stage:")
        for data in sorted(papers, key=lambda d: str(d.get("id"))):
            entered = parse_date(data.get("stage_entered")) if data.get("stage_entered") else None
            age = "%d days in stage" % (today - entered).days if entered else "stage age unknown"
            print("  %-40s %-16s %s" % (data.get("id"), data.get("status"), age))

    print("\n%d errors | %d warnings" % (len(errors), len(warns)))
    return 1 if errors else 0


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    parser.add_argument("--today", help="override today's date (YYYY-MM-DD), for testing")
    sub = parser.add_subparsers(dest="command", required=True)

    p_val = sub.add_parser("validate", help="check the graph")
    p_val.add_argument("paths", nargs="*", help="limit to these files (used by the edit hook)")
    p_val.set_defaults(func=cmd_validate)

    p_idx = sub.add_parser("index", help="regenerate generated/")
    p_idx.add_argument("--force", action="store_true", help="index even with errors")
    p_idx.set_defaults(func=cmd_index)

    p_aud = sub.add_parser("audit", help="human-readable health report")
    p_aud.set_defaults(func=cmd_audit)

    args = parser.parse_args(argv)
    today = parse_date(args.today) if args.today else dt.date.today()
    if today is None:
        print("ERROR --today must be YYYY-MM-DD")
        return 2
    return args.func(args, load_schema(), today)


if __name__ == "__main__":
    sys.exit(main())
