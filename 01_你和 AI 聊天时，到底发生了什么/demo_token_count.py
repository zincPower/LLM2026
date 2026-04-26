"""
查看 Token 用量

运行方式：
  export GOOGLE_API_KEY="your-api-key-here"
  python demo_token_count.py
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
    print("🔍 查看 Token 用量")
    print("=" * 60)

    prompt = "用一句话解释什么是 Token"
    print(f'\n📌 Prompt: "{prompt}"')

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt,
        # gemini-2.5-flash 默认开启 thinking，会多消耗几百个思考 Token，导致 total_token_count > input + output。
        # 这里关掉 thinking，则 total = input + output 。
        config=types.GenerateContentConfig(
            thinking_config=types.ThinkingConfig(thinking_budget=0),
        ),
    )

    print(f"\n📝 模型回复：{response.text}")

    if response.usage_metadata:
        print(f"\n📊 Token 用量统计：")
        print(f"   输入 Token 数（prompt）:  {response.usage_metadata.prompt_token_count}")
        print(f"   输出 Token 数（response）: {response.usage_metadata.candidates_token_count}")
        print(f"   总 Token 数:              {response.usage_metadata.total_token_count}")
    else:
        print("\n⚠️ 未获取到 Token 用量信息")

if __name__ == "__main__":
    main()