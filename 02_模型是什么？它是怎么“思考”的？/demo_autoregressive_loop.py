"""
把 “预测下一个 Token” 循环起来

运行方式：
  export GOOGLE_API_KEY="your-api-key-here"
  python demo_autoregressive_loop.py
"""

import os
import sys
import unicodedata

from google import genai
from google.genai import types

# 最多执行 30 次
MAX_STEPS = 30

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

SYSTEM_CONTINUATION = (
    "你是一个纯文本续写引擎。用户给你一段未完成的文本，"
    "你的唯一任务是输出接下来最可能出现的那一点内容。"
    "可以是一个字、一个词、一个标点，也可以是一个空格或换行。"
    "不要解释，不要复述已有内容，不要加引号，不要加前后缀。"
    "如果你认为这段文本已经自然结束，输出空字符串即可。"
)

def one_step(client, text_so_far: str, temperature: float) -> tuple[str, str]:
    """
    让模型只吐 1 个 Token 的续写，返回 (新 token 文本, finish_reason)。
    """
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=text_so_far,
        config=types.GenerateContentConfig(
            system_instruction=SYSTEM_CONTINUATION,
            max_output_tokens=1,
            temperature=temperature,
            thinking_config=types.ThinkingConfig(thinking_budget=0),  # flash 默认开启思考，需关掉
        ),
    )
    new_token = response.text or ""
    finish = str(response.candidates[0].finish_reason) if response.candidates else ""
    return new_token, finish

def run_autoregressive(client, seed: str, temperature: float) -> None:
    print("=" * 100)
    print(f"  起始文本：{seed!r}   (temperature={temperature})")

    text = seed
    print(f"  {_pad('步骤', 8)} {_pad('本轮新 Token', 18)} {_pad('finish', 14)} 累计续写出来的文本")
    print(f"  {'─' * 100}")

    for step in range(1, MAX_STEPS + 1):
        new_tok, finish = one_step(client, text, temperature)
        text += new_tok

        display_tok = new_tok.replace("\n", "\\n") or "(空)"
        display_finish = finish.replace("FinishReason.", "")
        display_text = text.replace("\n", " ⏎ ")
        print(f"  {_pad(f'第 {step} 步', 8)} {_pad(display_tok[:16], 18)} {_pad(display_finish, 14)} {display_text}")

        # 模型主动结束
        if finish and finish.endswith("STOP") and not new_tok:
            print(f"\n  模型输出了 STOP（空续写），循环结束。")
            break

    print(f"\n  最终完整文本：\n    {text}\n")
    print("=" * 100)

def main():
    client = get_client()

    print("=" * 100)
    print("  用代码模拟自回归生成")
    print("=" * 100)

    run_autoregressive(client, "今天天气", temperature=0.5)
    run_autoregressive(client, "床前明月", temperature=0.0)

if __name__ == "__main__":
    main()
