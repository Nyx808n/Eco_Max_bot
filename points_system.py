from typing import List, Dict, Optional
from database import get_db_session, User

def get_total_points(user_id: int) -> int:
    """
    Подсчет общего количества баллов пользователя
    Суммирует quiz_points и challenge_points
    """
    db = get_db_session()
    try:
        user = db.query(User).filter(User.user_id == user_id).first()
        if not user:
            return 0
        return user.quiz_points + user.challenge_points
    finally:
        db.close()


def get_user_rank(user_id: int) -> str:
    """
    Определение ранга пользователя на основе общих баллов.
    """
    total = get_total_points(user_id)

    if total < 50:
        return "🌱 Новичок"
    elif total < 150:
        return "🌿 Эко-активист"
    elif total < 300:
        return "🌳 Эко-защитник"
    elif total < 500:
        return "🏆 Эко-герой"
    else:
        return " Эко-легенда"

def get_leaderboard(top_n: int = 10) -> List[Dict]:
    """
    Получение топ-N пользователей по общему рейтингу.
    """
    db = get_db_session()
    try:
        # Запрашиваем пользователей, сортируем по сумме баллов
        users = db.query(User).order_by(
            (User.quiz_points + User.challenge_points).desc()
        ).limit(top_n).all()

        leaderboard = []
        for rank, user in enumerate(users, start=1):
            total = user.quiz_points + user.challenge_points
            leaderboard.append({
                "rank": rank,
                "user_id": user.user_id,
                "username": user.username,
                "quiz_points": user.quiz_points,
                "challenge_points": user.challenge_points,
                "total_points": total,
                "rank_title": get_user_rank(user.user_id)
            })

        return leaderboard
    finally:
        db.close()
def get_user_stats(user_id: int) -> Optional[Dict]:
    """
    Полная статистика пользователя.
    """
    db = get_db_session()
    try:
        user = db.query(User).filter(User.user_id == user_id).first()
        if not user:
            return None

        total = user.quiz_points + user.challenge_points

        # Определяем позицию в лидерборде
        users_above = db.query(User).filter(
            (User.quiz_points + User.challenge_points) > total
        ).count()
        position = users_above + 1

        return {
            "user_id": user.user_id,
            "username": user.username,
            "quiz_points": user.quiz_points,
            "challenge_points": user.challenge_points,
            "total_points": total,
            "rank_title": get_user_rank(user.user_id),
            "leaderboard_position": position
        }
    finally:
        db.close()

def format_leaderboard(leaderboard: List[Dict]) -> str:
    """
    Форматирование лидерборда для отображения.
    """
    if not leaderboard:
        return "Лидерборд пока пуст."

    text = "🏆 ТОП-10 Эко-активистов:\n\n"

    for entry in leaderboard:
        medal = "🥇" if entry["rank"] == 1 else "🥈" if entry["rank"] == 2 else "🥉" if entry[
                                                                                         "rank"] == 3 else f"{entry['rank']}."
        text += f"{medal} {entry['username']}\n"
        text += f"   Баллы: {entry['total_points']} ({entry['rank_title']})\n"
        text += f"   Викторины: {entry['quiz_points']} | Челленджи: {entry['challenge_points']}\n\n"

    return text


if __name__ == "__main__":
    from database import init_db, create_user

    print("points_system.py\n")
    init_db()

    test_users = [
        (111222333, "QuizTestUser"),
        (222333444, "EcoWarrior"),
        (333444555, "GreenHero"),
    ]

    for user_id, username in test_users:
        create_user(user_id=user_id, username=username)

    for user_id, username in test_users:
        print(f"{username}: {get_total_points(user_id)}")

    print("2. Полная статистика пользователя 111222333:")
    stats = get_user_stats(111222333)
    if stats:
        print(f"   Имя: {stats['username']}")
        print(f"   Викторины: {stats['quiz_points']}")
        print(f"   Челленджи: {stats['challenge_points']}")
        print(f"   Всего: {stats['total_points']}")
        print(f"   Ранг: {stats['rank_title']}")
        print(f"   Позиция в лидерборде: {stats['leaderboard_position']}\n")

    print("3. Лидерборд:")
    leaderboard = get_leaderboard(top_n=10)
    print(format_leaderboard(leaderboard))
