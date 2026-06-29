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


ai_service = AIServes()

if __name__ == "__main__":
    print("start")

    Answer = ai_service.ReceivingAnswerFromAi("сгенерируй совет для эко дня")

    if Answer:
        print(Answer)
    else:
        print("error")