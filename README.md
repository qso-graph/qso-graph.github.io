# QSO Graph website

The site uses Docusaurus 3 and its classic theme. Fetched `.md` files are processed as Markdown; hand-written pages use MDX. The fetcher sanitizes HTML in released documentation. Search is self-hosted with `@easyops-cn/docusaurus-search-local` (MIT).

Install Node 24 or later and [uv](https://docs.astral.sh/uv/), then run `make install`, `make docs`, `make data`, and `make build`. Set `GITHUB_TOKEN` when fetching to avoid GitHub's rate limit. Run `make serve` to preview locally. `npm ci` installs the exact dependency versions in the lockfile.

Public, non-archived repositories opt in with a `qso-graph-app`, `qso-graph-mcp`, `qso-graph-library`, or `qso-graph-tool` topic; infrastructure is excluded. The latest stable GitHub Release supplies `README.md` and `docs/user/`; `docs.lock` is a JSON object mapping repository names to pinned tags.

The daily deployment tests the scripts, fetches documentation, collects released server metadata, builds into `build/`, and publishes to the `gh-pages` branch. Pull requests build without publishing.
