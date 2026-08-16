"""Agent Engine(Memory Bank 含む)をデフォルト構成で作成する。"""
import vertexai
from common.config import PROJECT_ID, LOCATION

client = vertexai.Client(project=PROJECT_ID, location=LOCATION)

memory_bank = client.agent_engines.create()
name = memory_bank.api_resource.name
# 例: projects/xxx/locations/us-central1/reasoningEngines/1234567890
print("Created:", name)
print("\n以下を実行して環境変数に設定してください:")
print(f'export AGENT_ENGINE_ID="{name.split("/")[-1]}"')