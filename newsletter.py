# newsletter.py
# Модуль рассылки эко-советов пользователям

import random
from datetime import datetime
from ai_service import ai_service

import schedule
import time

from config import settings
from database import (
    get_user,
    update_newsletter_status,
    is_user_subscribed,
    get_subscribed_users,
)


def generate_eco_tip_with_ai() -> str:
    """
    Генерирует эко-совет через ИИ.
    """
    
    advice = ai_service.generation_eco_advice()

    if not advice:
        return "Ошибка генерации эко совета. \n Мы уже занимаемся решением данной проблемы. \n Ожидайте."

    return advice


def subscribe_user(user_id: int) -> str:
    """
    Оформляет подписку пользователя на ежедневные эко-советы.
    """

    user = get_user(user_id)

    if not user:
        return "Сначала необходимо пройти регистрацию."

    update_newsletter_status(user_id, True)

    return "Вы успешно подписались на ежедневные эко-советы."


def unsubscribe_user(user_id: int) -> str:
    """
    Отключает подписку пользователя на ежедневные эко-советы.
    """

    user = get_user(user_id)

    if not user:
        return "Пользователь не найден."

    update_newsletter_status(user_id, False)

    return "Вы отписались от ежедневной рассылки эко-советов."


def create_eco_tip_message() -> str:
    """
    Формирует сообщение с эко-советом.
    """

    eco_tip = generate_eco_tip_with_ai()

    return f"🌱 Эко-совет дня:\n\n{eco_tip}"


def send_eco_tip_now(user_id: int) -> str:
    """
    Возвращает пользователю эко-совет сразу после нажатия кнопки.
    """

    user = get_user(user_id)

    if not user:
        return "Сначала необходимо пройти регистрацию."

    return create_eco_tip_message()


def send_daily_tip_to_user(user_id: int) -> str:
    """
    Формирует ежедневный эко-совет для одного пользователя.
    """

    message = create_eco_tip_message()

    # Здесь main.py должен отправить это сообщение пользователю через MAX API
    # Например:
    # send_message(user_id, message)

    print(f"Эко-совет отправлен пользователю {user_id}")

    return message


def send_daily_tips_to_all_users() -> None:
    """
    Отправляет ежедневный эко-совет всем подписанным пользователям.
    """

    users = get_subscribed_users()

    for user_id in users:
        send_daily_tip_to_user(user_id)

    print(f"Рассылка эко-советов выполнена: {datetime.now()}")


def start_newsletter_schedule() -> None:
    """
    Запускает ежедневную рассылку по расписанию.
    """

    schedule.every().day.at(settings.NEWSLETTER_TIME).do(send_daily_tips_to_all_users)

    print(f"Рассылка эко-советов запущена на {settings.NEWSLETTER_TIME}")

    while True:
        schedule.run_pending()
        time.sleep(60)


def get_newsletter_status_text(user_id: int) -> str:
    """
    Возвращает текст о статусе подписки пользователя.
    """

    if is_user_subscribed(user_id):
        return "Вы уже подписаны на ежедневные эко-советы."

    return "Вы пока не подписаны на ежедневные эко-советы."


def handle_newsletter_button(user_id: int, callback: str) -> str:
    """
    Обрабатывает кнопки раздела 'Эко-совет дня'.
    """

    if callback == "eco_tip":
        return send_eco_tip_now(user_id)

    if callback == "eco_tip_subscribe":
        return "Подтвердите подписку на ежедневные эко-советы."

    if callback == "eco_tip_confirm_subscribe":
        return subscribe_user(user_id)

    if callback == "eco_tip_unsubscribe":
        return unsubscribe_user(user_id)

    return "Неизвестное действие."


if __name__ == "__main__":
    from database import init_db, create_user

    print("newsletter.py\n")

    init_db()

    test_user_id = 999888777
    create_user(user_id=test_user_id, username="NewsletterTestUser")

    # Тест 1: Проверка статуса до подписки
    print("1. Статус до подписки:")
    print(get_newsletter_status_text(test_user_id))

    # Тест 2: Подписка
    print("\n2. Оформление подписки:")
    print(subscribe_user(test_user_id))
    print(get_newsletter_status_text(test_user_id))

    # Тест 3: Получение совета прямо сейчас
    print("\n3. Получение эко-совета:")
    print(send_eco_tip_now(test_user_id))

    # Тест 4: Отписка
    print("\n4. Отписка от рассылки:")
    print(unsubscribe_user(test_user_id))
    print(get_newsletter_status_text(test_user_id))