import asyncio
import os
import logging
from dotenv import load_dotenv
from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties

from handlers.commands import command


load_dotenv()
dp = Dispatcher()


async def main():
    # await create_db()
    # dp.update.middleware(DataBaseSession(session_pool=session_maker))
    bot = Bot(token=os.getenv('TOKEN'), default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    dp.include_routers(command)
    await dp.start_polling(bot)



if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    print('Бот включен!')
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print('Бот выключен!')
