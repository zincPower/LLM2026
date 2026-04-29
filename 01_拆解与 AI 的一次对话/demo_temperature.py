"""
Temperature 对比实验

对比 Temperature 0.0 vs 1.0 的效果。
Temperature 越低越确定，越高越有创造力。

运行方式：
  export GOOGLE_API_KEY="your-api-key-here"
  python demo_temperature.py
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
    print("🌡️ Temperature 对比实验")
    print("=" * 60)

    prompt = "给一只橘色的猫起个名字，只回复名字，不要解释。"

    print(f"\n📌 Prompt: \"{prompt}\"")
    print(f"\n--- 使用 Temperature = 0.0（最确定，结果趋于一致）---")

    for i in range(3):
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt,
            config=types.GenerateContentConfig(temperature=0.0),
        )
        print(f"   第 {i + 1} 次: {response.text.strip()}")

    print(f"\n--- 使用 Temperature = 1.0（更随机，结果可能不同）---")

    for i in range(3):
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt,
            config=types.GenerateContentConfig(temperature=1.0),
        )
        print(f"   第 {i + 1} 次: {response.text.strip()}")

if __name__ == "__main__":
    main()
