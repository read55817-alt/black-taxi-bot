import os
import asyncio
import datetime
import sqlite3

from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

# ===== BOT =====
bot = Bot(token=os.getenv("BOT_TOKEN"))
dp = Dispatcher()

# ===== DATABASE =====
db = sqlite3.connect("taxi.db", check_same_thread=False)
cur = db.cursor()

cur.execute("""
CREATE TABLE IF NOT EXISTS shifts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    start TEXT,
    end TEXT,
    duration REAL
)
""")
db.commit()

# ===== MENU =====
def menu():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🟢 Начать смену", callback_data="start")],
        [InlineKeyboardButton(text="🔴 Завершить смену", callback_data="end")],
        [InlineKeyboardButton(text="📊 Статистика", callback_data="stats")]
    ])

# ===== START =====
@dp.message(Command("start"))
async def start(msg: types.Message):
    await msg.answer("🔥 БОТ РАБОТАЕТ НОВАЯ ВЕРСИЯ", reply_markup=menu())

# ===== CALLBACKS =====
@dp.callback_query()
async def callback(call: types.CallbackQuery):
    uid = call.from_user.id

    # 🟢 START SHIFT
    if call.data == "start":
        cur.execute("""
            INSERT INTO shifts (user_id, start, end, duration)
            VALUES (?, ?, ?, ?)
        """, (uid, datetime.datetime.now().isoformat(), None, None))
        db.commit()

        await call.message.answer("🟢 Смена начата")
        await call.answer()

    # 🔴 END SHIFT
    elif call.data == "end":
        cur.execute("""
            SELECT id, start FROM shifts
            WHERE user_id=? AND end IS NULL
            ORDER BY id DESC LIMIT 1
        """, (uid,))
        row = cur.fetchone()

        if not row:
            await call.message.answer("❌ Нет активной смены")
            await call.answer()
            return

        shift_id, start_time = row
        start_dt = datetime.datetime.fromisoformat(start_time)
        end_dt = datetime.datetime.now()

        duration = (end_dt - start_dt).total_seconds() / 60

        cur.execute("""
            UPDATE shifts
            SET end=?, duration=?
            WHERE id=?
        """, (end_dt.isoformat(), duration, shift_id))
        db.commit()

        await call.message.answer(f"🔴 Смена завершена\n⏱ {int(duration)} мин")
        await call.answer()

    # 📊 STATS
    elif call.data == "stats":
        cur.execute("""
            SELECT COUNT(*), COALESCE(SUM(duration), 0)
            FROM shifts
            WHERE user_id=?
        """, (uid,))
        data = cur.fetchone()

        await call.message.answer(
            f"📊 Статистика\n"
            f"Смен: {data[0]}\n"
            f"Минут: {int(data[1])}"
        )
        await call.answer()

# ===== RUN =====
async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
