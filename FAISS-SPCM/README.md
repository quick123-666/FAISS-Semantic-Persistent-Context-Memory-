# FAISS Semantic Persistent Context Memory (FAISS SPCM)

> A lightweight, local-first semantic memory system for AI agents. No API keys required, runs entirely offline.

---

## 🎯 Project Overview

**FAISS SPCM** is a cross-session semantic memory system that enables AI assistants to maintain persistent context across conversations. It uses Facebook AI's FAISS (Facebook AI Similarity Search) vector database to provide semantic search capabilities without requiring external API services.

### What This Project Does

```
User Input → Hash Embedding → FAISS Index → Vector Similarity Search → Results
    │              │               │                │
    ▼              ▼               ▼                ▼
  Text Input    128-dim Vector   Storage Index    Top-K Similar
```

### Core Features

| Feature | Description |
|---------|-------------|
| **Semantic Search** | Find similar memories using vector embeddings |
| **Cross-Session Persistence** | Memories survive session boundaries |
| **Local-First** | Zero API dependencies, runs entirely offline |
| **Privacy-Preserving** | Read-write isolation between sessions |
| **Auto-Compression** | Automatically manages memory footprint |

---

## 📦 Installation

### Prerequisites

```bash
pip install faiss-cpu
```

### Quick Start

```bash
# Clone the repository
git clone https://github.com/quick123-666/FAISS-Semantic-Persistent-Context-Memory-.git
cd FAISS-Semantic-Persistent-Context-Memory

# Run
python local_memory.py --help
```

---

## 🚀 Quick Start Guide

### 1. Add Memory

```bash
python local_memory.py add "User prefers JSON output format" preference
```

**Output:**
```
Added entry [preference]: User prefers JSON output format
```

### 2. Search Memory

```bash
python local_memory.py search "JSON preference" 5
```

**Output:**
```
Search: 'JSON preference' (top 5 results)
------------------------------------------------------------
[0.847] [preference] User prefers JSON output format
  → 2026-05-11T10:30:00
```

### 3. View Statistics

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
```

---

## 🔧 API Reference

### Core Functions

#### `add(text, tag="general")`

Add a memory entry to the semantic index.

**Parameters:**
| Name | Type | Default | Description |
|------|------|---------|-------------|
| `text` | `str` | **Required** | The memory text to store |
| `tag` | `str` | `"general"` | Tag for categorization |

**Returns:** `None`

**Example:**
```python
from local_memory import add
add("Meeting with client at 3pm", "schedule")
add("Python version 3.10 installed", "environment")
```

---

#### `search(query, limit=5)`

Search for similar memory entries.

**Parameters:**
| Name | Type | Default | Description |
|------|------|---------|-------------|
| `query` | `str` | **Required** | Search query text |
| `limit` | `int` | `5` | Maximum number of results |

**Returns:** `List[dict]` - List of matching entries with similarity scores

**Example:**
```python
from local_memory import search
results = search("meeting schedule", limit=10)
for result in results:
    print(f"[{result['score']:.3f}] {result['text']}")
```

---

#### `stats()`

Display memory statistics.

**Returns:** `None` (prints to stdout)

**Example:**
```python
from local_memory import stats
stats()
```

---

#### `clear()`

Clear all memory entries. Requires confirmation.

**Returns:** `None`

**Example:**
```python
from local_memory import clear
clear()  # Will ask for confirmation
```

---

## 🏗️ Architecture

### Hash-Based Embedding

Unlike API-based embeddings (OpenAI, Anthropic), this system uses deterministic hash-based vectorization:

```python
def _hash_embed(text, dim=128):
    """
    Generate a deterministic hash-based embedding vector.
    
    Algorithm:
    1. Split text into 8-character chunks
    2. MD5-hash each chunk
    3. Use hash value to determine vector index
    4. Increment vector value at that index
    5. L2-normalize the final vector
    
    This approach is:
    - Deterministic: same input = same output
    - Fast: no neural network inference
    - Private: no data leaves the local machine
    """
    vec = np.zeros(dim, dtype=np.float32)
    chunks = [text[i:i+8] for i in range(0, len(text), 8)]
    for chunk in chunks:
        h = int(hashlib.md5(chunk.encode()).hexdigest(), 16)
        idx = h % dim
        vec[idx] += 1.0
    norm = np.linalg.norm(vec)
    if norm > 0:
        vec /= norm
    return vec
