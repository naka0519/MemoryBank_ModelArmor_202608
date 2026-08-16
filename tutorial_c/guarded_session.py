"""ガード付きエージェントで PII 混入防止の検証シナリオを実行する。"""
import asyncio

from tutorial_c.pii_guard import agent
from tutorial_a.runner import build_runner, call_agent

USER_ID = "pii-test-user-005"   # ベースライン(001)と分ける


async def main():
    runner, session_service = build_runner(agent)

    # シナリオ1: PII なし → 記憶化される
    s1 = await session_service.create_session(
        app_name=runner.app_name, user_id=USER_ID)
    await call_agent(runner, "温度は21度が好きです", s1.id, USER_ID)

    # シナリオ2: PII あり → 方式1: 記憶化されない / 方式2: 匿名化して記憶化
    s2 = await session_service.create_session(
        app_name=runner.app_name, user_id=USER_ID)
    await call_agent(
        runner,
        "私は山田太郎、メールは taro.yamada@example.com。22度に変えて",
        s2.id, USER_ID)

    # シナリオ3: 新セッションで想起確認(PII が記憶から出てこないこと)
    s3 = await session_service.create_session(
        app_name=runner.app_name, user_id=USER_ID)
    await call_agent(runner, "温度なおして", s3.id, USER_ID)

    await asyncio.sleep(3)


if __name__ == "__main__":
    asyncio.run(main())