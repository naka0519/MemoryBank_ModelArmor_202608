#!/usr/bin/env bash
# チュートリアルCで作成したテンプレート類を削除する
set -euo pipefail
: "${PROJECT_ID:?}" "${LOCATION:?}"
TOKEN="$(gcloud auth print-access-token)"

# Model Armor テンプレート
gcloud model-armor templates delete ma-pii-template --location=${LOCATION} --quiet

# SDP テンプレート
curl -s -X DELETE -H "Authorization: Bearer ${TOKEN}" \
  "https://dlp.googleapis.com/v2/projects/${PROJECT_ID}/locations/${LOCATION}/inspectTemplates/pii-inspect"
curl -s -X DELETE -H "Authorization: Bearer ${TOKEN}" \
  "https://dlp.googleapis.com/v2/projects/${PROJECT_ID}/locations/${LOCATION}/deidentifyTemplates/pii-deidentify"