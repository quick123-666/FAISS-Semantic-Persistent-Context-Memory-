# FAISS Semantic Persistent Context Memory (FAISS SPCM)

**A lightweight, local-first semantic memory system powered by FAISS vector similarity search.**

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/Python-3.8%2B-blue.svg)](https://www.python.org/)
[![FAISS](https://img.shields.io/badge/FAISS-Enabled-green.svg)](https://github.com/facebookresearch/faiss)

---

## Overview

FAISS SPCM is a cross-session semantic memory system that enables AI assistants to maintain persistent context across conversations. Built on Facebook AI's FAISS vector similarity search, it provides:

- **Semantic Search**: Find similar memories using vector embeddings
- **Cross-Session Persistence**: Memories survive session boundaries
- **Local-First**: Zero API dependencies, runs entirely offline
- **Privacy-Preserving**: Read-write isolation between sessions
- **Auto-Compression**: Automatically manages memory footprint

---

## Architecture

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
└─────────────────────────────────────────────────────────────┘

Storage: ~/.qclaw/workspace/memory_faiss/
├── index.faiss    # FAISS vector index
└── meta.json      # Entry metadata
```

---

## Installation

### Prerequisites

```bash
pip install faiss-cpu
```

### Clone & Use

```bash
git clone https://github.com/quick123-666/FAISS-Semantic-Persistent-Context-Memory.git
cd FAISS-Semantic-Persistent-Context-Memory

# Make executable
chmod +x local_memory.py

# Run commands
python local_memory.py --help
```

---

## Usage

### Search Memory

```bash
python local_memory.py search "project deadline" 5
```

**Output:**
```
Search: 'project deadline' (top 5 results)
------------------------------------------------------------
[0.847] [work] Remember to submit project report by Friday
  → 2026-05-11T10:30:00

[0.723] [personal] Deadline for tax filing is April 15
  → 2026-05-10T14:22:00
```

### Add Memory

```bash
python local_memory.py add "User prefers JSON output format" preference
```

**Output:**
```
Added entry [preference]: User prefers JSON output format
```

### View Statistics

```bash
python local_memory.py stats
```

**Output:**
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

## Configuration

| Variable | Default | Description |
|----------|---------|-------------|
| `MEMORY_DIR` | `~/.qclaw/workspace/memory_faiss` | Storage directory |
| `DIM` | `128` | Vector embedding dimension |

Modify in `local_memory.py`:

```python
MEMORY_DIR = "/custom/path"
DIM = 256  # Higher = more precision, more memory
```

---

## Technical Details

### Hash-Based Embedding

Unlike API-based embeddings (OpenAI, Anthropic), this system uses deterministic hash-based vectorization:

1. Text is split into 8-character chunks
2. Each chunk is MD5-hashed
3. Hash value determines vector index
4. Chunk frequency determines vector weight
5. Vector is L2-normalized

**Advantages:**
- No API key required
- Deterministic (same input = same output)
- Fast computation
- Privacy-preserving

**Trade-offs:**
- No semantic understanding (keyword-based similarity)
- Fixed 128-dimension resolution

### FAISS Index

- **Index Type**: `IndexFlatIP` (Inner Product, Cosine Similarity)
- **Search**: Top-K nearest neighbors
- **Scaling**: O(n) for n entries (acceptable for <100k entries)

---

## Integration with OpenClaw

FAISS SPCM integrates with OpenClaw's agent workflow:

```python
# In OpenClaw session start
from local_memory import search
context = search(user_query, limit=3)

# Use context in response generation
```

**OpenClaw SOUL.md configuration:**
```markdown
### FAISS Semantic Persistent Context Memory (FAISS SPCM)
- **工具：** `python "{workspace}/tools/local_memory.py"`
- **会话开始：** 搜索记忆获取相关 context
- **任务中：** 用 `add` 存储关键发现、决策、用户偏好
```

---

## License

MIT License - See [LICENSE](LICENSE) for details.

---

## Contributing

Contributions welcome! Please:

1. Fork the repository
2. Create a feature branch
3. Add tests for new features
4. Submit a pull request

---

## References

- [FAISS: A Library for Efficient Similarity Search](https://github.com/facebookresearch/faiss)
- [Facebook AI Similarity Search](https://faiss.ai/)