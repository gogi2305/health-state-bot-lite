import os
import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from models import User
from analysis import calculate_energy_score, get_energy_avatar, generate_advice

# In-memory storage (for demo only)
USERS = {}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    USERS[user_id] = User(id=user_id)
    await update.message.reply_text(
        "👋 Привет! Я помогу понять твоё состояние по данным фитнес-трекера.\n\n"
        "Сначала короткий опрос:\n"
        "1. Сколько тебе лет? (пример: 32)"
    )
    return "ASK_AGE"

async def handle_age(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    try:
        age = int(update.message.text)
        USERS[user_id].age = age
        await update.message.reply_text(
            "2. Какая цель?\n"
            "• energy - энергия в течение дня\n"
            "• recovery - восстановление\n"
            "• balance - баланс (стандарт)"
        )
        return "ASK_GOAL"
    except ValueError:
        await update.message.reply_text("Только цифры. Сколько тебе лет?")
        return "ASK_AGE"

async def handle_goal(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    goal = update.message.text.lower()
    USERS[user_id].goal = goal if goal in ["energy", "recovery", "balance"] else "balance"
    
    await update.message.reply_text(
        "✅ Готово! Теперь отправь данные в формате:\n"
        "`sleep:7.5 hrv:62 steps:9800`\n\n"
        "(числа могут быть любыми)"
    )
    return "ANALYZE"

async def analyze_data(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    user = USERS.get(user_id)
    
    if not user or user.age == 0:
        await update.message.reply_text("Сначала пройди опрос: /start")
        return
    
    # Parse input like "sleep:7.5 hrv:62 steps:9800"
    data = {}
    for item in update.message.text.split():
        if ":" in item:
            key, value = item.split(":")
            data[key] = float(value) if "." in value else int(value)
    
    # Validate minimal data
    if "sleep" not in data or "hrv" not in data or "steps" not in data:
        await update.message.reply_text(
            "❌ Недостаточно данных. Пример правильного формата:\n"
            "`sleep:7.5 hrv:62 steps:9800`"
        )
        return
    
    # Calculate and show result
    score = calculate_energy_score(data, user)
    avatar = get_energy_avatar(score)
    advice = generate_advice(avatar, user)
    
    # Save to history (for demo)
    user.history.append(data)
    
    await update.message.reply_text(
        f"{avatar['emoji']} **{avatar['name']}**\n\n"
        f"Сон: {data['sleep']}ч | HRV: {data['hrv']} | Шаги: {data['steps']}\n\n"
        f"💡 {advice}\n\n"
        "Отправь новые данные завтра!",
        parse_mode="Markdown"
    )

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "💡 Как использовать:\n"
        "1. Старт: /start\n"
        "2. Отправь данные в формате:\n"
        "`sleep:7.5 hrv:62 steps:9800`\n"
        "3. Получи простой совет без медицинских обещаний"
    )

if __name__ == "__main__":
    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
    
    app = Application.builder().token(os.getenv("TELEGRAM_TOKEN")).build()
    
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, analyze_data))
    
    app.run_polling()
