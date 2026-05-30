# 《模型是什么？它是怎么 “思考” 的？》 Demo 运行指南

## Demo 一览

| 文件 | 演示内容 | 对应文章章节 |
|---|---|---|
| `demo_next_token_prediction.py` | 同一前缀重复采样，看到 “下一个 Token” 其实是一个概率分布 | 二、大模型是怎么 “想” 出回答的？ |
| `demo_autoregressive_loop.py` | 把 “预测下一个 Token → 拼接 → 再预测” 的自回归循环搬到代码里，每次只让模型吐 1 个 Token | 二、大模型是怎么 “想” 出回答的？ |

## 环境要求

- 建议 Python >= 3.10 （ 3.9 也能跑，但会有警告提示）
- 需要一个 Google Gemini API Key ，可以到 [Google AI Studio](https://aistudio.google.com/apikey) 免费申请。免费的 Key 会有使用频率限制，但是不妨碍学习。

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
→ 依赖没安装，参考 “2、安装依赖” 执行 `pip install -r requirements.txt` 。

**Q: 报错 `❌ 请先设置环境变量 GOOGLE_API_KEY`**
→ 没设置 API Key。在终端先输入 `export GOOGLE_API_KEY="你申请到的 Gemini API Key"` 之后再运行。注意 `export` 只在当前 shell 有效，新开终端要重新设。

**Q: Gemini API Key 是免费的吗？**
→ 是的，但是每天有请求次数的限制。如果受到请求频率限制，影响到你学习的话，可以考虑开通付费 GOOGLE Gemini Key（充值最低限额 80 RMB 即可），整个分享的 Token 消耗并不大。