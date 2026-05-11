# FAISS Semantic Persistent Context Memory (FAISS SPCM)

**FAISS 语义持久化上下文记忆系统**

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/Python-3.8%2B-blue.svg)](https://www.python.org/)
[![FAISS](https://img.shields.io/badge/FAISS-Enabled-green.svg)](https://github.com/facebookresearch/faiss)
[![No API Key](https://img.shields.io/badge/No%20API%20Key-Required-red.svg)](https://github.com/quick123-666/FAISS-Semantic-Persistent-Context-Memory)

---

## Overview / 概述

FAISS SPCM is a lightweight, local-first semantic memory system powered by **FAISS (Facebook AI Similarity Search)** vector search engine. It enables AI assistants to maintain persistent context across conversations without requiring external API services.

FAISS SPCM 是一个轻量级、本地优先的语义记忆系统，基于 **FAISS (Facebook AI 相似度搜索)** 向量搜索引擎。无需外部 API 服务，即可让 AI 助手在对话间保持持续的上下文记忆。

### Key Features / 核心特性

| Feature | 特性 | Description | 描述 |
|---------|------|-------------|------|
| 🔍 **Semantic Search** | 语义搜索 | Vector-based similarity matching | 基于向量的相似度匹配 |
| 💾 **Persistent Memory** | 持久化记忆 | Cross-session context survival | 跨会话上下文存活 |
| 🔒 **Local-First** | 本地优先 | Zero API dependencies, runs offline | 无 API 依赖，离线运行 |
| 🛡️ **Privacy-Preserving** | 隐私保护 | Read-write isolation architecture | 读写隔离架构 |
| 📦 **Auto-Compression** | 自动压缩 | Memory management after 16+ entries | 超过 16 条自动管理 |
| ⚡ **Fast Computation** | 快速计算 | Hash-based embedding (no GPU needed) | 基于哈希的嵌入（无需 GPU） |

---

## Architecture / 架构

```
┌─────────────────────────────────────────────────────────────┐
│                    FAISS SPCM System                        │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│   User Input ──► Hash Embedding ──► FAISS Index             │
│                      │                    │                  │
│                      ▼                    ▼                  │
│                 128-dim Vector    Vector Similarity Search   │
│                      │                    │                  │
│                      ▼                    ▼                  │
│                 Metadata (JSON) ◄──── Results              │
│                                                             │
│   Storage: ~/.qclaw/workspace/memory_faiss/                │
│   ├── index.faiss    # FAISS vector index                  │
│   └── meta.json      # Entry metadata                       │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

---

## Installation / 安装

### Prerequisites / 前置要求

```bash
pip install faiss-cpu
```

### Quick Start / 快速开始

```bash
# Clone the repository / 克隆仓库
git clone https://github.com/quick123-666/FAISS-Semantic-Persistent-Context-Memory.git
cd FAISS-Semantic-Persistent-Context-Memory

# Install dependency / 安装依赖
pip install faiss-cpu

# Run / 运行
python local_memory.py --help
```

---

## Usage / 使用

### Search Memory / 搜索记忆

```bash
python local_memory.py search "project deadline" 5
```

**Output / 输出:**
```
Search: 'project deadline' (top 5 results)
------------------------------------------------------------
[0.847] [work] Remember to submit project report by Friday
  → 2026-05-11T10:30:00

[0.723] [personal] Deadline for tax filing is April 15
  → 2026-05-10T14:22:00
```

### Add Memory / 添加记忆

```bash
python local_memory.py add "User prefers JSON output format" preference
```

**Output / 输出:**
```
Added entry [preference]: User prefers JSON output format
```

### View Statistics / 查看统计

```bash
python local_memory.py stats
```

**Output / 输出:**
```
FAISS SPCM Statistics
============================================================
Total entries: 42
Index dimension: 128
Storage path: ~/.qclaw/workspace/memory_faiss
Index file: /home/user/.qclaw/workspace/memory_faiss/index.faiss

Tag distribution:
  general: 25
  preference: 10
  task: 7

Oldest entry: 2026-05-01T08:00:00
Newest entry: 2026-05-11T12:45:00
```

---

## API Reference / API 参考

### Core Functions / 核心函数

| Function | 函数 | Parameters | 参数 | Description | 描述 |
|----------|------|------------|------|-------------|------|
| `add(text, tag)` | 添加 | `text: str`, `tag: str` | Add memory entry | 添加记忆条目 |
| `search(query, limit)` | 搜索 | `query: str`, `limit: int` | Search similar entries | 搜索相似条目 |
| `stats()` | 统计 | None | Display memory stats | 显示记忆统计 |
| `clear()` | 清除 | None (confirmation required) | Clear all memory | 清除所有记忆 |

### Configuration / 配置

| Variable | 变量 | Default | 默认值 | Description | 描述 |
|----------|------|---------|--------|-------------|------|
| `MEMORY_DIR` | 记忆目录 | `~/.qclaw/workspace/memory_faiss` | Storage location | 存储位置 |
| `DIM` | 维度 | `128` | Vector dimension | 向量维度 |

---

## Technical Details / 技术细节

### Hash-Based Embedding / 基于哈希的嵌入

Unlike API-based embeddings (OpenAI, Anthropic), this system uses deterministic hash-based vectorization:

1. Text is split into 8-character chunks / 文本被分割成 8 字符块
2. Each chunk is MD5-hashed / 每个块进行 MD5 哈希
3. Hash value determines vector index / 哈希值决定向量索引
4. Chunk frequency determines vector weight / 块频率决定向量权重
5. Vector is L2-normalized / 向量进行 L2 归一化

**Advantages / 优势:**
- ✅ No API key required / 无需 API key
- ✅ Deterministic (same input = same output) / 确定性（相同输入 = 相同输出）
- ✅ Fast computation / 快速计算
- ✅ Privacy-preserving / 隐私保护

**Trade-offs / 权衡:**
- ⚠️ No semantic understanding (keyword-based) / 无语义理解（基于关键词）
- ⚠️ Fixed 128-dimension resolution / 固定 128 维分辨率

### FAISS Index / FAISS 索引

- **Index Type / 索引类型**: `IndexFlatIP` (Inner Product, Cosine Similarity)
- **Search / 搜索**: Top-K nearest neighbors
- **Scaling / 扩展**: O(n) for n entries (acceptable for <100k entries)

---

## Integration / 集成

### OpenClaw Integration / OpenClaw 集成

```python
# In OpenClaw session start / 在 OpenClaw 会话开始时
from local_memory import search
context = search(user_query, limit=3)

# Use context in response generation / 在响应生成中使用上下文
```

**OpenClaw SOUL.md configuration / OpenClaw SOUL.md 配置:**

```markdown
### FAISS Semantic Persistent Context Memory (FAISS SPCM)
- **工具：** `python "{workspace}/tools/local_memory.py"`
- **会话开始：** 搜索记忆获取相关 context
- **任务中：** 用 `add` 存储关键发现、决策、用户偏好
```

---

## Comparison / 对比

| Feature | FAISS SPCM | OpenAI Embeddings | Pinecone |
|---------|-------------|-------------------|----------|
| API Key Required | ❌ No | ✅ Yes | ✅ Yes |
| Cloud Service | ❌ No | ✅ Yes | ✅ Yes |
| Cross-Session | ✅ Yes | ✅ Yes | ✅ Yes |
| Privacy | ✅ Full | ❌ Limited | ❌ Limited |
| Cost | ✅ Free | 💰 Paid | 💰 Paid |
| Offline Mode | ✅ Yes | ❌ No | ❌ No |

---

## License / 许可证

MIT License - See [LICENSE](LICENSE) for details.

---

## Contributing / 贡献

Contributions welcome! Please:

1. Fork the repository
2. Create a feature branch
3. Add tests for new features
4. Submit a pull request

---

## References / 参考

- [FAISS: A Library for Efficient Similarity Search](https://github.com/facebookresearch/faiss)
- [Facebook AI Similarity Search](https://faiss.ai/)
- [OpenClaw Agent Framework](https://docs.openclaw.ai/)

---

**Star ⭐ if this project helped you! / 如果这个项目对你有帮助，请加星 ⭐**