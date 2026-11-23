#!/bin/bash
set -euo pipefail

./scripts/build_lambda.sh

for function_name in upload put; do
  aws lambda update-function-code \
    --function-name "$function_name" \
    --zip-file fileb://build/lambda.zip \
    --query "[FunctionName, LastUpdateStatus]"
done