"""Runner とサービス群の構築、およびエージェント呼び出しの共通関数。"""
from google import adk
from google.adk.memory import VertexAiMemoryBankService
from google.adk.sessions import VertexAiSessionService
from google.genai import types

from common.config import PROJECT_ID, LOCATION, AGENT_ENGINE_ID, APP_NAME


def build_services():
    """Session / Memory サービスを構築する。"""
    assert AGENT_ENGINE_ID, "AGENT_ENGINE_ID が未設定です(§A-2 参照)"
    memory_service = VertexAiMemoryBankService(
        project=PROJECT_ID, location=LOCATION,
        agent_engine_id=AGENT_ENGINE_ID,
    )
    session_service = VertexAiSessionService(
        project=PROJECT_ID, location=LOCATION,
        agent_engine_id=AGENT_ENGINE_ID,
    )
    return session_service, memory_service


def build_runner(agent):
    """任意のエージェントで Runner を構築する(§3・Cでも再利用)。"""
    session_service, memory_service = build_services()
    runner = adk.Runner(
        agent=agent,
        app_name=APP_NAME,        # scope に含まれ、アプリ間で記憶が分離される
        session_service=session_service,
        memory_service=memory_service,
    )
    return runner, session_service


async def call_agent(runner, query: str, session_id: str, user_id: str):
    """1ターン分の対話を実行して最終応答を表示する。"""
    content = types.Content(role="user", parts=[types.Part(text=query)])
    async for event in runner.run_async(
            user_id=user_id, session_id=session_id, new_message=content):
        if event.is_final_response():
            print("Agent:", event.content.parts[0].text)