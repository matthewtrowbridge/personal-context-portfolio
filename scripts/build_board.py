#!/usr/bin/env python3
"""Build the deliverables board: generated/index.json -> generated/board.html.

Python 3 standard library only. Emits ONE self-contained file -- no CDN, no
external fonts, no network at runtime -- so it works from Cloudflare Pages, from
the iCloud mirror, and on a plane with the phone in airplane mode.

Only T1/T2 entities are rendered, ever. The validator already guarantees the
spine holds nothing above T2; this is the second lock.

    python3 scripts/build_board.py [--out PATH]
"""

import argparse
import datetime as dt
import html
import json
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
INDEX_JSON = os.path.join(ROOT, "generated", "index.json")
DEFAULT_OUT = os.path.join(ROOT, "generated", "board.html")

RENDERABLE_SENSITIVITY = ("T1", "T2")
DOMAIN_LABELS = {
    "hip": "HIP",
    "uva-em": "UVA Emergency Medicine",
    "mdp-hds": "MDP / Health Design Sprint",
    "red-cell": "Red Cell",
    "personal": "Personal",
}
PAPER_STAGES = [
    "idea", "scoped", "lit-complete", "irb", "data", "analysis", "drafting",
    "internal-review", "external-review", "submitted", "revision", "accepted",
]

CSS = """
*{box-sizing:border-box}
:root{
  --bg:#fbfbfa; --fg:#1a1a18; --muted:#6b6b66; --line:#e2e2dd;
  --card:#fff; --accent:#8a4b2a; --warn:#a33; --ok:#2f6b3f;
}
@media (prefers-color-scheme:dark){
  :root{--bg:#16161a;--fg:#e8e8e4;--muted:#9a9a94;--line:#2c2c33;
        --card:#1e1e24;--accent:#d08a5e;--warn:#e08585;--ok:#7fbf8f}
}
:root[data-theme=dark]{--bg:#16161a;--fg:#e8e8e4;--muted:#9a9a94;--line:#2c2c33;
  --card:#1e1e24;--accent:#d08a5e;--warn:#e08585;--ok:#7fbf8f}
:root[data-theme=light]{--bg:#fbfbfa;--fg:#1a1a18;--muted:#6b6b66;--line:#e2e2dd;
  --card:#fff;--accent:#8a4b2a;--warn:#a33;--ok:#2f6b3f}
body{margin:0;background:var(--bg);color:var(--fg);
  font:16px/1.55 -apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,sans-serif;
  padding:1rem;max-width:52rem;margin:0 auto;-webkit-text-size-adjust:100%}
header{padding:.5rem 0 1rem}
h1{font-size:1.35rem;margin:0 0 .15rem}
.sub{color:var(--muted);font-size:.85rem}
#q{width:100%;padding:.7rem .85rem;font-size:1rem;border:1px solid var(--line);
  border-radius:.6rem;background:var(--card);color:var(--fg);margin:.75rem 0 1rem}
h2{font-size:.78rem;text-transform:uppercase;letter-spacing:.09em;
  color:var(--muted);margin:1.75rem 0 .6rem;font-weight:600}
.card{background:var(--card);border:1px solid var(--line);border-radius:.7rem;
  padding:.85rem .95rem;margin-bottom:.7rem}
.card h3{margin:0;font-size:1rem;font-weight:600}
.meta{color:var(--muted);font-size:.8rem;margin-top:.2rem}
.na{margin-top:.5rem;font-size:.88rem;padding-left:.7rem;
  border-left:2px solid var(--accent)}
ul.d{list-style:none;padding:0;margin:.7rem 0 0}
ul.d li{padding:.45rem 0;border-top:1px solid var(--line)}
a{color:var(--accent)}
a.file{display:block;text-decoration:none;font-weight:500}
a.file:hover{text-decoration:underline}
.tag{display:inline-block;font-size:.68rem;text-transform:uppercase;
  letter-spacing:.05em;padding:.1rem .4rem;border:1px solid var(--line);
  border-radius:.3rem;color:var(--muted);margin-right:.3rem}
.overdue{color:var(--warn);font-weight:600}
.pipe{display:flex;gap:2px;margin:.5rem 0 .2rem;flex-wrap:wrap}
.pipe span{flex:1;min-width:9px;height:5px;background:var(--line);border-radius:2px}
.pipe span.on{background:var(--accent)}
details summary{cursor:pointer;color:var(--muted);font-size:.82rem;padding:.3rem 0}
.empty{color:var(--muted);font-style:italic;font-size:.88rem}
footer{color:var(--muted);font-size:.75rem;margin:2.5rem 0 1rem;
  border-top:1px solid var(--line);padding-top:.8rem}
"""

