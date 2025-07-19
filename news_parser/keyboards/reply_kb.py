from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

start_kb_reply = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text='Habr'), KeyboardButton(text='Ria')],
    [KeyboardButton(text='Vk'), KeyboardButton(text='Wb')]],
    resize_keyboard=True, one_time_keyboard=True, input_field_placeholder='Что дальше?'
)