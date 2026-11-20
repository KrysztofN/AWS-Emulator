#!/bin/bash
set -euo pipefail

rm -rf build
mkdir -p build/package

uv export --frozen --no-dev --no-emit-project --quiet -o build/requirements.txt
uv pip install -r build/requirements.txt \
  --target build/package \
  --python-platform x86_64-manylinux2014 \
  --python-version 3.12 \
  --only-binary=:all: \
  --quiet
cp -r src/aws_emulator_proj build/package/

(cd build/package && zip -qr ../lambda.zip .)
echo "Built build/lambda.zip"