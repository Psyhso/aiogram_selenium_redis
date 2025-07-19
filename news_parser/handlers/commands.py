from aiogram.types import Message
from aiogram.filters import CommandStart, Command, or_f
from aiogram import F, Router

from keyboards.reply_kb import start_kb_reply
from services.parser import parser_habr, parser_ria, parser_vk, parser_wb

command = Router()


@command.message(CommandStart())
async def start(message: Message):
    await message.answer(f'Привет, {message.from_user.first_name}! Что ты хочешь узнать?', reply_markup=start_kb_reply)


@command.message(or_f(Command('habr'), F.text == 'Habr'))
async def habr(message: Message):
    await message.answer(parser_habr(), reply_markup=start_kb_reply)


@command.message(or_f(Command('ria'), F.text == 'Ria'))
async def ria(message: Message):
    await message.answer(parser_ria(), reply_markup=start_kb_reply)


@command.message(or_f(Command('vk'), F.text == 'Vk'))
async def vk(message: Message):
    try:
        posts = parser_vk()
        
        if isinstance(posts, dict) and "error" in posts:
            await message.answer(posts["error"])
            return

        for post in posts:
            if post["photo"]:
                await message.answer_photo(
                    photo=post["photo"],
                    caption=post["text"] or "Нет текста"
                )
            else:
                await message.answer(post["text"] or "Пост без текста")
        await message.answer('Вот три поста с РиПа', reply_markup=start_kb_reply)
    except Exception as e:
        await message.answer(f"Ошибка при отправке: {str(e)}")


@command.message(or_f(Command('wb'), F.text == 'Wb'))
async def wb(message: Message):
    await message.answer(parser_wb(), reply_markup=start_kb_reply)
