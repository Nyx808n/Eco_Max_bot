from config import settings
from gigachat import GigaChat

from typing import Optional

print("1")
giga = GigaChat(
    credentials=f"{settings.GIGACHAT_AUTH_KEY}",
    verify_ssl_certs=False
)

class AIServes:
    """Работа с гигачатом"""

    def __init__(self):
        self.giga = GigaChat(
            credentials=f"{settings.GIGACHAT_AUTH_KEY}",
            verify_ssl_certs=False
        )

    def ReceivingAnswerFromAi(self, contex: str = "") -> Optional[str]:
        if contex == "":
            return "contex input is nullptr"

        try:
            response = self.giga.chat(contex)
            return response.choices[0].message.content
        except:
            print("error in AIServes|ReceivingAnswerFromAi")
            return None

    def GenerationEcoAdvice(self)-> Optional[str]:
        contex = "Сгенерируй интересный эко совет не поврторяя прошлые" #then edit promt
        return self.ReceivingAnswerFromAi(contex)
    



ai_service = AIServes()

if __name__ == "__main__":
    print("start\n")

    print("promt сгенерируй эко совет для майнкрафта\n")
    Answer = ai_service.ReceivingAnswerFromAi("сгенерируй эко совет для майнкрафта")

    if Answer:
        print(Answer)
    else:
        print("error\n")

    print("\n\n")
    print("Совет для бота \n")

    Answer = ai_service.GenerationEcoAdvice()

    if Answer:
        print(Answer)
    else:
        print("error\n")