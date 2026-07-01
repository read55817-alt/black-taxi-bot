from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import asyncio
import datetime

bot = Bot(token="YOUR_TOKEN")
dp = Dispatcher()

shifts = {}

# ===== КНОПКИ =====
def main_menu():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🟢 Начать смену", callback_data="start_shift")],
        [InlineKeyboardButton(text="🔴 Завершить смену", callback_data="end_shift")],
        [InlineKeyboardButton(text="📊 Моя статистика", callback_data="stats")]
    ])

# ===== /start =====
@dp.message(Command("start"))
async def start(msg: types.Message):
    await msg.answer(
        "🚕 Black Taxi Manager\nВыбери действие:",
        reply_markup=main_menu()
    )

# ===== НАЖАТИЯ КНОПОК =====
@dp.callback_query()
async def handler(call: types.CallbackQuery):
    user_id = call.from_user.id

    # 🟢 START SHIFT
    if call.data == "start_shift":
        shifts[user_id] = {
            "start": datetime.datetime.now(),
            "end": None
        }
        await call.message.answer("🟢 Смена начата")

    # 🔴 END SHIFT
    elif call.data == "end_shift":
        if user_id not in shifts or shifts[user_id]["end"] is not None:
            await call.message.answer("❌ Нет активной смены")
            return

        shifts[user_id]["end"] = datetime.datetime.now()

        start = shifts[user_id]["start"]
        end = shifts[user_id]["end"]

        duration = end - start

        await call.message.answer(f"🔴 Смена завершена\n⏱ Время: {duration}")

    # 📊 STATS
    elif call.data == "stats":
        if user_id not in shifts:
            await call.message.answer("📊 Пока нет данных")
        else:
            await call.message.answer(str(shifts[user_id]))

    await call.answer()

# ===== RUN =====
async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
