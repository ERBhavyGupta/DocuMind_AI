# 🧠 DocuMind AI: Human-in-the-Loop RAG Bot

DocuMind AI is an intelligent document assistant that combines the power of **Large Language Models (LLMs)** and **Vector Databases** to provide accurate, context-aware answers from uploaded documents. 

Unlike standard AI bots, DocuMind features a **Human-in-the-Loop (HITL)** escalation system. If the AI cannot find the answer in the provided documents, it seamlessly forwards the query to a human administrator, who can respond directly to the user via Telegram.

## 🚀 Features
- **Multi-Format Ingestion:** Support for `.pdf`, `.docx`, and `.txt` files.
- **Semantic Search:** Uses `sentence-transformers` and `ChromaDB` to find meaning-based matches rather than just keywords.
- **RAG Pipeline:** Implements Retrieval-Augmented Generation to eliminate AI hallucinations.
- **Telegram Interface:** Full integration for chatting and document uploading.
- **Admin Escalation:** Automatic routing of "I don't know" answers to a human manager.
- **Human-to-User Routing:** Admin can reply to escalated queries, and the bot routes the answer back to the original user.

## 🛠️ Tech Stack
- **Language:** Python 3.10+
- **AI Framework:** Pollinations AI (via OpenAI-compatible API)
- **Vector Database:** ChromaDB
- **Embeddings:** Sentence-Transformers (`all-MiniLM-L6-v2`)
- **Bot API:** `python-telegram-bot`
- **Document Processing:** `PyPDF2`, `python-docx`

## 📂 Project Structure
```text
├── bot.py            # Main entry point: Telegram bot logic & Admin routing
├── llm.py            # AI prompt engineering & API integration
├── retriever.py      # Logic for searching and storing vectors in ChromaDB
├── database.py       # ChromaDB client configuration
├── embeddings.py     # Text-to-Vector translation logic
├── ingest.py         # PDF/DOCX/TXT text extraction and chunking
├── .env              # Secret keys (API keys, Bot tokens)
└── requirements.txt  # List of dependencies
