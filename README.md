# QSO Graph website

The site uses Astro Starlight. Hand-written pages use Markdoc; fetched Markdown uses Astro’s GFM pipeline, and fetched `.mdoc` files use Markdoc. The fetcher allows common HTML elements and attributes, removes script, style, iframe, object and embed elements, event handlers and JavaScript URLs, and strips other non-allowlisted tags and attributes. Install Node 24 or later and [uv](https://docs.astral.sh/uv/), then run `make install`, `make docs`, `make data`, and `make build`. Set `GITHUB_TOKEN` when fetching to avoid GitHub's rate limit. Run `make serve` to preview locally.

Public, non-archived repositories opt in with a `qso-graph-app`, `qso-graph-mcp`, `qso-graph-library`, or `qso-graph-tool` topic; infrastructure is excluded. The latest stable GitHub Release supplies `README.md` and `docs/user/`; `docs.lock` is a JSON object mapping repository names to pinned tags.

The daily deployment fetches documentation, collects released server metadata, builds the site, and publishes to the `gh-pages` branch. Pull requests build without publishing.
