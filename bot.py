import os
import json
import calendar
from datetime import datetime
from datetime import datetime
from telegram.error import TelegramError
from dotenv import load_dotenv

from telegram import (
    Update,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
)

from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
    ContextTypes,
)

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
ADMIN_ID = int(os.getenv("ADMIN_ID"))

DATA_FILE = "reminders.json"


def load_data():
    if not os.path.exists(DATA_FILE):
        with open(DATA_FILE, "w") as f:
            json.dump({}, f)
    with open(DATA_FILE, "r") as f:
        return json.load(f)


def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=4)


user_setting = {
    "day": datetime.now().day,
    "month": datetime.now().month,
    "year": datetime.now().year,
    "hour": datetime.now().hour,
    "minute": datetime.now().minute,
}


def menu():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("📅 Date", callback_data="date")],
        [InlineKeyboardButton("🕒 Time", callback_data="time")],
        [InlineKeyboardButton("💾 Save Reminder", callback_data="save")],
        [InlineKeyboardButton("📋 My Reminder", callback_data="view")],
        [InlineKeyboardButton("🗑 Delete Reminder", callback_data="delete")],
    ])


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    if update.effective_user.id != ADMIN_ID:
        await update.message.reply_text(
            "❌ This bot is private.\nOnly Admin can use this bot."
        )
        return

    now = datetime.now()

    text = (
        "🤖 Reminder Bot\n\n"
        f"📅 Today : {now.strftime('%d-%m-%Y')}\n"
        f"🕒 Time : {now.strftime('%H:%M')}\n\n"
        "Choose an option."
    )

    await update.message.reply_text(
        text,
        reply_markup=menu()
  )
  def date_keyboard():
    return InlineKeyboardMarkup([
        [
            InlineKeyboardButton("◀ Day", callback_data="day_minus"),
            InlineKeyboardButton(str(user_setting["day"]), callback_data="none"),
            InlineKeyboardButton("Day ▶", callback_data="day_plus"),
        ],
        [
            InlineKeyboardButton("◀ Month", callback_data="month_minus"),
            InlineKeyboardButton(str(user_setting["month"]), callback_data="none"),
            InlineKeyboardButton("Month ▶", callback_data="month_plus"),
        ],
        [
            InlineKeyboardButton("◀ Year", callback_data="year_minus"),
            InlineKeyboardButton(str(user_setting["year"]), callback_data="none"),
            InlineKeyboardButton("Year ▶", callback_data="year_plus"),
        ],
        [
            InlineKeyboardButton("✅ Done", callback_data="done"),
            InlineKeyboardButton("⬅ Back", callback_data="back"),
        ],
    ])


async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == "date":
        await query.edit_message_text(
            "📅 Date Settings",
            reply_markup=date_keyboard()
        )
        return
      if query.data == "day_plus":
        max_day = calendar.monthrange(
            user_setting["year"],
            user_setting["month"]
        )[1]

        if user_setting["day"] < max_day:
            user_setting["day"] += 1

        await query.edit_message_reply_markup(
            reply_markup=date_keyboard()
        )
        return

    if query.data == "day_minus":
        if user_setting["day"] > 1:
            user_setting["day"] -= 1

        await query.edit_message_reply_markup(
            reply_markup=date_keyboard()
        )
        return

    if query.data == "month_plus":
        if user_setting["month"] < 12:
            user_setting["month"] += 1

        await query.edit_message_reply_markup(
            reply_markup=date_keyboard()
        )
        return

    if query.data == "month_minus":
        if user_setting["month"] > 1:
            user_setting["month"] -= 1

        await query.edit_message_reply_markup(
            reply_markup=date_keyboard()
        )
        return

    if query.data == "year_plus":
        user_setting["year"] += 1

        await query.edit_message_reply_markup(
            reply_markup=date_keyboard()
        )
        return

    if query.data == "year_minus":
        if user_setting["year"] > 2025:
            user_setting["year"] -= 1

        await query.edit_message_reply_markup(
            reply_markup=date_keyboard()
        )
        return
      def time_keyboard():
    return InlineKeyboardMarkup([
        [
            InlineKeyboardButton("◀ Hour", callback_data="hour_minus"),
            InlineKeyboardButton(str(user_setting["hour"]).zfill(2), callback_data="none"),
            InlineKeyboardButton("Hour ▶", callback_data="hour_plus"),
        ],
        [
            InlineKeyboardButton("◀ Minute", callback_data="minute_minus"),
            InlineKeyboardButton(str(user_setting["minute"]).zfill(2), callback_data="none"),
            InlineKeyboardButton("Minute ▶", callback_data="minute_plus"),
        ],
        [
            InlineKeyboardButton("✅ Done", callback_data="done"),
            InlineKeyboardButton("⬅ Back", callback_data="back"),
        ],
    ])
if query.data == "save":

        data = load_data()

        data[str(ADMIN_ID)] = {
            "day": user_setting["day"],
            "month": user_setting["month"],
            "year": user_setting["year"],
            "hour": user_setting["hour"],
            "minute": user_setting["minute"],
        }

        save_data(data)

        await query.edit_message_text(
            f"""✅ Reminder Saved

📅 Date : {user_setting['day']:02d}-{user_setting['month']:02d}-{user_setting['year']}

🕒 Time : {user_setting['hour']:02d}:{user_setting['minute']:02d}

Bot will notify you automatically."""
        )
        return


    if query.data == "view":

        data = load_data()

        if str(ADMIN_ID) not in data:
            await query.edit_message_text("❌ No reminder found.")
            return

        r = data[str(ADMIN_ID)]

        await query.edit_message_text(
            f"""📋 Saved Reminder

📅 {r['day']:02d}-{r['month']:02d}-{r['year']}

🕒 {r['hour']:02d}:{r['minute']:02d}"""
        )
        return


    if query.data == "delete":

        data = load_data()

        if str(ADMIN_ID) in data:
            del data[str(ADMIN_ID)]
            save_data(data)

        await query.edit_message_text("🗑 Reminder Deleted Successfully.")
        return
      async def reminder_checker(context: ContextTypes.DEFAULT_TYPE):

    data = load_data()

    if str(ADMIN_ID) not in data:
        return

    r = data[str(ADMIN_ID)]

    now = datetime.now()

    if (
        now.day == r["day"]
        and now.month == r["month"]
        and now.year == r["year"]
        and now.hour == r["hour"]
        and now.minute == r["minute"]
    ):

        try:
            await context.bot.send_message(
                chat_id=ADMIN_ID,
                text=(
                    "🔔 Reminder!\n\n"
                    "আজ তোমার Best Friend-কে মেসেজ দেওয়ার দিন। ❤️\n\n"
                    "ভুলে যেও না!"
                ),
            )

            del data[str(ADMIN_ID)]
            save_data(data)

        except TelegramError:
            pass
          def main():

    app = Application.builder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))

    app.add_handler(
        CallbackQueryHandler(button)
    )

    job_queue = app.job_queue

    job_queue.run_repeating(
        reminder_checker,
        interval=60,
        first=5,
    )

    print("✅ Reminder Bot Started...")

    app.run_polling(
        drop_pending_updates=True
    )


if __name__ == "__main__":
    main()
