"""Model Armor 入力ガード付きエージェント(インジェクション/メモリ ポイズニング対策)。"""
from google import adk
from google.adk.agents.callback_context import CallbackContext
from google.adk.models import LlmRequest, LlmResponse
from google.adk.tools.preload_memory_tool import PreloadMemoryTool
from google.genai import types
from google.api_core.client_options import ClientOptions
from google.cloud import modelarmor_v1

from common.config import MA_ENDPOINT, MA_TEMPLATE
from tutorial_a.agent import generate_memories_callback   # A-3 のコールバックを再利用

ma_client = modelarmor_v1.ModelArmorClient(
    transport="rest",
    client_options=ClientOptions(api_endpoint=MA_ENDPOINT),
)


def model_armor_guard(callback_context: CallbackContext,
                      llm_request: LlmRequest) -> LlmResponse | None:
    # 直近のユーザー入力テキストを抽出
    user_text = ""
    for content in reversed(llm_request.contents or []):
        if content.role == "user" and content.parts:
            user_text = "".join(p.text or "" for p in content.parts)
            break
    if not user_text:
        return None

    res = ma_client.sanitize_user_prompt(
        request=modelarmor_v1.SanitizeUserPromptRequest(
            name=MA_TEMPLATE,
            user_prompt_data=modelarmor_v1.DataItem(text=user_text)))

    if res.sanitization_result.filter_match_state == \
            modelarmor_v1.FilterMatchState.MATCH_FOUND:
        # LLM 呼び出しをスキップし、固定応答を返す(=記憶生成にも汚染入力が渡らない)
        return LlmResponse(content=types.Content(
            role="model",
            parts=[types.Part(text="このリクエストはセキュリティポリシーによりブロックされました。")]))
    return None


agent = adk.Agent(
    model="gemini-2.5-flash",
    name="guarded_stateful_agent",
    instruction="""あなたは車載ボイスエージェントです。
- 車両操作の依頼には仮の実行結果を答える
- 必要なら好みを確認する
- 回答は30語以内で簡潔に""",
    tools=[PreloadMemoryTool()],
    before_model_callback=model_armor_guard,          # 入口ガード
    after_agent_callback=generate_memories_callback,  # 記憶生成
)