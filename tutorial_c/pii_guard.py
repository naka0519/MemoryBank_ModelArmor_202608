"""PII 検査付き記憶化ガード: Memory Bank への書き込み前に Model Armor SDP で検査する。"""
from google import adk
from google.adk.agents.callback_context import CallbackContext
from google.adk.tools.preload_memory_tool import PreloadMemoryTool
from google.api_core.client_options import ClientOptions
from google.cloud import modelarmor_v1

from common.config import MA_ENDPOINT, MA_PII_TEMPLATE

ma_client = modelarmor_v1.ModelArmorClient(
    transport="rest",
    client_options=ClientOptions(api_endpoint=MA_ENDPOINT),
)

# 方式の切り替え: "block"(方式1) / "mask"(方式2)
GUARD_MODE = "mask"


def screen_pii(text: str):
    """Model Armor で PII を検査し、(検出有無, 匿名化テキスト) を返す"""
    res = ma_client.sanitize_user_prompt(
        request=modelarmor_v1.SanitizeUserPromptRequest(
            name=MA_PII_TEMPLATE,
            user_prompt_data=modelarmor_v1.DataItem(text=text)))
    sdp = res.sanitization_result.filter_results["sdp"].sdp_filter_result
    deid = sdp.deidentify_result
    matched = (deid.match_state == modelarmor_v1.FilterMatchState.MATCH_FOUND)
    sanitized = deid.data.text if matched else text
    return matched, sanitized


async def pii_guarded_memory_callback(callback_context: CallbackContext):
    # 直近のユーザー発話テキストを抽出
    events = callback_context.session.events[-5:]
    user_texts = []
    for ev in events:
        if ev.content and ev.content.role == "user" and ev.content.parts:
            user_texts.append(
                "".join(p.text or "" for p in ev.content.parts))

    pii_found = False
    sanitized_texts = []
    for t in user_texts:
        matched, sanitized = screen_pii(t)
        pii_found = pii_found or matched
        sanitized_texts.append(sanitized)

    if not pii_found:
        # PII なし → 通常どおり記憶化
        await callback_context.add_session_to_memory()
        return None

    if GUARD_MODE == "block":
        # ===== 方式1(ブロック): PII 検出時は記憶化をスキップ =====
        print("[PII Guard] PII detected. Memory generation skipped.")
        return None

    # ===== 方式2(匿名化): 匿名化済みテキストから記憶を生成 =====
    # 会話イベントの代わりに、匿名化済みテキストを直接ソースとして
    # GenerateMemories を呼び出す(SDK バージョンによりシグネチャ要確認)。
    import vertexai
    from common.config import (PROJECT_ID, LOCATION,
                               AGENT_ENGINE_NAME, APP_NAME)
    client = vertexai.Client(project=PROJECT_ID, location=LOCATION)
    for t in sanitized_texts:
        print("Sanitize: ", t)
    client.agent_engines.memories.generate(
        name=AGENT_ENGINE_NAME,
        direct_contents_source={"events": [
            {"content": {"role": "user",
                         "parts": [{"text": t}]}} for t in sanitized_texts
        ]},
        scope={"app_name": APP_NAME,
               "user_id": callback_context._invocation_context.user_id},
    )
    print("[PII Guard] PII masked. Sanitized memory generated.")
    return None


agent = adk.Agent(
    model="gemini-2.5-flash",
    name="pii_guarded_agent",
    instruction="""あなたは車載ボイスエージェントです。
- 車両操作の依頼には仮の実行結果を答える
- 必要なら好みを確認する
- 回答は30語以内で簡潔に""",
    tools=[PreloadMemoryTool()],
    after_agent_callback=pii_guarded_memory_callback,
)