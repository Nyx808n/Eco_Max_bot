from config import settings
from gigachat import GigaChat
from typing import Optional

import re
import json

class AIServes:
    """Работа с гигачатом"""

    def __init__(self):
        self.giga = GigaChat(
            credentials=f"{settings.GIGACHAT_AUTH_KEY}",
            verify_ssl_certs=False
        )

    def receiving_answer_from_ai(self, context: str = "") -> Optional[str]:
        if context == "":
            return "context input is nullptr"

        try:
            response = self.giga.chat(context)
            return response.choices[0].message.content
        except:
            print("error in AIServes|receiving_answer_from_ai")
            return None

    def generation_eco_advice(self)-> Optional[str]:
        context = "Сгенерируй интересный эко совет не поврторяя прошлые" #then edit promt
        return self.receiving_answer_from_ai(context)

    def generation_eco_challenge(self) -> Optional[str]:
        context = "Сгенерируй ОДИН короткий и простой эко-челлендж, который можно выполнить за один день (например, собрать 5 пластиковых бутылок, пройти пешком 1 км, выключить свет). Ответ должен быть СТРОГО 1-2 предложениями. Не пиши планы на неделю и неповторяй челеджи!"
        return self.receiving_answer_from_ai(context)

    def generation_quiz_question(self, topic: str = "")-> Optional[dict]:

        if topic == "":
            print("Error topic is nullptr\n")
            return None

        context = f"""Сгенерируй один вопрос для экологической викторины на тему "{topic}".
                    ВАЖНО: Ответ должен быть СТРОГО в формате JSON без лишних слов и markdown-разметки и не должен повторять прошлые вопросы.
                    Формат JSON:
                    {{
                        "question": "Текст вопроса",
                        "options": ["Вариант 1", "Вариант 2", "Вариант 3", "Вариант 4"],
                        "correct_index": 0,
                        "explanation": "Краткое пояснение, почему этот ответ правильный"
                    }}
                    """
        try:

            raw_answer = self.receiving_answer_from_ai(context)
            if not raw_answer:
                return None

            cleaned = re.sub(r'^```json\s*', '', raw_answer)
            cleaned = re.sub(r'\s*```$', '', cleaned)
            cleaned = cleaned.strip()

            question_data = json.loads(cleaned)

            if len(question_data.get("options", [])) != 4:
                print("error: ИИ вернул не 4 варианта ответа")
                return None

            return question_data

        except json.JSONDecodeError as e:
            print(f"error in AIServes|generation_quiz_question: JSON decode error: {e}")
            print(f"Raw answer: {raw_answer}")
            return None

        except Exception as e:
            print(f"error in AIServes|generation_quiz_question: {e}")
            return None


ai_service = AIServes()

if __name__ == "__main__":
    """""""""
    print("start\n")

    print("promt сгенерируй эко совет для майнкрафта\n")
    Answer = ai_service.receiving_answer_from_ai("сгенерируй эко совет для майнкрафта")

    if Answer:
        print(Answer)
    else:
        print("error\n")

    print("\n\n")
    print("Совет для бота \n")

    Answer = ai_service.generation_eco_advice()

    if Answer:
        print(Answer)
    else:
        print("error\n")

    print("\n\n")
    print("челлендж для бота \n")

    Answer = ai_service.generation_eco_challenge()

    if Answer:
        print(Answer)
    else:
        print("error\n")
        
    print("\n\n")
    """""""""""

    print("start check Quiz Ai integration\n")

    print('\n\n')
    print('Generation Quiz')
    quiz_question = ai_service.generation_quiz_question("Помощь природе")

    if quiz_question:
        print(quiz_question)
    else:
        print("error\n")