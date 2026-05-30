"""
模型输出的其实是一个概率分布

运行方式：
  export GOOGLE_API_KEY="your-api-key-here"
  python demo_next_token_prediction.py
"""

import os
import sys
import unicodedata
from collections import Counter

from google import genai
from google.genai import types

SAMPLES_PER_CASE = 8  # 每个前缀采样多少次

def _disp_width(s: str) -> int:
    """终端显示宽度：CJK 字符算 2 列，其它算 1 列。"""
    return sum(2 if unicodedata.east_asian_width(c) in ("F", "W") else 1 for c in s)

def _pad(s: str, width: int) -> str:
    """按显示宽度右侧补空格。"""
    return s + " " * max(0, width - _disp_width(s))

def get_client() -> genai.Client:
    api_key = os.environ.get("GOOGLE_API_KEY")
    if not api_key:
        print("❌ 请先设置环境变量 GOOGLE_API_KEY")
        print('   export GOOGLE_API_KEY="your-api-key-here"')
        sys.exit(1)
    return genai.Client(api_key=api_key)

def sample_next_token(client, prompt: str, n: int) -> list[str]:
    """
    给定前缀，让模型按真实概率分布采样 n 次，每次只生成 1 个 Token。
    返回这 n 次拿到的 Token 文本列表。
    """
    tokens: list[str] = []
    print(f"  采样中", end="", flush=True)
    for i in range(n):
        r = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt,
            config=types.GenerateContentConfig(
                max_output_tokens=1,                                        # 只输出一个 token
                temperature=1.0,                                            # 按真实概率分布采样
                top_p=1.0,                                                  # 不裁切候选范围，全部保留
                thinking_config=types.ThinkingConfig(thinking_budget=0),    # 关闭模型先推理再回答
            ),
        )
        tokens.append((r.text or "").strip())
        print(".", end="", flush=True)
    print()
    return tokens

def summarize(tokens: list[str], prompt: str) -> None:
    """把采样结果按频率排序展示——这就是反推出的概率分布。"""
    print(f"  前缀：{prompt!r}")
    print(f"  采样次数：{len(tokens)}")

    counter = Counter(tokens)
    total = sum(counter.values())

    print(f"\n  出现过的候选 Token 概率分布：")
    print(f"  {'─' * 70}")
    print(f"  {_pad('排名', 6)} {_pad('候选 Token', 24)} {_pad('出现次数', 10)} 估计概率")
    print(f"  {'─' * 70}")
    for i, (tok, cnt) in enumerate(counter.most_common(), 1):
        display = repr(tok) if tok else "''"
        prob = cnt / total
        bar = "█" * max(1, round(prob * 20))
        print(f"  {_pad(str(i), 6)} {_pad(display, 24)} {_pad(str(cnt), 10)} {prob * 100:5.1f}% {bar}")

def main():
    client = get_client()

    print("\n" + "=" * 72)
    print("模型的『预测』是一个概率分布")
    print("=" * 72)

    cases = [
        ("案例 1：事实性前缀（分布集中）", "The capital of France is"),
        ("案例 2：开放续写（分布发散）", "今天天气"),
        ("案例 3：固定搭配", "Roses are red, violets are"),
    ]

    for label, prompt in cases:
        print("=" * 72)
        print(f"  🎲 {label}")
        tokens = sample_next_token(client, prompt, SAMPLES_PER_CASE)
        summarize(tokens, prompt)
        print("=" * 72)
        print()

if __name__ == "__main__":
    main()
