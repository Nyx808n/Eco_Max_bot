from flask import Flask, request, jsonify
import requests
from config import settings

from Utility import send_message

TOKEN = settings.MAX_BOT_TOKEN
MAX_WEBHOOK_URL = settings.MAX_WEBHOOK_URL
HEADERS = {"Authorization": TOKEN}
API_URL = "https://platform-api.max.ru"

app = Flask(__name__)

"""
Пока тут тест логика не относящиеся к теме бота
"""

@app.route('/webhook', methods=['POST'])
def webhook():
    """Сюда MAX будет присылать обновления"""
    print("📥 Входящий webhook запрос!")
    print(f"Headers: {request.headers}")
    print(f"Data: {request.get_data(as_text=True)}")

    try:
        data = request.json
        print(f"📨 Получены данные: {data}")

        # MAX может присылать разные типы событий
        update_type = data.get("update_type")
        print(f"Тип события: {update_type}")

        if update_type == "message_created":
            msg = data.get("message", {})
            chat_id = msg.get("recipient", {}).get("chat_id")
            text = msg.get("body", {}).get("text", "")

            if not chat_id or not text:
                return {}

            if (text == "/start"):
                print(f"💬  от {chat_id}: '{text}'")
                send_message(chat_id, f"здравстуйте я бот")
            else:
                print(f"💬 Сообщение от {chat_id}: '{text}'")
                send_message(chat_id, f"сообщение {text}")
        else:
            print(f"⚠️ Игнорируем событие типа: {update_type}")

    except Exception as e:
        print(f"❌ Ошибка обработки webhook: {e}")
        import traceback
        traceback.print_exc()

    # ВАЖНО: Нужно всегда возвращать 200 OK
    return jsonify({"status": "ok"}), 200


@app.route('/health', methods=['GET'])
def health():
    """Проверка работоспособности"""
    return jsonify({"status": "ok"}), 200



def start_bot():
    """Логики после команды старт"""


def subscribe_webhook(webhook_url):
    """Подписываем наш URL на получение событий от MAX"""
    print(f"🔔 Подписка на webhook: {webhook_url}")

    # Сначала отпишемся от всех старых подписок (на всякий случай)
    print("🗑️ Очищаем старые подписки...")
    try:
        resp_delete = requests.delete(
            f"{API_URL}/subscriptions",
            headers=HEADERS
        )
        print(f"Старые подписки удалены: {resp_delete.status_code}")
    except:
        pass

    payload = {
        "update_types": [
            "message_created",
        ],
        "url": webhook_url
    }

    resp = requests.post(
        f"{API_URL}/subscriptions",
        headers=HEADERS,
        json=payload
    )

    print(f"📋 Ответ от API подписки: {resp.status_code}")
    print(f"📋 Тело ответа: {resp.text}")

    if resp.status_code == 200:
        print(f"✅ Webhook успешно подписан на {webhook_url}")
    else:
        print(f"❌ Ошибка подписки: {resp.status_code} - {resp.text}")

    return resp.json()


if __name__ == '__main__':

    print("=" * 60)
    print(f"🌐 Webhook URL: {MAX_WEBHOOK_URL}")
    print("=" * 60)

    # Проверяем доступность туннеля
    try:
        test_resp = requests.get(MAX_WEBHOOK_URL.replace('/webhook', '/health'), timeout=5)
        print(f"✅ Туннель работает! Ответ: {test_resp.status_code}")
    except Exception as e:
        print(f"❌ Туннель недоступен: {e}")
        print("💡 Убедитесь, что cloudflared запущен и URL актуален")

    # Подписываемся на webhook
    subscribe_webhook(MAX_WEBHOOK_URL)

    # Запускаем веб-сервер
    print("🚀 Webhook-сервер запущен на порту 5000...")
    print("💡 Ожидаю входящие сообщения...")
    print("=" * 60)
    app.run(host='0.0.0.0', port=5000, debug=True)