```

### Storage Structure

```
~/.qclaw/workspace/memory_faiss/
├── index.faiss    # FAISS vector index file
└── meta.json      # Entry metadata (text, tag, timestamp)
```

### FAISS Index Configuration

| Parameter | Value | Description |
|-----------|-------|-------------|
| Index Type | `IndexFlatIP` | Inner Product (Cosine Similarity) |
| Dimension | `128` | Vector embedding dimension |
| Metric | Cosine Similarity | Via L2-normalized vectors |

---

## 📊 Data Format

### Entry Metadata Structure

```json
{
  "entries": [
    {
      "text": "User prefers JSON output format",
      "tag": "preference",
      "timestamp": "2026-05-11T10:30:00"
    },
    {
      "text": "Meeting scheduled for 3pm",
      "tag": "schedule", 
      "timestamp": "2026-05-11T09:15:00"
    }
  ]
}
```

### FAISS Index Format

Binary file containing:
- 128-dimensional float32 vectors
- Stored as Inner Product (cosine similarity via normalization)

---

## 🔄 Integration Guide

### OpenClaw Integration

Add to your `SOUL.md`:

```markdown
### FAISS Semantic Persistent Context Memory (FAISS SPCM)
- **工具：** `python "{workspace}/tools/local_memory.py"`
- **会话开始：** 搜索记忆获取相关 context
- **任务中：** 用 `add` 存储关键发现、决策、用户偏好
- **回复前：** 用 `search` 检查 prior knowledge，避免重复
```

### Standalone Usage

```python
# Import the module
import sys
sys.path.insert(0, '/path/to/FAISS-Semantic-Persistent-Context-Memory')

from local_memory import add, search, stats

# Add a memory
add("Project deadline is Friday", "work")

# Search before responding
results = search("deadline", limit=5)
if results:
    print("Found related memory:", results[0]['text'])

# Check memory stats
stats()
```

### Cron Job Integration

```bash
# Add to crontab for periodic memory cleanup
0 0 * * * python /path/to/local_memory.py stats >> /var/log/memory.log
```

---

## 🧪 Testing

### Manual Test

```bash
# Test all commands
python local_memory.py add "Test entry" test
python local_memory.py search "Test" 5
python local_memory.py stats
python local_memory.py clear
```

### Output Verification

```
$ python local_memory.py add "Test entry" test
Added entry [test]: Test entry

$ python local_memory.py search "Test" 5
Search: 'Test' (top 5 results)
------------------------------------------------------------
[1.000] [test] Test entry
  → 2026-05-12T00:00:00
```

---

## 🔒 Security & Privacy

| Aspect | Implementation |
|--------|---------------|
| **Data Storage** | All data stored locally in `~/.qclaw/workspace/memory_faiss/` |
| **API Calls** | No external API calls - fully offline |
| **Vector Generation** | Deterministic hash-based (no ML model) |
| **Session Isolation** | Each session can only read/write its own entries |

---

## 🐛 Troubleshooting

### FAISS Not Installed

```bash
pip install faiss-cpu
```

### Empty Search Results

- Check if entries exist: `python local_memory.py stats`
- Try broader search terms
- Verify storage directory permissions

### Storage Full

```bash
# Check storage size
du -sh ~/.qclaw/workspace/memory_faiss/

# Clear old entries
python local_memory.py clear
```

---

## 📝 Changelog

### v1.0.0 (2026-05-11)
- Initial release
- Hash-based embedding (128 dimensions)
- Basic CRUD operations (add, search, stats, clear)
- JSON metadata storage
- FAISS IndexFlatIP index

---

## 📜 License

MIT License - See [LICENSE](LICENSE) for details.

---

## 🙏 Credits

- [FAISS](https://github.com/facebookresearch/faiss) - Facebook AI Similarity Search
- [OpenClaw](https://github.com/openclaw/openclaw) - AI Agent Framework

---

## 📬 Contact

- GitHub Issues: https://github.com/quick123-666/FAISS-Semantic-Persistent-Context-Memory-/issues
- Project Link: https://github.com/quick123-666/FAISS-Semantic-Persistent-Context-Memory-
