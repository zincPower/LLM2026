# Python Demo 运行指南

## 环境要求

- 建议 Python >= 3.10 （ 3.9 也能跑，但会有警告提示）
- 需要一个 Google Gemini API Key ，可以到 [Google AI Studio](https://aistudio.google.com/apikey) 免费申请，可以免费使用但会有使用限制

## 如何运行

### 1、进入目录

```bash
cd `你要运行的 demo 目录`
```

### 2、安装依赖

```bash
pip install -r requirements.txt
```

> 建议做环境隔离，避免污染你的 python 环境

### 3、设置 API Key 并运行

```bash
export GOOGLE_API_KEY="your-api-key-here"

python xxx.py
```

## 常见问题

**Q: 报错 `ModuleNotFoundError: No module named 'google.genai'`**
→ 没装依赖，回到第 2 步执行 `pip install -r requirements.txt`。

**Q: 报错 `❌ 请先设置环境变量 GOOGLE_API_KEY`**
→ 没设 API Key。`export GOOGLE_API_KEY="..."` 之后再运行。注意 `export` 只在当前 shell 有效，新开终端要重新设。

**Q: Gemini API Key 是免费的吗？**
→ 是的，但是每天有请求次数的限制。如果免费的限制影响到你学习的话，建议付费，整个分享的 Token 消耗并不大，所以应该在您的承受范围内。