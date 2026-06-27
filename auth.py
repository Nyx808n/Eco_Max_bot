from dataclasses import dataclass
from typing import Optional
from database import get_user, create_user, User

@dataclass
class AuthResult:
    """Результат авторизации пользователя"""
    user_id: int                    # ID пользователя из MAX
    username: str                   # Имя пользователя
    is_registered: bool             # Статус регистрации
    message: str                    # Сообщение для вывода пользователю
    user: Optional[User] = None     # Объект пользователя из БД (если есть)

def authorize(user_id: int, username: str, consent_pd: bool) -> AuthResult:
    existing_user = get_user(user_id)

    if existing_user:
        # Если есть в бд возвращаем его
        return AuthResult(
            user_id=existing_user.user_id,
            username=existing_user.username or username,
            is_registered=True,
            message="Вы вошли в акаунт", # Мб надо
            user=existing_user
        )

    if not consent_pd:
        # Согласия нет — отказываем в регистрации
        return AuthResult(
            user_id=user_id,
            username=username,
            is_registered=False,
            message="Для регестации нужно дать согласие на обработку ПД",
            user=None
        )

    new_user = create_user(user_id=user_id, username=username)

    return AuthResult(
        user_id=new_user.user_id,
        username=new_user.username,
        is_registered=True,
        message="Вы успешено зарегестрировались",
        user=new_user
    )


def check_registration_status(user_id: int) -> bool:
    user = get_user(user_id)
    return user is not None


if __name__ == "__main__":
    print("Start auth\n")

    result1 = authorize(user_id=111222333, username="NewUser_Eco", consent_pd=True)
    print(f"  ID: {result1.user_id}")
    print(f"  Имя: {result1.username}")
    print(f"  Зарегистрирован: {result1.is_registered}")
    print(f"  Сообщение: {result1.message}\n\n")

    result2 = authorize(user_id=111222333, username="NewUser_Eco", consent_pd=True)
    print(f"  Сообщение: {result2.message}\n\n")

    result3 = authorize(user_id=444555666, username="NoConsentUser", consent_pd=False)
    print(f"  Зарегистрирован: {result3.is_registered}")
    print(f"  Сообщение: {result3.message}\n\n")

    status1 = check_registration_status(user_id=111222333)
    status2 = check_registration_status(user_id=999888777)
    print(f"  Пользователь 111222333 зарегистрирован: {status1}")
    print(f"  Пользователь 999888777 зарегистрирован: {status2}")