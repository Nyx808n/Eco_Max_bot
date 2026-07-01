from Eco_Max_bot import bot
from config import settings

if __name__ == "__main__":
    # Запускаем бота
    bot.run(webhook_url=settings.MAX_WEBHOOK_URL)