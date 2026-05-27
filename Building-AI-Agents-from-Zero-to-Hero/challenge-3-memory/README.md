# Challenge 3: Agent with Persistent Memory ⭐⭐

> Give your agent **persistent memory** using FAISS so it remembers facts across messages — even after you quit and restart.

---

## 🎯 Goal

Build an agent that stores and recalls user preferences using `mem0_memory` (FAISS-backed) — proving memory persists across program restarts.

---

## 🔧 Setup

### Install Dependencies (IMPORTANT — exact versions matter!)

```bash
pip install strands-agents strands-agents-bedrock "strands-agents-tools[mem0-memory]" faiss-cpu opensearch-py
```

> ⚠️ **Critical:** Use `"strands-agents-tools[mem0-memory]"` — this installs the correct `mem0ai` version (`>=0.1.99,<1.0.0`). If you install `mem0ai` separately with `pip install mem0ai`, you'll get version 1.x which is **NOT compatible** and will break everything.

### Enable These Models in Bedrock Console (us-east-1)

1. **Amazon Nova Pro** (`amazon.nova-pro-v1:0`) — main agent LLM
2. **Amazon Titan Text Embeddings V2** (`amazon.titan-embed-text-v2:0`) — for vector embeddings

Go to: [Bedrock Console](https://console.aws.amazon.com/bedrock/) → Model access → Enable both → Wait for "Access granted"

### AWS Credentials

```bash
aws configure
# Region: us-east-1
```

---

## ▶️ How to Run

```bash
# Step 1: Store memories
python starter.py

# Step 2: Verify persistence (separate program run)
python verify_memory.py
```

---

## 🧠 How It Works

```python
import os
os.environ["MEM0_LLM_MODEL"] = "amazon.nova-pro-v1:0"
os.environ["MEM0_EMBEDDER_MODEL"] = "amazon.titan-embed-text-v2:0"
os.environ["BYPASS_TOOL_CONSENT"] = "true"

from strands import Agent
from strands.models.bedrock import BedrockModel
from strands_tools import mem0_memory

model = BedrockModel(model_id="amazon.nova-pro-v1:0", region_name="us-east-1")
agent = Agent(model=model, tools=[mem0_memory])

# Store
agent.tool.mem0_memory(action="store", content="My name is DD", user_id="dd_user")

# Retrieve
agent.tool.mem0_memory(action="retrieve", query="name", user_id="dd_user")
```

| Env Variable | Purpose |
|---|---|
| `MEM0_LLM_MODEL` | LLM used internally by mem0 (default: Claude Haiku — change to Nova Pro if you don't have Haiku enabled) |
| `MEM0_EMBEDDER_MODEL` | Embedding model for vectors (Titan Embed V2) |
| `BYPASS_TOOL_CONSENT` | Skips confirmation prompts for store/delete |

---

## 📊 Two Types of Memory

| Type | Persists After Quit? |
|------|---------------------|
| Conversation History (default) | ❌ No |
| mem0_memory + FAISS (this challenge) | ✅ Yes |

---

## ⚠️ Common Errors & Fixes

### `ERROR: No matching distribution found for strands-tools`

```bash
# ❌ Wrong package name
pip install strands-tools

# ✅ Correct
pip install strands-agents-tools
```

### `ModuleNotFoundError: No module named 'mem0'`

```bash
pip install "strands-agents-tools[mem0-memory]"
```

### `ModuleNotFoundError: No module named 'opensearchpy'`

```bash
pip install opensearch-py
```

### `Unsupported vector store provider: faiss` / `Unsupported embedding provider: aws_bedrock`

Your `mem0ai` version is too new (1.x). Fix:

```bash
pip install "mem0ai>=0.1.99,<1.0.0"
```

### `Top-level entity parameters frozenset({'user_id'}) are not supported in get_all()`

Same issue — `mem0ai` version too new. Fix:

```bash
pip install "mem0ai>=0.1.99,<1.0.0"
```

### Authorization error when using mem0_memory

The `mem0_memory` tool internally uses its own LLM (default: Claude Haiku). If you only have Nova Pro enabled:

```python
os.environ["MEM0_LLM_MODEL"] = "amazon.nova-pro-v1:0"
```

---


## output :

![Screenshot 2026-05-21 193822.png](https://images.tomarkdown.dev/uploaded/r3qdsf6gont2v6gs.png)

![Screenshot 2026-05-21 194042.png](https://images.tomarkdown.dev/uploaded/1h614zcm7uctilse.png)



## 🏗️ Project Structure

```
challenge-3-memory/
├── starter.py         # Stores memories
├── verify_memory.py   # Verifies persistence after restart
├── debug_mem0.py      # Debug script to test mem0 directly
└── README.md
```

---

## 💡 Key Takeaways

- Package: `strands-agents-tools[mem0-memory]` (NOT `strands-tools`)
- `mem0ai` must be `<1.0.0` — newer versions break FAISS/aws_bedrock support
- Always set `MEM0_LLM_MODEL` env var if you don't have Claude Haiku enabled
- Use same `user_id` across scripts for persistence to work
- FAISS stores data locally on disk — no cloud DB needed

---

## 📎 References

- [Strands Agents Tools (PyPI)](https://pypi.org/project/strands-agents-tools/)
- [Memory Agent Example](https://strandsagents.com/docs/examples/python/memory_agent/)
- [mem0 FAISS Docs](https://docs.mem0.ai/components/vectordbs/dbs/faiss)
