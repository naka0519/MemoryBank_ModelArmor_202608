"""全チュートリアル共通の設定。環境変数から読み込む。"""
import os

# 必須(§0-4 で export 済みであること)
PROJECT_ID = os.environ["GOOGLE_CLOUD_PROJECT"]
LOCATION = os.environ.get("GOOGLE_CLOUD_LOCATION", "us-central1")

# A-2 実行後に export する(未設定のうちは空文字)
AGENT_ENGINE_ID = os.environ.get("AGENT_ENGINE_ID", "")

# Memory Bank のリソース名(scope の app_name にも使うアプリ名)
APP_NAME = "car_agent"
AGENT_ENGINE_NAME = (
    f"projects/{PROJECT_ID}/locations/{LOCATION}"
    f"/reasoningEngines/{AGENT_ENGINE_ID}"
)

# Model Armor テンプレート(B-1 / C-2 で作成するIDと一致させる)
MA_TEMPLATE_ID = "ma-test-template"
MA_PII_TEMPLATE_ID = "ma-pii-template"
MA_ENDPOINT = f"modelarmor.{LOCATION}.rep.googleapis.com"
MA_TEMPLATE = f"projects/{PROJECT_ID}/locations/{LOCATION}/templates/{MA_TEMPLATE_ID}"
MA_PII_TEMPLATE = f"projects/{PROJECT_ID}/locations/{LOCATION}/templates/{MA_PII_TEMPLATE_ID}"

# ADK が Vertex AI(Agent Platform)を使うための設定
os.environ.setdefault("GOOGLE_GENAI_USE_ENTERPRISE", "TRUE")  # ドキュメント記載の設定(旧: GOOGLE_GENAI_USE_VERTEXAI)