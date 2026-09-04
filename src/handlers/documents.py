import os
from pathlib import Path
from aiogram import Router, types, F, Bot
import pypdf
from src.services.rag_service import RAGService

router = Router()
TEMP_DIR = Path(__file__).resolve().parent.parent.parent / "temp"

@router.message(F.document)
async def document_handler(message: types.Message, bot: Bot, rag_service: RAGService):
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
            f" Успішно! Файл `{file_name}` проіндексовано.\n"
            f"Створено **{chunks_count} фрагментів** знань."
        )

    except Exception as e:
        await message.answer(f"Помилка при обробці файлу: {e}")
    finally:
        if file_path.exists():
            os.remove(file_path)