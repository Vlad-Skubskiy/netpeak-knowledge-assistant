# Enterprise Knowledge Assistant Bot 🤖

An enterprise-ready Telegram bot featuring a complete RAG (Retrieval-Augmented Generation) pipeline. It allows users to upload documents (PDF/TXT) and chat with their data using Gemini AI, complete with conversational memory and vector search.

## 🌟 Core Features
* **Dynamic RAG Pipeline:** Upload PDFs or TXT files directly in the chat for instant chunking, vectorization, and querying.
* **Conversational Context:** Asynchronous SQLite storage tracks user history, allowing the LLM to remember previous messages in the dialogue.
* **Modern AI Integration:** Powered by the new `google-genai` SDK (Gemini Flash) for fast, context-aware responses.
* **Production-Ready:** Built with a modular architecture (`aiogram 3.x` routers), strict separation of concerns, and fully containerized for one-click deployment.

## 🛠 Tech Stack
* **Language:** Python 3.12
* **Bot Framework:** `aiogram` 3.x
* **AI & Vector Search:** `google-genai`, `chromadb` (PersistentClient)
* **Relational Database:** `SQLAlchemy` 2.0 (async / `aiosqlite`)
* **Infrastructure:** Docker, Docker Compose

## 🚀 Quick Start (Docker)

1. **Clone the repository:**
   ```bash
   git clone [https://github.com/YourUsername/ai-assistant-bot.git](https://github.com/YourUsername/ai-assistant-bot.git)
   cd ai-assistant-bot