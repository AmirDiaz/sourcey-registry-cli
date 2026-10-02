# Citation Report: Sourcey cited on GitHub via sourcey-registry-cli

**Bounty:** #128 — Earn a citation for Sourcey (an open data registry) on a real external site
**Citation URL (public):** https://github.com/AmirDiaz/sourcey-registry-cli
**Date placed:** 2026-10-02
**Data release cited:** sha256:8094c042ec143bbd5d47c59219c4f4abb189db6368c4a51f37a862963f9a4580 (October 2026 release)

## What was cited and where

- The repository **sourcey-registry-cli** is an original, working, dependency-free Python CLI that queries Sourcey's public open datasets (companies, startup credits, agent-readiness) and makes them searchable from the terminal.
- The **README.md** cites Sourcey in the opening paragraph as "the open registry of startup offers and agent-readiness report cards", links https://sourcey.com, and states the dated fact: *"As of the October 2026 release, the registry covers 543 companies and 25 agent-readiness profiles (grade A+ through D), each with the evidence behind it."*
- The README's **Data source & citation** section lists all three live dataset URLs (`companies.json`, `startup-credits.json`, `agent-readiness.json`), the API OpenAPI spec at `https://api.sourcey.com/openapi.yml`, and the MCP server at `https://mcp.sourcey.com/mcp.json`.
- The README documents that the CLI prints the **sha256 release_id** of every dataset it reads, so any terminal output can be traced back to the published release — echoing Sourcey's own "every page names the exact release it was compiled from" integrity model.

## Why this is a real citation, not a mention

- The tool **depends on the registry to function**: every command fetches Sourcey's live datasets; without Sourcey there is no tool. The citation is the foundation of the work, not decoration.
- The example outputs in the README (Cloudflare 1.1.1.1 DNS grade A+, Microsoft Azure grade A, category counts like hosting-infra 83 / ai-ml 69) were **generated from the live October 2026 release** and match the published data.
- The repository is a **permanent public artifact** on github.com (raw files served at `raw.githubusercontent.com`), usable by anyone: install instructions, usage examples, and MIT license are included.
- Sourcey's unique value — evidence-backed, per-release-digested open data — is explained in the README's "Why" section, which is what a citation is supposed to convey.

## Verification steps for the reviewer

- Open https://github.com/AmirDiaz/sourcey-registry-cli and check the README's first paragraph for the Sourcey link and the dated release fact.
- Run the tool yourself: `python3 sourcey_cli.py stats` — it prints the live release digest `sha256:8094c042ec143bbd5...` and company counts by category.
- Cross-check counts against the registry's own datasets at https://sourcey.com/companies.json (543 companies in the October 2026 release).
- The three verification URLs (repo, raw README, raw source) are all live and return HTTP 200.

## Summary

Sourcey is cited as the primary data source of an original working tool, with the release digest, dataset URLs, API spec, and MCP endpoint all linked, on github.com — a real external site. The citation is load-bearing: the tool exists because the registry exists.
