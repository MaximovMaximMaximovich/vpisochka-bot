import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

# Настройка логирования
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# ================== ТОКЕН БОТА ==================
TOKEN = "8811206687:AAE5em4FCe6sU4sAKJApneTh2iJF1_hO1SI"
# ================================================

PROMO_MESSAGE = (
    "Сохраните наш бот и Вы ни когда нас не потеряете ❤️\n\n"
    "https://t.me/vpisochka112_bot"
)

chat_id = None

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global chat_id
    chat_id = update.effective_chat.id
    
    await update.message.reply_text(
        "✅ Бот успешно активирован в этом чате!\n\n"
        "Теперь каждые 30 мин. будет автоматически публиковаться промо-сообщение."
    )
    logger.info(f"Автопостинг настроен для чата: {chat_id}")


async def post_job(context: ContextTypes.DEFAULT_TYPE):
    global chat_id
    if not chat_id:
        logger.warning("Chat ID не установлен")
        return
    try:
        await context.bot.send_message(chat_id=chat_id, text=PROMO_MESSAGE)
        logger.info(f"Пост опубликован в чат {chat_id}")
    except Exception as e:
        logger.error(f"Ошибка публикации: {e}")


async def status(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global chat_id
    if chat_id:
        await update.message.reply_text(f"✅ Автопостинг активен\nЧат ID: {chat_id}")
    else:
        await update.message.reply_text("❌ Напишите /start в группе")


def main():
    application = Application.builder().token(TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("status", status))

    # Автопост каждые 3 часа
    application.job_queue.run_repeating(
        post_job, 
        interval=1800,   # 30 мин
        first=30
    )

    logger.info("Бот успешно запущен и готов к работе!")
    application.run_polling()


if __name__ == "__main__":
    main()
