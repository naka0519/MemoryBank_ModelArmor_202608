"""Memory Bank 連携付きの車載ボイスエージェント定義。"""
from google import adk
from google.adk.agents.callback_context import CallbackContext
from google.adk.tools.preload_memory_tool import PreloadMemoryTool


# エージェント実行後に、そのセッションを Memory Bank へ送り記憶生成をトリガー
async def generate_memories_callback(callback_context: CallbackContext):
    # 推奨: 直近イベントのみ送る add_events_to_memory(増分処理向け)
    # ここでは簡単のためセッション全体を送る
    await callback_context.add_session_to_memory()
    return None


agent = adk.Agent(
    model="gemini-2.5-flash",   # 利用可能な Gemini モデルを指定
    name="stateful_agent",
    instruction="""あなたは車載ボイスエージェントです。
- 車両操作の依頼(例: エアコンをつけて)には仮の実行結果を答える
- 必要なら好みを確認する
- 回答は30語以内で簡潔に""",
    tools=[PreloadMemoryTool()],            # 毎ターン開始時に記憶を自動取得
    after_agent_callback=generate_memories_callback,  # 毎ターン終了時に記憶生成
)

# adk web(A-8)がエージェントを発見するための変数名
root_agent = agent