JS = """
var q=document.getElementById('q');
function norm(s){return (s||'').toLowerCase()}
q.addEventListener('input',function(){
  var t=norm(q.value).trim();
  var cards=document.querySelectorAll('.card');
  for(var i=0;i<cards.length;i++){
    var c=cards[i];
    c.style.display = (!t || norm(c.dataset.s).indexOf(t)>-1) ? '' : 'none';
  }
  var secs=document.querySelectorAll('section');
  for(var j=0;j<secs.length;j++){
    var s=secs[j], vis=s.querySelectorAll('.card:not([style*="none"])').length;
    s.style.display = vis ? '' : 'none';
  }
});
"""


def esc(value):
    return html.escape(str(value if value is not None else ""))


def renderable(record):
    return record.get("sensitivity") in RENDERABLE_SENSITIVITY


def deliverable_sort_key(item):
    return (str(item.get("date") or ""), str(item.get("title") or ""))


def render_deliverables(items):
    """Newest first; anything superseded folded into an expander."""
    if not items:
        return '<p class="empty">No deliverables recorded yet.</p>'
    ordered = sorted(items, key=deliverable_sort_key, reverse=True)
    current = [d for d in ordered if d.get("status") != "superseded"]
    older = [d for d in ordered if d.get("status") == "superseded"]

    def row(item):
        title = esc(item.get("title"))
        url = item.get("url")
        link = ('<a class="file" href="%s">%s</a>' % (esc(url), title)) if url \
            else '<span class="file">%s</span>' % title
        tags = "".join(
            '<span class="tag">%s</span>' % esc(item[f])
            for f in ("type", "status", "version") if item.get(f))
        sent = ""
        if item.get("sent_on"):
            who = item.get("sent_to") or []
            if isinstance(who, str):
                who = [who]
            names = ", ".join(w.split(":")[-1].replace("-", " ") for w in who)
            sent = " &middot; sent %s%s" % (esc(item["sent_on"]),
                                            " to %s" % esc(names) if names else "")
        return '<li>%s<div class="meta">%s%s%s</div></li>' % (
            link, tags, esc(item.get("date") or ""), sent)

    out = '<ul class="d">%s</ul>' % "".join(row(d) for d in current)
    if older:
        out += '<details><summary>%d older version%s</summary><ul class="d">%s</ul></details>' % (
            len(older), "" if len(older) == 1 else "s", "".join(row(d) for d in older))
    return out


def search_blob(record):
    parts = [record.get("id"), record.get("title"), record.get("status"),
             record.get("domain"), record.get("next_action"), record.get("summary")]
    for key in ("keywords",):
        value = record.get(key) or []
        if isinstance(value, str):
            value = [value]
        parts.extend(value)
    for item in record.get("deliverables") or []:
        if isinstance(item, dict):
            parts.append(item.get("title"))
            kws = item.get("keywords") or []
            if isinstance(kws, str):
                kws = [kws]
            parts.extend(kws)
    return " ".join(str(p) for p in parts if p)


def due_html(record, today):
    date = record.get("review_by") or record.get("target_date") or record.get("key_deadline")
    if not date:
        return ""
    try:
        parsed = dt.date.fromisoformat(str(date))
    except ValueError:
        return ""
    if parsed < today:
        return ' &middot; <span class="overdue">%s &mdash; %d days overdue</span>' % (
            esc(date), (today - parsed).days)
    return " &middot; due %s" % esc(date)


