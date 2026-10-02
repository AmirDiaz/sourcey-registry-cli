#!/usr/bin/env python3
"""Sourcey Registry CLI — query Sourcey's open datasets from the terminal.

Data source: https://sourcey.com — the open registry of startup offers and
agent-readiness report cards (543 companies, published with evidence).

Usage:
    python sourcey_cli.py companies [--search QUERY] [--category CAT] [--limit N]
    python sourcey_cli.py credits --search QUERY [--limit N]
    python sourcey_cli.py readiness [--entity SLUG] [--grade A|B|C|D] [--limit N]
    python sourcey_cli.py stats
"""
import argparse
import json
import sys
import urllib.request

BASE = "https://sourcey.com"
DATASETS = {
    "companies": f"{BASE}/companies.json",
    "credits": f"{BASE}/startup-credits.json",
    "readiness": f"{BASE}/agent-readiness.json",
}


def fetch(name):
    with urllib.request.urlopen(DATASETS[name], timeout=30) as r:
        return json.load(r)


def slug_to_name(companies, entity_id):
    for c in companies:
        if c["entity_id"] == entity_id:
            return c["name"]
    return entity_id


def cmd_companies(args):
    d = fetch("companies")
    rows = d["companies"]
    if args.search:
        q = args.search.lower()
        rows = [c for c in rows if q in c["name"].lower() or q in (c.get("summary") or "").lower()]
    if args.category:
        rows = [c for c in rows if (c.get("category") or "").lower() == args.category.lower()]
    print(f"release: {d['release_id'][:24]}...  matched: {len(rows)} of {len(d['companies'])}")
    for c in rows[: args.limit]:
        print(f"  {c['name']:<22} [{c.get('category', '?')}] {c.get('website', '')}")
        if c.get("summary"):
            print(f"    {c['summary'][:110]}")


def cmd_credits(args):
    d = fetch("credits")
    companies = {c["entity_id"]: c for c in fetch("companies")["companies"]}
    hits = []
    for pol in d.get("policies", []):
        blob = json.dumps(pol).lower()
        if not args.search or args.search.lower() in blob:
            hits.append(pol)
    print(f"release: {d['release_id'][:24]}...  matched policies: {len(hits)}")
    for pol in hits[: args.limit]:
        ent = pol.get("entity_id", "")
        co = companies.get(ent, {})
        print(f"  {co.get('name', ent):<22} {pol.get('policy_id', '')[:30]}")
        offer = (pol.get("headline") or pol.get("summary") or json.dumps(pol)[:90])
        print(f"    {str(offer)[:110]}")


def cmd_readiness(args):
    d = fetch("readiness")
    companies = {c["entity_id"]: c for c in fetch("companies")["companies"]}
    rows = d["profiles"]
    if args.entity:
        want = companies.get(args.entity, {}).get("entity_id")
        rows = [p for p in rows if want and p["entity_id"] == want]
    if args.grade:
        rows = [p for p in rows if (p.get("grade") or "").upper().startswith(args.grade.upper())]
    print(f"release: {d['release_id'][:24]}...  profiles: {len(rows)} of {len(d['profiles'])}")
    for p in rows[: args.limit]:
        co = companies.get(p["entity_id"], {})
        scope = p.get("scope", {}).get("product", {}).get("name", "")
        funnel = p.get("scope", {}).get("funnel", {}).get("name", "")
        print(f"  {co.get('name', p['entity_id']):<22} {scope[:28]:<30} grade={p.get('grade', '?'):<2} {funnel[:30]}")
        pf = p.get("primary_finding")
        if pf:
            if isinstance(pf, dict):
                stage = pf.get("stage_label") or pf.get("stage") or ""
                finding = pf.get("finding") or {}
                sig = finding.get("signal_code") if isinstance(finding, dict) else finding
                txt = f"{stage}: {sig}" if stage else str(sig)
            else:
                txt = str(pf)
            print(f"    {txt[:110]}")


def cmd_stats(args):
    comps = fetch("companies")
    red = fetch("readiness")
    cats = {}
    for c in comps["companies"]:
        cats[c.get("category") or "uncategorized"] = cats.get(c.get("category") or "uncategorized", 0) + 1
    print(f"companies: {len(comps['companies'])}  release: {comps['release_id'][:24]}...")
    print(f"readiness profiles: {len(red['profiles'])}  release: {red['release_id'][:24]}...")
    print("by category:")
    for k, v in sorted(cats.items(), key=lambda x: -x[1]):
        print(f"  {k:<24} {v}")


def main():
    ap = argparse.ArgumentParser(description="Query the Sourcey open registry")
    sub = ap.add_subparsers(dest="cmd", required=True)
    p1 = sub.add_parser("companies")
    p1.add_argument("--search"); p1.add_argument("--category"); p1.add_argument("--limit", type=int, default=20)
    p2 = sub.add_parser("credits")
    p2.add_argument("--search"); p2.add_argument("--limit", type=int, default=20)
    p3 = sub.add_parser("readiness")
    p3.add_argument("--entity"); p3.add_argument("--grade"); p3.add_argument("--limit", type=int, default=25)
    sub.add_parser("stats")
    args = ap.parse_args()
    {"companies": cmd_companies, "credits": cmd_credits,
     "readiness": cmd_readiness, "stats": cmd_stats}[args.cmd](args)


if __name__ == "__main__":
    main()
