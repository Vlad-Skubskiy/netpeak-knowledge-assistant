import chromadb
from chromadb import EmbeddingFunction, Embeddings
from google import genai

class GeminiEmbeddingFunction(EmbeddingFunction):
    def __init__(self, client_instance: genai.Client):
        self.client = client_instance
        available = [
            m.name for m in self.client.models.list()
            if "embedContent" in getattr(m, "supported_actions", [])
        ]
        self.model_name = available[0] if available else "models/gemini-embedding-001"

    def __call__(self, input: list[str]) -> Embeddings:
        response = self.client.models.embed_content(
            model=self.model_name,
            contents=input
        )
        return [e.values for e in response.embeddings]

class RAGService:
    def __init__(self, api_key: str):
        self.client = genai.Client(api_key=api_key)
        self.chroma_client = chromadb.PersistentClient(path="./data/chroma_db")
        self.collection = self.chroma_client.get_or_create_collection(
            name="company_rules",
            embedding_function=GeminiEmbeddingFunction(self.client)
        )

    def _chunk_text(self, text: str, chunk_size: int = 800, overlap: int = 100) -> list[str]:
        chunks = []
        start = 0
        while start < len(text):
            end = start + chunk_size
            chunks.append(text[start:end])
            start += chunk_size - overlap
        return [c.strip() for c in chunks if c.strip()]

    def add_document(self, text: str, source_name: str) -> int:
        chunks = self._chunk_text(text)
        if not chunks:
            return 0

        ids = [f"{source_name}_chunk_{i}" for i in range(len(chunks))]
        metadatas = [{"source": source_name} for _ in chunks]

        self.collection.add(
            documents=chunks,
            ids=ids,
            metadatas=metadatas
        )
        return len(chunks)

    def answer_question(self, user_query: str, history: list[dict] = None) -> str:
        results = self.collection.query(query_texts=[user_query], n_results=3)
        
        context = ""
        if results['documents'] and results['documents'][0]:
            context = "\n---\n".join(results['documents'][0])
        else:
            context = "Інформація не знайдена в базі знань."

        formatted_history = ""
        if history:
            for msg in history:
                role_label = "Користувач" if msg["role"] == "user" else "Асистент"
                formatted_history += f"{role_label}: {msg['content']}\n"

        prompt = f"""
Ти — внутрішній корпоративний асистент. Відповідай на запитання користувача, використовуючи контекст із бази знань та історію діалогу.
Якщо відповіді немає ні в контексті, ні в історії, скажи "Інформація не знайдена в базі знань".

Історія попереднього діалогу:
{formatted_history if formatted_history else "Історія порожня."}

Контекст із бази знань (документів):
{context}

Поточне запитання користувача: {user_query}
"""
        response = self.client.models.generate_content(
            model="gemini-3.6-flash",
            contents=prompt
        )
        return response.text