from typing import List, Dict, Optional
from config import settings
from database import get_db_session, User, get_subscribed_users

def is_admin(user_id: int) -> bool:
    """
    Проверяет, является ли пользователь администратором.
    """
    return user_id in settings.ADMIN_IDS


def get_global_stats() -> Dict:
    """
    Получение глобальной статистики бота.
    """
    db = get_db_session()
    try:
        total_users = db.query(User).count()

        total_quiz_points = db.query(User).with_entities(
            db.query(User.quiz_points).subquery()
        ).count()  # Упрощенный вариант, лучше через func.sum

        from sqlalchemy import func
        sum_quiz = db.query(func.sum(User.quiz_points)).scalar() or 0
        sum_challenge = db.query(func.sum(User.challenge_points)).scalar() or 0
        total_points = sum_quiz + sum_challenge

        subscribed_count = len(get_subscribed_users())

        return {
            "total_users": total_users,
            "subscribed_users": subscribed_count,
            "total_points_distributed": total_points,
            "sum_quiz": sum_quiz,
            "sum_challenge": sum_challenge
        }
    finally:
        db.close()


def broadcast_message(message: str, only_subscribed: bool = False) -> List[int]:
    """
    Массовая раасылка
    Возвращает список ID пользователей, которым отправлено сообщение.
    """
    db = get_db_session()
    try:
        if only_subscribed:
            target_ids = get_subscribed_users()
        else:
            # Берем всех зарегистрированных пользователей
            users = db.query(User).all()
            target_ids = [user.user_id for user in users]

        # потом из max api рассылать сообщения
        # for uid in target_ids:
        #     send_message(uid, message)

        print(f"Рассылка '{message[:30]}...' отправлена {len(target_ids)} пользователям.")
        return target_ids

    finally:
        db.close()

def format_global_stats(stats: Dict) -> str:
    """
    Форматирование статистики для вывода.
    """
    text = "Глобальная статистика бота:\n\n"
    text += f" Всего пользователей: {stats['total_users']}\n"
    text += f"Подписано на рассылку: {stats['subscribed_users']}\n\n"
    text += f"Всего баллов выдано: {stats['total_points_distributed']}\n"
    text += f"   - За викторины: {stats['sum_quiz']}\n"
    text += f"   - За челленджи: {stats['sum_challenge']}\n"
    return text


if __name__ == "__main__":
    from database import init_db, create_user

    print("--- Тест модуля admin_panel.py ---\n")
    init_db()

    test_users = [
        (111222333, "QuizTestUser"),
        (222333444, "EcoWarrior"),
        (999999999, "CorrectAdmin"),
    ]
    for user_id, username in test_users:
        create_user(user_id=user_id, username=username)

    print("1. Проверка прав администратора:")
    admin_id = 123456789
    regular_id = 111222333

    print(f"   ID {admin_id} — админ? {is_admin(admin_id)}")
    print(f"   ID {regular_id} — админ? {is_admin(regular_id)}")

    print("2. Глобальная статистика:")
    stats = get_global_stats()
    print(format_global_stats(stats))

    print("3. Тест массовой рассылки:")
    broadcast_message("Внимание! Завтра День Земли!", only_subscribed=False)