def render_project(record, today):
    body = ['<article class="card" data-s="%s">' % esc(search_blob(record))]
    body.append("<h3>%s</h3>" % esc(record.get("title")))
    body.append('<div class="meta">%s%s</div>' % (
        esc(record.get("status")), due_html(record, today)))
    if record.get("next_action"):
        body.append('<div class="na">%s</div>' % esc(record["next_action"]))
    if record.get("workspace_url"):
        body.append('<div class="meta"><a href="%s">Open project folder</a></div>'
                    % esc(record["workspace_url"]))
    body.append(render_deliverables(record.get("deliverables")))
    body.append("</article>")
    return "".join(body)


def render_paper(record, today):
    status = record.get("status")
    idx = PAPER_STAGES.index(status) if status in PAPER_STAGES else -1
    pipe = "".join('<span class="%s"></span>' % ("on" if i <= idx else "")
                   for i in range(len(PAPER_STAGES)))
    body = ['<article class="card" data-s="%s">' % esc(search_blob(record))]
    body.append("<h3>%s</h3>" % esc(record.get("title")))
    body.append('<div class="pipe">%s</div>' % pipe)
    meta = [esc(status)]
    if record.get("days_in_stage") is not None:
        meta.append("%d days in stage" % record["days_in_stage"])
    body.append('<div class="meta">%s%s</div>' % (" &middot; ".join(meta),
                                                  due_html(record, today)))
    if record.get("next_action"):
        body.append('<div class="na">%s</div>' % esc(record["next_action"]))
    body.append(render_deliverables(record.get("deliverables")))
    body.append("</article>")
    return "".join(body)


def build(payload, today):
    records = [r for r in payload["entities"] if renderable(r)]
    papers = sorted((r for r in records if r.get("type") == "paper"),
                    key=lambda r: (PAPER_STAGES.index(r["status"])
                                   if r.get("status") in PAPER_STAGES else 99, r["id"]),
                    reverse=True)
    projects = [r for r in records if r.get("type") in ("project", "engagement")]

    by_domain = {}
    for record in projects:
        by_domain.setdefault(record.get("domain") or "personal", []).append(record)

    parts = [
        "<title>Deliverables</title>",
        '<meta name="viewport" content="width=device-width,initial-scale=1">',
        "<style>%s</style>" % CSS,
        "<header><h1>Deliverables</h1>",
        '<div class="sub">%d projects &middot; %d manuscripts &middot; updated %s</div></header>'
        % (len(projects), len(papers), esc(payload.get("generated_on"))),
        '<input id="q" type="search" placeholder="Search titles, keywords, next actions…" '
        'autocomplete="off" autocapitalize="off">',
    ]

    if papers:
        parts.append("<section><h2>Manuscripts</h2>")
        parts.extend(render_paper(r, today) for r in papers)
        parts.append("</section>")

    for domain in sorted(by_domain, key=lambda d: DOMAIN_LABELS.get(d, d)):
        parts.append("<section><h2>%s</h2>" % esc(DOMAIN_LABELS.get(domain, domain)))
        parts.extend(render_project(r, today) for r in sorted(by_domain[domain],
                                                             key=lambda r: r["id"]))
        parts.append("</section>")

    parts.append(
        "<footer>Generated from the context graph. Do not edit &mdash; edit the entity "
        "and re-run <code>build_board.py</code>.<br>"
        "Searches titles, keywords and next actions. For text <em>inside</em> a document, "
        "use Drive or SharePoint search.<br>"
        "Only T1/T2 entities appear here.</footer>")
    parts.append("<script>%s</script>" % JS)
    return "\n".join(parts) + "\n"


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    parser.add_argument("--out", default=DEFAULT_OUT)
    parser.add_argument("--today", help="override today's date (YYYY-MM-DD), for testing")
    args = parser.parse_args(argv)

    if not os.path.exists(INDEX_JSON):
        print("ERROR %s missing -- run: python3 scripts/graph.py index" % INDEX_JSON)
        return 1
    with open(INDEX_JSON, encoding="utf-8") as fh:
        payload = json.load(fh)

    today = dt.date.fromisoformat(args.today) if args.today \
        else dt.date.fromisoformat(payload.get("generated_on"))

    os.makedirs(os.path.dirname(args.out), exist_ok=True)
    with open(args.out, "w", encoding="utf-8") as fh:
        fh.write(build(payload, today))
    print("Board written to %s" % os.path.relpath(args.out, ROOT))
    return 0


if __name__ == "__main__":
    sys.exit(main())
