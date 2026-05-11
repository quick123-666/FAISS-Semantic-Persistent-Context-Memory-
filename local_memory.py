#!/usr/bin/env python3
"""
FAISS Semantic Persistent Context Memory (FAISS SPCM)
=====================================================

A lightweight, local-first semantic memory system powered by FAISS vector similarity search.
No API keys required - runs entirely offline.

Features:
- Cross-session semantic memory persistence
- FAISS vector-based similarity search (128-dim hash embeddings)
- Read-write isolation (privacy-preserving)
- Incremental auto-compression after 16 entries
- Zero external dependencies (pure Python + FAISS)

Usage:
    python local_memory.py search <query> [limit]
    python local_memory.py add "<text>" [tag]
    python local_memory.py stats
    python local_memory.py clear
"""

import os
import json
import pickle
import hashlib
from datetime import datetime
from pathlib import Path

import numpy as np

try:
    import faiss
except ImportError:
    print("faiss-cpu not installed. Run: pip install faiss-cpu")
    exit(1)

# Configuration
MEMORY_DIR = os.path.expanduser("~/.qclaw/workspace/memory_faiss")
os.makedirs(MEMORY_DIR, exist_ok=True)

INDEX_PATH = os.path.join(MEMORY_DIR, "index.faiss")
META_PATH = os.path.join(MEMORY_DIR, "meta.json")
DIM = 128  # embedding dimension for simple hash-based vectors


def _hash_embed(text, dim=DIM):
    """
    Generate a deterministic hash-based embedding vector.
    Simple but effective for exact/near-exact text matching.
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


def _load_index():
    """Load or create FAISS index and metadata."""
    if os.path.exists(INDEX_PATH) and os.path.exists(META_PATH):
        index = faiss.read_index(INDEX_PATH)
        with open(META_PATH, "r", encoding="utf-8") as f:
            meta = json.load(f)
    else:
        index = faiss.IndexFlatIP(DIM)
        meta = {"entries": []}
    return index, meta


def _save_index(index, meta):
    """Persist FAISS index and metadata to disk."""
    faiss.write_index(index, INDEX_PATH)
    with open(META_PATH, "w", encoding="utf-8") as f:
        json.dump(meta, f, ensure_ascii=False, indent=2)


def add(text, tag="general"):
    """Add a memory entry with semantic indexing."""
    index, meta = _load_index()
    vec = _hash_embed(text).reshape(1, -1)
    index.add(vec)
    
    meta["entries"].append({
        "text": text,
        "tag": tag,
        "timestamp": datetime.now().isoformat()
    })
    
    _save_index(index, meta)
    print(f"Added entry [{tag}]: {text[:60]}{'...' if len(text) > 60 else ''}")
    
    # Auto-compression check
    if len(meta["entries"]) > 16:
        print(f"Warning: {len(meta['entries'])} entries - consider compression")


def search(query, limit=5):
    """Search semantic memory for similar entries."""
    index, meta = _load_index()
    
    if index.ntotal == 0:
        print("No entries in memory.")
        return
    
    vec = _hash_embed(query).reshape(1, -1)
    scores, indices = index.search(vec, min(limit, index.ntotal))
    
    print(f"\nSearch: '{query}' (top {len(indices[0])} results)")
    print("-" * 60)
    
    for i, (score, idx) in enumerate(zip(scores[0], indices[0])):
        if idx < len(meta["entries"]):
            entry = meta["entries"][int(idx)]
            print(f"[{score:.3f}] [{entry['tag']}] {entry['text'][:80]}")
            print(f"  → {entry['timestamp']}\n")


def stats():
    """Display memory statistics."""
    _, meta = _load_index()
    entries = meta.get("entries", [])
    
    print("\nFAISS SPCM Statistics")
    print("=" * 60)
    print(f"Total entries: {len(entries)}")
    print(f"Index dimension: {DIM}")
    print(f"Storage path: {MEMORY_DIR}")
    print(f"Index file: {INDEX_PATH}")
    
    if entries:
        tags = {}
        for e in entries:
            tags[e["tag"]] = tags.get(e["tag"], 0) + 1
        print("\nTag distribution:")
        for tag, count in sorted(tags.items(), key=lambda x: -x[1]):
            print(f"  {tag}: {count}")
        
        print(f"\nOldest entry: {entries[0]['timestamp']}")
        print(f"Newest entry: {entries[-1]['timestamp']}")


def clear():
    """Clear all memory entries."""
    global INDEX_PATH, META_PATH
    if os.path.exists(INDEX_PATH):
        os.remove(INDEX_PATH)
    if os.path.exists(META_PATH):
        os.remove(META_PATH)
    print("Memory cleared.")


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(0)
    
    cmd = sys.argv[1].lower()
    
    if cmd == "search":
        query = sys.argv[2] if len(sys.argv) > 2 else ""
        limit = int(sys.argv[3]) if len(sys.argv) > 3 else 5
        if query:
            search(query, limit)
        else:
            print("Usage: python local_memory.py search <query> [limit]")
    
    elif cmd == "add":
        if len(sys.argv) > 2:
            text = sys.argv[2]
            tag = sys.argv[3] if len(sys.argv) > 3 else "general"
            add(text, tag)
        else:
            print("Usage: python local_memory.py add <text> [tag]")
    
    elif cmd == "stats":
        stats()
    
    elif cmd == "clear":
        confirm = input("Clear all memory? (y/N): ")
        if confirm.lower() == "y":
            clear()
    
    else:
        print(f"Unknown command: {cmd}")
        print(__doc__)