import requests
from config import settings
import time

TOKEN = settings.MAX_BOT_TOKEN
HEADERS = {"Authorization": TOKEN}
API_URL = "https://platform-api.max.ru"


def get_updates(marker=None):
    """Получить обновления через long polling"""
    params = {"timeout": 30}
    if marker:
        params["marker"] = marker

    resp = requests.get(f"{API_URL}/updates", params=params, headers=HEADERS)
    if resp.status_code != 200:
        print(f"Ошибка получения обновлений: {resp.status_code} - {resp.text}")
        return {}
    return resp.json()


def send_message(chat_id, text):
    """Отправить сообщение в чат"""
    # ВАЖНО: chat_id передается в параметрах URL (params), а не в теле (json)!
    params = {"chat_id": chat_id}
    data = {"text": text}

    resp = requests.post(
        f"{API_URL}/messages",
        headers=HEADERS,
        params=params,  # <-- chat_id здесь
        json=data  # <-- только текст здесь
    )

    print(f"Сообщение отправлено в чат {chat_id}")
    return resp.json()


def main():
    print("Бот запущен!")
    marker = None

    while True:
        data = get_updates(marker)
        updates = data.get("updates", [])

        for update in updates:
            if update.get("update_type") == "message_created":
                msg = update.get("message", {})

                # Безопасное извлечение chat_id
                chat_id = msg.get("recipient", {}).get("chat_id")
                text = msg.get("body", {}).get("text", "")

                if chat_id and text:
                    print(f"💬 Получено сообщение: '{text}'")
                    send_message(chat_id, f"Вы написали: {text}")

        marker = data.get("marker", marker)


if __name__ == "__main__":
    main()