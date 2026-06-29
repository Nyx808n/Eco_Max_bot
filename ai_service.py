from config import settings
from gigachat import GigaChat

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
    

if __name__ == "__main__":

    response = giga.chat("напиши короткий эко совет")
    #response = giga.get_token()
    answer = response.choices[0].message.content
    print("2")
    print(answer)

    print("3")