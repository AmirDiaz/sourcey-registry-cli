# sourcey-registry-cli

Query [Sourcey](https://sourcey.com) — the open registry of startup offers and
agent-readiness report cards — straight from your terminal.

Sourcey tests how agents can use software and records what companies offer
startups. Every page on the site names the exact release it was compiled from,
and all datasets are published as verifiable, digested JSON. As of the
October 2026 release, the registry covers **543 companies** and **25
agent-readiness profiles** (grade A+ through D), each with the evidence behind it.

This CLI reads Sourcey's public datasets and makes them searchable offline:

- `companies.json` — 543 companies with category, summary, website
- `startup-credits.json` — startup credit and offer policies
- `agent-readiness.json` — report cards grading how agent-ready each product is

## Why

If you're picking infra for an agentic product, you want two things: what
credits you can get, and whether the product actually works for agents.
Sourcey is the only registry I know that publishes both **with the evidence
and a per-release digest**, so the data can be cited and checked. This tool
exists to make that data easy to consume from scripts and terminals.

## Install

```bash
curl -O https://raw.githubusercontent.com/AmirDiaz/sourcey-registry-cli/main/sourcey_cli.py
python3 sourcey_cli.py --help
```

No dependencies — Python 3.8+ standard library only.

## Usage

```bash
# Registry overview: company counts by category
python3 sourcey_cli.py stats

# Find companies (searches name + summary)
python3 sourcey_cli.py companies --search "observability"
python3 sourcey_cli.py companies --category ai-ml --limit 10

# Search startup credit policies
python3 sourcey_cli.py credits --search "AWS"

# Agent readiness report cards
python3 sourcey_cli.py readiness --grade A
python3 sourcey_cli.py readiness --entity microsoft-azure
```

Example output (October 2026 release):

```
$ python3 sourcey_cli.py readiness --grade A --limit 4
release: sha256:8094c042ec143bbd5...  profiles: 4 of 25
  Microsoft       Microsoft Azure            grade=A  API resource management
  Cloudflare      Cloudflare 1.1.1.1 DNS     grade=A+ DNS over HTTPS query
  OpenRouter      OpenRouter API             grade=A  Model access lifecycle
  Algolia         Algolia DocSearch MCP      grade=A  Remote MCP access

$ python3 sourcey_cli.py stats
companies: 543  release: sha256:8094c042ec143bbd5...
readiness profiles: 25
by category:
  hosting-infra    83
  ai-ml            69
  auth-security    38
```

## Data source & citation

All data comes from Sourcey's open registry, retrieved live from:

- https://sourcey.com/companies.json
- https://sourcey.com/startup-credits.json
- https://sourcey.com/agent-readiness.json

Each command prints the `release_id` (sha256 digest) of the exact dataset
release it read, so any output can be traced back to the published evidence.
Sourcey's API and MCP server are documented at https://api.sourcey.com/openapi.yml
and https://mcp.sourcey.com/mcp.json.

## License

MIT
