"""Memory Bank に生成された記憶を list / retrieve で直接確認する。"""
import vertexai
from common.config import PROJECT_ID, LOCATION, AGENT_ENGINE_NAME, APP_NAME

USER_ID = "test-user-001"   # 確認したいユーザーIDに合わせて変更

client = vertexai.Client(project=PROJECT_ID, location=LOCATION)

print("=== 全記憶の一覧(デバッグ用) ===")
for m in client.agent_engines.memories.list(name=AGENT_ENGINE_NAME):
    print(m)

print("\n=== 類似性検索での取得(実運用と同じ経路) ===")
res = client.agent_engines.memories.retrieve(
    name=AGENT_ENGINE_NAME,
    scope={"app_name": APP_NAME, "user_id": USER_ID},
    similarity_search_params={"search_query": "温度の好み"},
)
print(res)