# Enterprise Knowledge Assistant Bot 

An enterprise-grade Telegram bot featuring a complete RAG (Retrieval-Augmented Generation) pipeline. It allows users to upload documents (PDF/TXT) and query their contents using Gemini AI, featuring persistent vector search and asynchronous conversational history.

---

##  Core Features

* **Dynamic RAG Pipeline:** Upload PDF or TXT files directly in chat for automated text extraction (`pypdf`), chunking, vectorization, and context-aware responses.
* **Conversational Memory:** Asynchronous SQLite storage retains multi-turn chat history, allowing the LLM to process follow-up questions seamlessly.
* **Modern AI Capabilities:** Built on the `google-genai` SDK using Gemini Flash for rapid response times and structured context handling.
* **Enterprise Architecture:** Clean, modular structure using `aiogram 3.x` routers, strict separation of business logic, and containerized deployment with Docker.

---

##  Tech Stack

| Component | Technology |
| :--- | :--- |
| **Language** | Python 3.12 |
| **Bot Framework** | `aiogram` 3.x (Async Telegram Bot API) |
| **LLM & Vector Engine** | `google-genai` (Gemini Flash), `chromadb` (Persistent Client) |
| **Relational Database** | `SQLAlchemy` 2.0 (Async / `aiosqlite`) |
| **Document Processing** | `pypdf` |
| **Infrastructure** | Docker, Docker Compose |

---

##  Project Structure

```text
.
├── database/            # SQLAlchemy async engine, models, and CRUD operations
├── handlers/            # Modular aiogram routers (commands, documents, chat)
├── services/            # Core business logic (RAG pipeline, PDF parsing, AI SDK)
├── data/                # Volume directory for persistent SQLite and ChromaDB data
├── temp/                # Temporary storage for processing files
├── .env.example         # Environment configuration template
├── docker-compose.yml   # Deployment orchestration
├── Dockerfile           # Production container definition
├── main.py              # Application entry point
└── requirements.txt     # Python dependencies
```

---

##  Quick Start (Docker — Recommended)

1. **Clone the repository:**
   ```bash
   git clone https://github.com/Vlad-Skubskiy/netpeak-knowledge-assistant.git
   cd netpeak-knowledge-assistant
   ```

2. **Configure environment variables:**
   ```bash
   cp .env.example .env
   ```
   *Open `.env` and fill in your credentials (`TELEGRAM_BOT_TOKEN`, `GEMINI_API_KEY`).*

3. **Build and run containers:**
   ```bash
   docker compose up --build -d
   ```

4. **Check container logs:**
   ```bash
   docker compose logs -f
   ```

---

##  Local Development (Without Docker)

1. **Clone the repository:**
   ```bash
   git clone https://github.com/Vlad-Skubskiy/netpeak-knowledge-assistant.git
   cd netpeak-knowledge-assistant
   ```

2. **Create and activate a virtual environment:**
   ```bash
   # Windows
   python -m venv venv
   .\venv\Scripts\activate

   # Linux/macOS
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment and start:**
   ```bash
   cp .env.example .env
   # Add your API keys to .env
   python main.py
   ```

---

##  Environment Variables

| Variable | Description | Required |
| :--- | :--- | :---: |
| `TELEGRAM_BOT_TOKEN` | Bot API token obtained from @BotFather | Yes |
| `GEMINI_API_KEY` | API key generated in Google AI Studio | Yes |
| `DATABASE_URL` | Async database URI (defaults to `sqlite+aiosqlite:///data/bot_history.db`) | No |
