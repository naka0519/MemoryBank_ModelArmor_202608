"""セッション2(新規セッション): 記憶の想起と統合を確認する。"""
import asyncio

from tutorial_a.agent import agent
from tutorial_a.runner import build_runner, call_agent

USER_ID = "test-user-001"


async def main():
    runner, session_service = build_runner(agent)
    session = await session_service.create_session(
        app_name=runner.app_name, user_id=USER_ID)   # 新しいセッション!
    await call_agent(runner, "温度なおして。不快なんだけど", session.id, USER_ID)
    # → 「21度に設定しました」等、聞き返さずに記憶を使えば成功
    await call_agent(runner, "やっぱり25度が好き", session.id, USER_ID)
    # → 既存記憶と統合され「基本21度、朝は暖かめ」に更新されるはず

    await asyncio.sleep(3)


if __name__ == "__main__":
    asyncio.run(main())