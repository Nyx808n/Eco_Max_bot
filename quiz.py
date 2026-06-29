from typing import Optional, Dict, List

from ai_service import ai_service
from database import get_user, update_user_quiz_points
from config import settings

def start_quiz(user_id: int, topic: str = "экология") -> Optional[Dict]:
    """""
    Старт викторины
    """""
    user = get_user(user_id)

    if not user:
        print(f"Пользователь {user_id} не найден в базе данных")
        return None

    if not user.is_consent_pd:
        print(f"Пользователь {user.username} не дал согласие на обработку ПДн")
        return None

    print(f"Генерация вопроса для пользователя {user.username} (тема: {topic})...")
    question = ai_service.generation_quiz_question(topic)

    if not question:
        print("Ошибка генерации вопроса от ИИ.")
        return None

    return question

def check_correct_answer(user_id: int, answer_index: int, question: Dict) -> Optional[Dict]:
    """""
    Проверка ответа и начисление балов
    """""
    user = get_user(user_id)

    if not user:
        print("Пользователь {user_id} не найден в базе данных")
        return None

    if not user.is_consent_pd:
        print(f"Пользователь {user.username} не дал согласие на обработку ПДн")
        return None

    is_correct = answer_index == question["correct_index"]

    result = {
        "is_correct": is_correct,
        "points_earned": 0,
        "message": ""
    }

    if is_correct:
        points = settings.QUIZ_CORRECT_POINTS
        update_user_quiz_points(user_id, points)

        result["points_earned"] = points
        result["message"] = f"Правильно! Вы получили {points} баллов."
    else:
        correct_option = question["options"][question["correct_index"]]
        result["message"] = f"Неправильно. Правильный ответ: {correct_option}"

    return result


if __name__ == "__main__":

    from database import init_db, create_user
    print("\n\n")
    print("Старт викторины")

    init_db()
    test_user_id = 111222333
    create_user(user_id=test_user_id, username="QuizTestUser")

    qu = start_quiz(user_id=test_user_id, topic="экология")

    if qu:
        print("Вопрос успешно сгенерирован:")
        print(f"Вопрос: {qu['question']}")
        print(f"Варианты: {qu['options']}")
        print(f"Правильный индекс: {qu['correct_index']}")
        print(f"Пояснение: {qu['explanation']}")


        print("\n\n")

        print("Проверка ответов")
        answer = int(input("Введите ответ "))

        dict_answer = check_correct_answer(user_id=test_user_id, answer_index=answer, question=qu)

        if dict_answer:
            print(dict_answer.get("message"))
            print(f"общие очки викторины пользователся {get_user(user_id=test_user_id).username} составляют {get_user(user_id=test_user_id).quiz_points}")
        else:
            print("error")
    else:
        print("error\n")
        print("qu is NONE\n")