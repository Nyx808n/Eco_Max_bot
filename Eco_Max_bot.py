from flask import Flask, request, jsonify
import requests
from config import settings
from buttons import *  # Лучше заменить на конкретные импорты
from Utility import send_message
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class EcoMaxBot:

    def __init__(self):
        # Создаём ОДНО Flask-приложение
        self.app = Flask(__name__)
        self.token = settings.MAX_BOT_TOKEN
        self.api_url = "https://platform-api.max.ru"
        self.headers = {"Authorization": self.token}

        # Получаем ID бота для фильтрации своих сообщений
        self.bot_user_id = self._get_bot_id()

        # Регистрируем маршруты
        self.app.route('/webhook', methods=['POST'])(self.webhook)
        self.app.route('/health', methods=['GET'])(self.health)  # ← Раскомментировали

    def _get_bot_id(self):
        """Получаем ID бота из API"""
        try:
            resp = requests.get(
                f"{self.api_url}/me",
                headers=self.headers,
                timeout=10
            )
            if resp.status_code == 200:
                bot_id = resp.json().get("user_id")
                logger.info(f"🤖 Бот: {resp.json().get('username')} (ID: {bot_id})")
                return bot_id
        except Exception as e:
            logger.error(f"Не удалось получить ID бота: {e}")
        return None

    def webhook(self):
        """Обработчик входящих webhook от MAX"""
        try:
            data = request.get_json()
            logger.info(f"📥 Webhook: {data}")

            update_type = data.get("update_type")

            if update_type == "message_created":
                msg = data.get("message", {})

                # ✅ ПРАВИЛЬНОЕ получение chat_id
                chat_id = msg.get("recipient", {}).get("chat_id")
                sender_id = msg.get("sender", {}).get("user_id")
                text = msg.get("body", {}).get("text", "").strip()

                # ✅ Фильтрация своих сообщений
                if sender_id == self.bot_user_id:
                    logger.info("⏭️ Пропускаем своё сообщение")
                    return jsonify({"status": "ok"}), 200

                if chat_id and text:
                    logger.info(f"💬 [{chat_id}]: {text}")

                    if text == "/start":
                        self.command_start(chat_id)
                    elif text == "/help":
                        self.command_help(chat_id)
                    else:
                        send_message(chat_id, f"Вы написали: {text}")

            elif update_type == "message_callback":  # ✅ Правильное имя
                self.handle_callback(data)

            return jsonify({"status": "ok"}), 200

        except Exception as e:
            logger.error(f"❌ Ошибка: {e}")
            import traceback
            traceback.print_exc()
            return jsonify({"status": "error"}), 500

    def health(self):
        """Проверка работоспособности"""
        return jsonify({
            "status": "ok",
            "bot_id": self.bot_user_id
        }), 200

    def handle_callback(self, data):
        """Обработка нажатий на inline-кнопки"""
        callback_data = data.get("callbackData") or data.get("message", {}).get("body", {}).get("callbackData")
        chat_id = data.get("message", {}).get("recipient", {}).get("chat_id")

        logger.info(f"🔘 Callback: {callback_data} from {chat_id}")

        # Здесь логика обработки кнопок
        if callback_data == "eco_tip":
            send_message(chat_id, "💡 Совет: используйте многоразовые сумки!")
        elif callback_data == "recycle_points":
            send_message(chat_id, "🗺️ Ближайшая точка: ул. Ленина, 10")

    def subscribe_webhook(self, webhook_url: str):
        """Подписка на webhook в API MAX"""
        logger.info(f"🔔 Подписка на webhook: {webhook_url}")

        # Очищаем старые подписки
        try:
            requests.delete(
                f"{self.api_url}/subscriptions",
                headers=self.headers,
                timeout=10
            )
            logger.info("🗑️ Старые подписки удалены")
        except:
            pass

        # ✅ Правильные имена событий
        payload = {
            "update_types": ["message_created", "message_callback"],
            "url": webhook_url
        }

        try:
            resp = requests.post(
                f"{self.api_url}/subscriptions",
                headers=self.headers,
                json=payload,
                timeout=10
            )

            if resp.status_code == 200:
                logger.info(f"✅ Webhook успешно подписан!")
            else:
                logger.error(f"❌ Ошибка подписки: {resp.status_code} - {resp.text}")

            return resp.json()

        except Exception as e:
            logger.error(f"Ошибка при подписке: {e}")
            return None

    def run(self, host='0.0.0.0', port=5000, webhook_url=None):
        """Запуск бота"""
        print("=" * 60)
        print("🤖 EcoMax Bot запускается...")
        print("=" * 60)

        if webhook_url:
            self.subscribe_webhook(webhook_url)

            # Проверяем доступность через /health
            try:
                test_url = webhook_url.replace('/webhook', '/health')
                resp = requests.get(test_url, timeout=5)
                print(f"✅ Туннель работает! Status: {resp.status_code}")
            except Exception as e:
                print(f"⚠️  Туннель недоступен: {e}")

        print(f"🌐 Сервер запущен на {host}:{port}")
        print("💡 Ожидаю сообщения...")
        print("=" * 60)

        # ⚠️ debug=True + use_reloader=False — чтобы не было двойного запуска
        self.app.run(host=host, port=port, debug=True, use_reloader=False)

    def command_start(self, chat_id: int):
        send_message(chat_id, "👋 Привет! Я эко-бот.\n\nИспользуй /help для списка команд.")

    def command_help(self, chat_id: int):
        help_text = """
📋 Доступные команды:
/start - Начать работу
/help - Список команд

🌱 Эко-возможности:
- Информация о точках сбора
- Эко-викторины
- Советы по экологии
        """
        send_message(chat_id, help_text)


bot = EcoMaxBot()

if __name__ == "__main__":
    webhook_url = settings.MAX_WEBHOOK_URL

    bot.run(webhook_url=webhook_url)