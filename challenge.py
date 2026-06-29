from typing import Optional, Dict
from ai_service import ai_service
from database import get_user, update_user_challenge_points
from config import settings

def start_challenge(user_id: int) -> Optional[Dict]:
    """
    Генерация эко-челленджа для пользователя.
    """
    user = get_user(user_id)

    if not user:
        print(f"Пользователь {user_id} не найден в базе данных")
        return None

    if not user.is_consent_pd:
        print(f"Пользователь {user.username} не дал согласие на обработку ПДн")
        return None

    print(f"Генерация челленджа для пользователя {user.username}...")
    challenge_text = ai_service.generation_eco_challenge()

    if not challenge_text:
        print("Ошибка генерации челленджа от ИИ.")
        return None

    return {
        "user_id": user_id,
        "challenge_text": challenge_text,
        "points": settings.CHALLENGE_SUCCESS_POINTS,
        "is_completed": False
    }


def complete_challenge(user_id: int, challenge_data: Dict) -> Dict:
    """
    Завершение челленджа и начисление баллов.
    """
    user = get_user(user_id)

    if not user:
        return {"success": False, "message": "Пользователь не найден"}

    if challenge_data.get("user_id") != user_id:
        return {"success": False, "message": "Челлендж не принадлежит этому пользователю"}

    if challenge_data.get("is_completed"):
        return {"success": False, "message": "Челлендж уже выполнен"}

    # Начисляем баллы
    points = challenge_data.get("points", settings.CHALLENGE_SUCCESS_POINTS)
    update_user_challenge_points(user_id, points)

    challenge_data["is_completed"] = True

    return {
        "success": True,
        "message": f"Челлендж выполнен! Вы получили {points} баллов.",
        "points_earned": points
    }


def get_challenge_statistics(user_id: int) -> Dict:
    """
    Получение статистики челленджей пользователя.
    """
    user = get_user(user_id)
    if not user:
        return {"success": False, "message": "Пользователь не найден"}

    return {
        "success": True,
        "challenge_points": user.challenge_points,
        "message": f"Ваши баллы за челленджи: {user.challenge_points}"
    }


if __name__ == "__main__":
    from database import init_db, create_user

    print("challenge.py\n")
    init_db()

    test_user_id = 111222333
    create_user(user_id=test_user_id, username="ChallengeTestUser")

    print("Генерация челленджа:")
    challenge = start_challenge(user_id=test_user_id)

    if challenge:
        print(f"   Задание: {challenge['challenge_text']}")
        print(f"   Награда: {challenge['points']} баллов\n")

        print("2. Выполнение челленджа:")
        result = complete_challenge(user_id=test_user_id, challenge_data=challenge)
        print(f"   {result['message']}\n")

        print("3. Повторное выполнение")
        result2 = complete_challenge(user_id=test_user_id, challenge_data=challenge)
        print(f"   {result2['message']}\n")

        print("4. Статистика:")
        stats = get_challenge_statistics(user_id=test_user_id)
        print(f"   {stats['message']}")
    else:
        print("Ошибка генерации челленджа")