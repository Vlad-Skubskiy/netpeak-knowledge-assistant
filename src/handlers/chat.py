from aiogram import Router, types
from src.services.rag_service import RAGService
from src.db.database import add_message, get_recent_history

router = Router()

@router.message()
async def query_handler(message: types.Message, rag_service: RAGService):
    user_id = message.from_user.id
    history = await get_recent_history(user_id, limit=6)
    
    await message.bot.send_chat_action(chat_id=message.chat.id, action="typing")
    
    answer = rag_service.answer_question(message.text, history=history)
    
    await add_message(user_id, "user", message.text)
    await add_message(user_id, "model", answer)
    
    await message.answer(answer)