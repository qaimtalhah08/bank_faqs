# 🧠 Enterprise RAG + Agentic AI System (Azure OpenAI + Cognitive Search)

A **production-style Retrieval-Augmented Generation (RAG) + Agentic AI system** built using Azure OpenAI, Azure Cognitive Search, and scalable backend architecture patterns.

This project demonstrates a **real-world AI engineering system design** including hybrid retrieval, caching, async processing, and cloud security practices.

---

## 🚀 Key Highlights

- 🧠 Azure OpenAI powered LLM reasoning
- 🔎 Azure Cognitive Search (Hybrid + Vector search indexing)
- 🤖 Agentic AI orchestration layer (multi-step reasoning)
- ⚡ Async + batching pipeline for performance optimization
- 🧩 Context-aware caching system (latency + cost reduction)
- 🐳 Fully Dockerized backend deployment
- 🔐 Enterprise-grade security design (RBAC + IAM + Key Vault)

---

## 🏗️ System Architecture

The system follows a modular, production-style architecture:

1. User query enters FastAPI backend
2. Agentic AI decides execution strategy
3. Query is embedded using Azure OpenAI
4. Azure Cognitive Search retrieves relevant chunks
5. Cache layer checks for previous responses
6. Re-ranking improves retrieval quality
7. LLM generates final grounded response
8. Response returned via API

---

