import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

TOKEN = "8985528943:AAEvYf4QSDcME0uqQTa7pxyg2ZxOTEUCkts"

bot = Bot(token=TOKEN)
dp = Dispatcher()

menu = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="🚕 Начать смену")],
        [KeyboardButton(text="📊 Моя статистика")],
        [KeyboardButton(text="🏆 Топ недели")],
        [KeyboardButton(text="📖 Правила")]
    ],
    resize_keyboard=True
)

@dp.message()
async def handler(message: types.Message):

    if message.text == "/start":
        await message.answer(
            "🚖 BLACK TAXI\n\nДобро пожаловать!",
            reply_markup=menu
        )

    elif message.text == "🚕 Начать смену":
        await message.answer("🟢 Смена начата")

    elif message.text == "📊 Моя статистика":
        await message.answer("📊 Пока нет данных")

    elif message.text == "🏆 Топ недели":
        await message.answer("🏆 Скоро будет рейтинг")

    elif message.text == "📖 Правила":
        await message.answer("📖 Работай и выполняй заказы")

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
