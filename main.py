import os
import asyncio
import datetime

from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

bot = Bot(token=os.getenv("BOT_TOKEN"))
dp = Dispatcher()

shifts = {}

def menu():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🟢 Начать смену", callback_data="start")],
        [InlineKeyboardButton(text="🔴 Завершить смену", callback_data="end")],
        [InlineKeyboardButton(text="📊 Статистика", callback_data="stats")]
    ])

@dp.message(Command("start"))
async def start(msg: types.Message):
    await msg.answer("🚕 Black Taxi Manager", reply_markup=menu())

@dp.callback_query()
async def cb(call: types.CallbackQuery):
    uid = call.from_user.id

    if call.data == "start":
        shifts[uid] = {"start": datetime.datetime.now()}
        await call.message.answer("🟢 Смена начата")

    elif call.data == "end":
        if uid not in shifts:
            await call.message.answer("❌ Нет активной смены")
            return

        start = shifts[uid]["start"]
        end = datetime.datetime.now()
        duration = end - start

        await call.message.answer(f"🔴 Смена завершена\n⏱ {duration}")

    elif call.data == "stats":
        if uid not in shifts:
            await call.message.answer("📊 Пока нет данных")
        else:
            await call.message.answer(str(shifts[uid]))

    await call.answer()

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
