# QSO Graph website

Install dependencies with `make install`, fetch documentation with `make docs` (`GITHUB_TOKEN` set avoids GitHub's rate limit), collect package data with `make data`, and build with `mkdocs build --strict`.
Public, non-archived repositories opt in with a `qso-graph-app`, `qso-graph-mcp`, `qso-graph-library`, or `qso-graph-tool` topic; infrastructure is excluded.
The latest stable GitHub Release supplies `README.md` and `docs/user/`; `docs.lock` can pin an exception.

`docs.lock` is a JSON object mapping repository names to pinned tags.
