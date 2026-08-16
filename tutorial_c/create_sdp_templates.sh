#!/usr/bin/env bash
# SDP の検査テンプレート・匿名化テンプレートを作成する
set -euo pipefail
: "${PROJECT_ID:?}" "${LOCATION:?}"
TOKEN="$(gcloud auth print-access-token)"

gcloud services enable dlp.googleapis.com

# 検査テンプレート: 検出したい infoType を定義
curl -s -X POST \
  -H "Authorization: Bearer ${TOKEN}" \
  -H "Content-Type: application/json" \
  -d '{
    "templateId": "pii-inspect",
    "inspectTemplate": {
      "inspectConfig": {
        "infoTypes": [
          {"name": "PERSON_NAME"},
          {"name": "EMAIL_ADDRESS"},
          {"name": "PHONE_NUMBER"},
          {"name": "CREDIT_CARD_NUMBER"},
          {"name": "JAPAN_INDIVIDUAL_NUMBER"}
        ]
      }
    }
  }' \
  "https://dlp.googleapis.com/v2/projects/${PROJECT_ID}/locations/${LOCATION}/inspectTemplates"
echo

# 匿名化テンプレート: 検出箇所を infoType 名のトークンに置換
curl -s -X POST \
  -H "Authorization: Bearer ${TOKEN}" \
  -H "Content-Type: application/json" \
  -d '{
    "templateId": "pii-deidentify",
    "deidentifyTemplate": {
      "deidentifyConfig": {
        "infoTypeTransformations": {
          "transformations": [
            {"primitiveTransformation": {"replaceWithInfoTypeConfig": {}}}
          ]
        }
      }
    }
  }' \
  "https://dlp.googleapis.com/v2/projects/${PROJECT_ID}/locations/${LOCATION}/deidentifyTemplates"
echo