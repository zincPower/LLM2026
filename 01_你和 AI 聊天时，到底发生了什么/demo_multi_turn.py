"""
多轮对话

运行方式:
  export GOOGLE_API_KEY="your-api-key-here"
  python demo_multi_turn.py
"""

import os
import sys

from google import genai
from google.genai import types

def main():
    api_key = os.environ.get("GOOGLE_API_KEY")
    if not api_key:
        print("❌ 请先设置环境变量 GOOGLE_API_KEY")
        print('   export GOOGLE_API_KEY="your-api-key-here"')
        sys.exit(1)
    client = genai.Client(api_key=api_key)

    print("=" * 60)
    print("💬 多轮对话")
    print("=" * 60)

    system_instruction = "你是一个友好的编程助手。回答要简洁,不超过两句话。"

    history = []

    conversations = [
        "我叫江澎涌,我正在学 Python",
        "我刚才说我叫什么?",
        "我在学什么编程语言?",
    ]

    for round_idx, user_msg in enumerate(conversations, start=1):
        print(f"\n{'═' * 60}")
        print(f"🔄 第 {round_idx} 轮")
        print(f"{'═' * 60}")

        # 把这一轮的用户消息追加进历史
        history.append(types.Content(
            role="user",
            parts=[types.Part(text=user_msg)],
        ))

        print(f"\n📤 这次发出去的 contents (共 {len(history)} 条 message):")
        for i, msg in enumerate(history, 1):
            text = msg.parts[0].text
            print(f"   [{i}] {msg.role:9s}: {text}")

        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=history,
            config=types.GenerateContentConfig(
                system_instruction=system_instruction,
                thinking_config=types.ThinkingConfig(thinking_budget=0),
            ),
        )

        assistant_text = response.text.strip()
        print(f"\n🤖 Assistant: {assistant_text}")

        # 输入 Token 在每一轮都会变多——这就是"重发历史"的真实代价
        if response.usage_metadata:
            print(
                f"📊 本轮 Token: "
                f"输入={response.usage_metadata.prompt_token_count}, "
                f"输出={response.usage_metadata.candidates_token_count}, "
                f"总计={response.usage_metadata.total_token_count}"
            )

        # 把 assistant 的回复也追加进历史,供下一轮重发时使用
        history.append(types.Content(
            role="model",
            parts=[types.Part(text=assistant_text)],
        ))

if __name__ == "__main__":
    main()