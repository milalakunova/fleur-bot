from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, MessageHandler, ContextTypes, filters
import os

TOKEN = os.environ["TOKEN"]
ADMIN_USERNAME = "@aleks_stali"  # ← Замени на свой username

models = [
    {
        "name": "Алиса, 24",
        "city": "Кишинёв",
        "desc": "Изысканная, внимательная. Сопровождение для настоящих ценителей."
    },
    {
        "name": "Эва, 26",
        "city": "Бельцы",
        "desc": "Тихая сила и тонкий шарм. Для деловых встреч и ужинов."
    }
]

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("📸 Модели", callback_data="show_models")],
        [InlineKeyboardButton("📍 Города", callback_data="cities")],
        [InlineKeyboardButton("📆 Запрос", callback_data="book")],
        [InlineKeyboardButton("📞 Менеджер", url=f"https://t.me/{ADMIN_USERNAME.strip('@')}")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text(
        "🌸 *Добро пожаловать в Fleur de Moldova* 🌸\n"
        "Элегантное сопровождение по Молдове\n"
        "Дискретно. Стильно. По личному запросу.\n\n"
        "Выберите действие ниже 👇",
        reply_markup=reply_markup,
        parse_mode="Markdown"
    )

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == "show_models":
        for model in models:
            await query.message.reply_text(
                f"👤 *{model['name']}* — {model['city']}\n_{model['desc']}_",
                parse_mode="Markdown"
            )
    elif query.data == "cities":
        cities = sorted(set([m['city'] for m in models]))
        await query.message.reply_text("📍 Доступные города:\n" + "\n".join(f"• {c}" for c in cities))
    elif query.data == "book":
        await query.message.reply_text("📆 Укажите имя, город, дату и предпочтения — менеджер свяжется с вами.")
        context.user_data['booking'] = True

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if context.user_data.get('booking'):
        text = update.message.text
        await context.bot.send_message(chat_id=ADMIN_USERNAME, text=f"📥 Новая заявка:\n{text}")
        await update.message.reply_text("Спасибо! Менеджер скоро с вами свяжется.")
        context.user_data['booking'] = False

app = ApplicationBuilder().token(TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(CallbackQueryHandler(button_handler))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
app.run_polling()
