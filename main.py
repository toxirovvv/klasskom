from aiogram import Bot, Dispatcher
from aiogram.types import BotCommand
from aiogram.fsm.storage.memory import MemoryStorage
from handlers import menu
from config import BOT_TOKEN
from aiogram.client.default import DefaultBotProperties
from handlers import menu, message_handler

import asyncio

async def main():
    bot = Bot(token=BOT_TOKEN, default=DefaultBotProperties(parse_mode="HTML"))
    dp = Dispatcher(storage=MemoryStorage())

    dp.include_router(menu.router)
    dp.include_router(message_handler.router)

    await bot.set_my_commands([
        BotCommand(command="start", description="Botni ishga tushirish"),
    ])
    

    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
