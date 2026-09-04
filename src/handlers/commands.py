from aiogram import Router, types
from aiogram.filters import CommandStart, Command
from src.db.database import clear_user_history

router = Router()

@router.message(CommandStart())
async def start_handler(message: types.Message):
    await message.answer(
        "Привіт! Я корпоративний AI-асистент.\n\n"
        "• Задай питання по базі знань\n"
        "• Надішли **PDF / TXT файл** для додавання документа\n"
        "• Введи `/clear`, щоб очистити контекст нашої розмови"
    )

@router.message(Command("clear"))
async def clear_handler(message: types.Message):
    await clear_user_history(message.from_user.id)
    await message.answer(" Пам'ять діалогу успішно очищена!")