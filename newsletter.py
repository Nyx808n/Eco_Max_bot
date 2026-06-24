# newsletter.py
# Модуль рассылки эко-советов пользователям

import random
import schedule
import time
from datetime import datetime


def subscribe_user(user_id):
    """
    Оформление подписки пользователя на ежедневные эко-советы.
    """

    # Обращение к database.py
    # database.update_newsletter_status(user_id, True)

    return "Вы успешно подписались на ежедневные эко-советы!"


def unsubscribe_user(user_id):
    """
    Отключение подписки пользователя от рассылки.
    """

    # Обращение к database.py
    # database.update_newsletter_status(user_id, False)

    return "Вы отписались от ежедневной рассылки эко-советов."


def get_eco_tip_of_day():
    """
    Выбор эко-совета дня.
    """

    # Обращение к database.py
    # eco_tips = database.get_all_eco_tips()

    eco_tips = [
        "Используйте многоразовую бутылку вместо пластиковых бутылок.",
        "Сортируйте бумагу, пластик, стекло и металл отдельно.",
        "Выключайте свет, когда выходите из комнаты.",
        "Берите с собой многоразовую сумку в магазин.",
        "Сдавайте батарейки в специальные пункты приёма.",
        "Сократите использование одноразовой посуды.",
        "Пользуйтесь общественным транспортом или ходите пешком чаще."
    ]

    if not eco_tips:
        return "Сегодня эко-совет недоступен."

    return random.choice(eco_tips)


def send_daily_tip_to_user(user_id):
    """
    Отправка ежедневного эко-совета одному пользователю.
    """

    eco_tip = get_eco_tip_of_day()

    message = f"🌱 Эко-совет дня:\n\n{eco_tip}"

    # Обращение к main.py или модулю отправки сообщений
    # bot.send_message(user_id, message)

    print(f"Сообщение отправлено пользователю {user_id}: {message}")

    return message


def send_daily_tips_to_all_users():
    """
    Отправка ежедневного совета всем подписанным пользователям.
    """

    # Обращение к database.py
    # users = database.get_subscribed_users()

    users = [101, 102, 103]  # Временные данные для примера

    for user_id in users:
        send_daily_tip_to_user(user_id)

    print(f"Рассылка выполнена: {datetime.now()}")


def start_newsletter_schedule():
    """
    Запуск рассылки по расписанию.
    По ТЗ советы отправляются ежедневно.
    """

    schedule.every().day.at("09:00").do(send_daily_tips_to_all_users)

    print("Рассылка эко-советов запущена. Время отправки: 09:00")

    while True:
        schedule.run_pending()
        time.sleep(60)


def handle_newsletter_button(user_id, action):
    """
    Обработка кнопок рассылки.
    """

    # Обращение к buttons.py
    # Отвечает за кнопки:
    # - Подписаться на эко-советы
    # - Отключить рассылку
    # - Получить совет сейчас

    if action == "subscribe":
        return subscribe_user(user_id)

    elif action == "unsubscribe":
        return unsubscribe_user(user_id)

    elif action == "get_tip_now":
        return send_daily_tip_to_user(user_id)

    else:
        return "Неизвестное действие."