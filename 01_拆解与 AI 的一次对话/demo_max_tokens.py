"""
Max Tokens

运行方式：
  export GOOGLE_API_KEY="your-api-key-here"
  python demo_max_tokens.py
"""

import os
import sys

from google import genai
from google.genai import types

MAX_OUTPUT_TOKENS = 50

def main():
    api_key = os.environ.get("GOOGLE_API_KEY")
    if not api_key:
        print("❌ 请先设置环境变量 GOOGLE_API_KEY")
        print('   export GOOGLE_API_KEY="your-api-key-here"')
        sys.exit(1)
    client = genai.Client(api_key=api_key)

    print("=" * 60)
    print("✂️ Max Tokens")
    print("=" * 60)

    prompt = "详细介绍 Python 的十大特性"

    print(f"\n📌 Prompt: \"{prompt}\"")
    print(f"   max_output_tokens = {MAX_OUTPUT_TOKENS}\n")

    # 关掉 thinking——否则这 max_output_tokens 个 token 会被思考阶段吃光，
    # 最终可见输出只剩几个字，max_tokens 的截断效果看不到。
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt,
        config=types.GenerateContentConfig(
            max_output_tokens=MAX_OUTPUT_TOKENS,
            thinking_config=types.ThinkingConfig(thinking_budget=0),
        ),
    )

    print(f"📝 模型回复：\n{response.text}")

    if response.candidates:
        finish_reason = response.candidates[0].finish_reason
        print(f"\n📊 停止原因: {finish_reason}")

if __name__ == "__main__":
    main()