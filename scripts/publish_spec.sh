#!/bin/bash
# publish_spec.sh — release the QSO Graph specification and publish it on qso-graph.io now.
#
#   make publish-spec VERSION=v1.1 [NOTES="what changed"]
#
# Tags qso-graph-spec's main as VERSION (annotated; NOTES, default "QSO-GRAPH-SPEC <VERSION>", is the
# tag's message), starts this site's deploy, and waits until https://qso-graph.io/spec/ shows that
# version. The site imports the highest vX.Y.Z tag (spec.lock: latest), so the tag IS the publication;
# without this, the daily build would publish it within a day anyway.
#
# The spec's changes are merged first, by their own PRs (governed: README of qso-graph-spec). This only
# tags what is on main.
#
# Checks, each of which stops it: VERSION is vX.Y.Z; it isn't tagged yet; it is newer than the last
# release. Uses the gh CLI as whoever runs it (GH_TOKEN, or gh's own login), with permission to make tags
# on qso-graph-spec and run workflows on this site.
#
# Runs on Linux and macOS (bash 3.2, no GNU-only tools).
set -Eeuo pipefail

VERSION="${VERSION:-}"
NOTES="${NOTES:-}"
SPEC=qso-graph/qso-graph-spec
SITE=qso-graph/qso-graph.github.io

die() { echo "publish-spec: $*" >&2; exit 1; }
say() { echo "publish-spec: $*"; }

# A vX.Y.Z tag as one comparable number (each part below 1000).
num() { local v="${1#v}" a b c; IFS=. read -r a b c <<EOF
$v
EOF
  echo $(( a * 1000000 + b * 1000 + c )); }

case "$VERSION" in
  v*.*.*) echo "$VERSION" | grep -Eq '^v[0-9]+\.[0-9]+\.[0-9]+$' || die "VERSION=vX.Y.Z (got '$VERSION')" ;;
  *) die "VERSION=vX.Y.Z (got '$VERSION')" ;;
esac
command -v gh >/dev/null || die "the gh CLI is needed"

if gh api "repos/$SPEC/git/ref/tags/$VERSION" >/dev/null 2>&1; then
  die "$VERSION is already tagged"
fi
latest=""
for t in $(gh api --paginate "repos/$SPEC/tags?per_page=100" --jq '.[].name'); do
  echo "$t" | grep -Eq '^v[0-9]+\.[0-9]+\.[0-9]+$' || continue
  if [ -z "$latest" ] || [ "$(num "$t")" -gt "$(num "$latest")" ]; then latest="$t"; fi
done
if [ -n "$latest" ] && [ "$(num "$VERSION")" -le "$(num "$latest")" ]; then
  die "$VERSION isn't newer than the last release, $latest"
fi

main="$(gh api "repos/$SPEC/commits/main" --jq .sha)"
subject="$(gh api "repos/$SPEC/commits/main" --jq '.commit.message | split("\n")[0]')"
say "tagging $VERSION on ${main:0:7} ($subject); last release: ${latest:-none}"
obj="$(gh api "repos/$SPEC/git/tags" -f tag="$VERSION" -f message="${NOTES:-QSO-GRAPH-SPEC $VERSION}" \
        -f object="$main" -f type=commit --jq .sha)"
gh api "repos/$SPEC/git/refs" -f ref="refs/tags/$VERSION" -f sha="$obj" --jq .ref >/dev/null
say "tagged"

before="$(gh run list -R "$SITE" --workflow deploy.yml --limit 1 --json databaseId --jq '.[0].databaseId // 0')"
gh workflow run deploy.yml -R "$SITE" --ref main >/dev/null
run=""
for i in 1 2 3 4 5 6 7 8 9 10 11 12; do
  sleep 5
  run="$(gh run list -R "$SITE" --workflow deploy.yml --limit 1 --json databaseId --jq '.[0].databaseId // 0')"
  [ "$run" != "$before" ] && break
done
[ -n "$run" ] && [ "$run" != "$before" ] || die "the site's deploy didn't start; run it from https://github.com/$SITE/actions"
say "deploying the site (https://github.com/$SITE/actions/runs/$run)"
gh run watch "$run" -R "$SITE" --exit-status >/dev/null || die "the deploy failed: https://github.com/$SITE/actions/runs/$run"

for i in $(seq 1 30); do
  # Read the page whole, then match: piping curl into grep -q ends the read early, curl reports a write
  # error, and with pipefail that counts as a miss even when the version is there.
  page="$(curl -fsS "https://qso-graph.io/spec/?v=$(date +%s)" 2>/dev/null || true)"
  if [[ "$page" == *"QSO-GRAPH-SPEC $VERSION"* ]]; then
    say "live: https://qso-graph.io/spec/ shows $VERSION"
    exit 0
  fi
  sleep 10
done
die "deployed, but https://qso-graph.io/spec/ doesn't show $VERSION after 5 minutes (GitHub Pages can lag; check again shortly)"
