"""Agent Engine を削除する(配下のセッション・記憶も削除される)。"""
import vertexai
from common.config import PROJECT_ID, LOCATION, AGENT_ENGINE_NAME

client = vertexai.Client(project=PROJECT_ID, location=LOCATION)
client.agent_engines.delete(name=AGENT_ENGINE_NAME, force=True)
print("Deleted:", AGENT_ENGINE_NAME)