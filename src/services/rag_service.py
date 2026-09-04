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
        self.model_name = available[0] if available else "models/text-embedding-004"

    def __call__(self, input: list[str]) -> Embeddings:
        response = self.client.models.embed_content(
            model=self.model_name,
            contents=input
        )
        return [e.values for e in response.embeddings]

class RAGService:
    def __init__(self, api_key: str):
        self.client = genai.Client(api_key=api_key)
        self.chroma_client = chromadb.Client()

        self.collection = self.chroma_client.get_or_create_collection(
            name="company_rules",
            embedding_function=GeminiEmbeddingFunction(self.client)
        )

        if self.collection.count() == 0:
            self._seed_database()

    def _seed_database(self):
        documents = [
            "Робочий день у компанії починається з 9:00 до 10:00 ранку.",
            "Заявка на відпустку подається суворо за 14 днів через Telegram-бота @HR_netpeak_bot.",
            "Річний бюджет на навчання кожного Junior-розробника становить $500.",
            "Оплата оренди житла компенсується тільки при релокації в інший офіс.",
        ]
        self.collection.add(
            documents=documents,
            ids=[f"doc_{i}" for i in range(len(documents))]
        )

    def answer_question(self, user_query: str) -> str:
        results = self.collection.query(query_texts=[user_query], n_results=2)
        
        if not results['documents'] or not results['documents'][0]:
            return "Інформація не знайдена."
            
        context = "\n".join(results['documents'][0])
        
        prompt = f"""
Ти — внутрішній корпоративний асистент. Відповідай на запитання користувача, використовуючи ТІЛЬКИ наданий контекст.
Якщо відповіді немає в контексті, скажи "Інформація не знайдена в базі знань".

Контекст:
{context}

Запитання: {user_query}
"""
        response = self.client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt
        )
        return response.text


if __name__ == "__main__":
    import os
    
    api_key = os.environ.get("GEMINI_API_KEY", "YOUR_API_KEY")
    rag = RAGService(api_key=api_key)
    
    query = "Як подати заявку на відпустку?"
    print(f"Запитання: {query}")
    print(f"Відповідь: {rag.answer_question(query)}")