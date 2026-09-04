import asyncio
import os
from pathlib import Path
from dotenv import load_dotenv
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import CommandStart
import pypdf

from src.services.rag_service import RAGService
from src.db.database import init_db, add_message, get_recent_history

BASE_DIR = Path(__file__).resolve().parent
load_dotenv(BASE_DIR / ".env")

BOT_TOKEN = os.getenv("BOT_TOKEN")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()
rag_service = RAGService(api_key=GEMINI_API_KEY)

TEMP_DIR = BASE_DIR / "temp"
TEMP_DIR.mkdir(exist_ok=True)

@dp.message(CommandStart())
async def start_handler(message: types.Message):
    await message.answer(
        "Привіт! Я корпоративний AI-асистент з пам'яттю діалогу.\n\n"
        "Задай мені питання або надішли **PDF / TXT файл**, щоб додати його до моєї бази знань."
    )

@dp.message(F.document)
async def document_handler(message: types.Message):
    doc = message.document
    file_name = doc.file_name or "document"
    
    if not (file_name.endswith('.pdf') or file_name.endswith('.txt')):
        await message.answer("Будь ласка, надішли файл у форматі **PDF** або **TXT**.")
        return

    await message.answer(f"Завантажую та обробляю файл `{file_name}`...")

    file_path = TEMP_DIR / file_name
    await bot.download(doc.file_id, destination=file_path)

    extracted_text = ""

    try:
        if file_name.endswith('.pdf'):
            reader = pypdf.PdfReader(file_path)
            for page in reader.pages:
                extracted_text += (page.extract_text() or "") + "\n"
        elif file_name.endswith('.txt'):
            with open(file_path, "r", encoding="utf-8") as f:
                extracted_text = f.read()

        if not extracted_text.strip():
            await message.answer("Не вдалося витягнути текст із файлу.")
            return

        chunks_count = rag_service.add_document(extracted_text, file_name)
        await message.answer(
            f"Успішно! Файл `{file_name}` проіндексовано.\n"
            f"Створено **{chunks_count} фрагментів** знань."
        )

    except Exception as e:
        await message.answer(f"Помилка при обробці файлу: {e}")
    finally:
        if file_path.exists():
            os.remove(file_path)

@dp.message()
async def query_handler(message: types.Message):
    user_id = message.from_user.id
    
    history = await get_recent_history(user_id, limit=6)
    
    await message.bot.send_chat_action(chat_id=message.chat.id, action="typing")
    
    answer = rag_service.answer_question(message.text, history=history)
    
    await add_message(user_id, "user", message.text)
    await add_message(user_id, "model", answer)
    
    await message.answer(answer)

async def main():
    await init_db()
    print("Бот запущений")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())