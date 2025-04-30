from aiogram import Router, types
from config import ADMIN_ID

router = Router()

# Dictionary orqali foydalanuvchini aniqlash
user_cache = {}

@router.message()
async def catch_all_messages(message: types.Message):
    # 1. Agar bu admin yozgan bo‘lsa:
    if message.from_user.id == ADMIN_ID:
        # Reply qilib yozayotgan bo‘lsa:
        if message.reply_to_message:
            # Reply bo‘layotgan xabarda asl foydalanuvchining ID’si bo‘lishi kerak
            original_text = message.reply_to_message.text

            # Foydalanuvchining ID sini olishga harakat qilamiz
            for user_id, text in user_cache.items():
                if text in original_text:
                    try:
                        await message.bot.send_message(
                            chat_id=user_id,
                            text=message.text
                        )
                    except Exception as e:
                        await message.bot.send_message(chat_id=ADMIN_ID, text=f"Xatolik: {e}")
                    return
        return  # admin yozgan xabarni boshqa joyga yubormaymiz

    # 2. Agar bu foydalanuvchi yozgan bo‘lsa:
    if not message.text.startswith("/"):
        # Foydalanuvchini cache ga qo‘shib qo‘yamiz
        user_cache[message.from_user.id] = message.text[:20]  # qisqa xotira uchun faqat 20 ta belgini saqlaymiz

        await message.bot.send_message(
            chat_id=ADMIN_ID,
            text=f"📥 Yangi xabar:\n\n👤 {message.from_user.full_name} (@{message.from_user.username})\n🆔 ID: {message.from_user.id}\n\n✉️ {message.text}"
        )
