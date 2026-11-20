#!/bin/bash
set -euo pipefail

./scripts/build_lambda.sh

aws lambda update-function-code \
  --function-name upload \
  --zip-file fileb://build/lambda.zip \
  --query "[FunctionName, LastUpdateStatus]"