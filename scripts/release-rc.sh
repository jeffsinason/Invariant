#!/bin/bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PKG_DIR="$SCRIPT_DIR/../harness"

if [ -z "${1:-}" ]; then
  echo "Usage: $0 <rc-number>"
  echo "Example: $0 1    # produces X.Y.ZrcN"
  exit 1
fi

RC=$1

cd "$PKG_DIR"

CURRENT=$(python3 -c "
import tomllib
with open('pyproject.toml', 'rb') as f:
    print(tomllib.load(f)['project']['version'])
")
RC_VERSION="${CURRENT}rc${RC}"

echo "Releasing invariant-harness ${RC_VERSION} to TestPyPI..."

sed -i.bak "s/version = \"${CURRENT}\"/version = \"${RC_VERSION}\"/" pyproject.toml

rm -rf dist/
python3 -m build

twine upload --repository testpypi dist/*

mv pyproject.toml.bak pyproject.toml

echo ""
echo "Published ${RC_VERSION} to TestPyPI."
echo "Install with:"
echo "  pip install --index-url https://test.pypi.org/simple/ invariant-harness==${RC_VERSION}"
