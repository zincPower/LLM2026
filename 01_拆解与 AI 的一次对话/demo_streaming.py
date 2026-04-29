"""
Streaming 流式输出

模型生成一个 Token 就返回一个，而不是等全部生成完再返回。
ChatGPT / Claude 界面上看到文字逐个蹦出来，就是这个效果。

运行方式：
  export GOOGLE_API_KEY="your-api-key-here"
  python demo_streaming.py
"""

import os
import sys
import time

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
    print("🌊 Streaming 流式输出")
    print("=" * 60)

    # 用长一点的 prompt 才能看清流式效果——太短的回复几个 chunk 就到齐了
    prompt = "请详细介绍 Python 编程语言的核心特点、典型应用场景，以及它和 JavaScript 的主要区别。分点说明，每点举一个例子，至少 600 字。"
    print(f'\n📌 Prompt: "{prompt}"')
    print("\n--- 流式输出（\033[95m▌\033[0m 是每个 chunk 的边界，注意 chunk 是分批到达的）---\n")

    response = client.models.generate_content_stream(
        model="gemini-2.5-flash",
        contents=prompt,
    )

    chunk_count = 0
    start = time.time()
    first_token_time = None
    for chunk in response:
        chunk_count += 1
        if chunk.text:
            if first_token_time is None:
                first_token_time = time.time() - start
            # 亮品红 ▌ 标出每个 chunk 的边界,让"分批到达"可见
            print("\033[95m▌\033[0m", end="", flush=True)
            print(chunk.text, end="", flush=True)

    total_time = time.time() - start
    print(f"\n\n📊 统计：")
    print(f"  - 共收到 {chunk_count} 个数据块（chunk）")
    if first_token_time is not None:
        print(f"  - 首 Token 延迟：{first_token_time:.2f} 秒")
    print(f"  - 总耗时：{total_time:.2f} 秒")

if __name__ == "__main__":
    main()