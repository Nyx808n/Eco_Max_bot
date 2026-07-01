import requests
from config import settings
def send_message(chat_id, text, keyboard: dict = None):
    """Отправка сообщения"""
    params = {"chat_id": chat_id}
    data = {"text": text}

    resp = requests.post(
        f"{settings.API_URL}/messages",
        headers={"Authorization": settings.MAX_BOT_TOKEN},
        params=params,
        json=data
    )
    print(f"✅ Отправлено в {chat_id}: {text}")
    if resp.status_code != 200:
        print(f"❌ Ошибка отправки: {resp.status_code} - {resp.text}")
    return resp.json()