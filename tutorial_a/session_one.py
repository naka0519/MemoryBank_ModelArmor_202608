"""セッション1: エージェントに温度の好みを教える。"""
import asyncio

from tutorial_a.agent import agent
from tutorial_a.runner import build_runner, call_agent

USER_ID = "test-user-001"


async def main():
    runner, session_service = build_runner(agent)
    session = await session_service.create_session(
        app_name=runner.app_name, user_id=USER_ID)
    await call_agent(runner, "温度を調整して", session.id, USER_ID)      # → 好みを聞き返してくるはず
    await call_agent(runner, "私は21度が快適です", session.id, USER_ID)  # → 記憶が生成されるはず


if __name__ == "__main__":
    asyncio.run(main())