#!/usr/bin/env bash
# Model Armor テンプレート(基本構成)の作成
set -euo pipefail
: "${PROJECT_ID:?}" "${LOCATION:?}"    # 未設定なら停止(§0-4 参照)
TEMPLATE_ID="ma-test-template"

gcloud model-armor templates create ${TEMPLATE_ID} \
  --location=${LOCATION} \
  --project=${PROJECT_ID} \
  --rai-settings-filters='[
    {"filterType":"HATE_SPEECH","confidenceLevel":"MEDIUM_AND_ABOVE"},
    {"filterType":"HARASSMENT","confidenceLevel":"MEDIUM_AND_ABOVE"},
    {"filterType":"DANGEROUS","confidenceLevel":"MEDIUM_AND_ABOVE"},
    {"filterType":"SEXUALLY_EXPLICIT","confidenceLevel":"MEDIUM_AND_ABOVE"}
  ]' \
  --pi-and-jailbreak-filter-settings-enforcement=enabled \
  --pi-and-jailbreak-filter-settings-confidence-level=MEDIUM_AND_ABOVE \
  --malicious-uri-filter-settings-enforcement=enabled \
  --basic-config-filter-enforcement=enabled \
  --template-metadata-log-operations \
  --template-metadata-log-sanitize-operations

gcloud model-armor templates list --location=${LOCATION}