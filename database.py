from sqlalchemy import create_engine, Column, BigInteger, String, Boolean, Integer, Float
from sqlalchemy.orm import sessionmaker, DeclarativeBase
from config import settings

engine = create_engine(settings.database_url)

class Base(DeclarativeBase):
    pass

Session = sessionmaker(bind=engine)

class User(Base):
    __tablename__ = "users"

    user_id = Column(BigInteger, primary_key=True, index=True) # ID из MAX
    username = Column(String, nullable=True)                   # Имя пользователя
    is_consent_pd = Column(Boolean, default=False)             # Согласие на обработку ПД
    quiz_points = Column(Integer, default=0)                   # Баллы викторины
    challenge_points = Column(Integer, default=0)              # Баллы челеджи

class RecyclingPoint(Base):
    """Таблица пунктов приема отходов"""
    __tablename__ = "recycling_points"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String, nullable=False)                      # Название пункта
    address = Column(String, nullable=False)                   # Адрес
    latitude = Column(Float, nullable=False)                   # Широта
    longitude = Column(Float, nullable=False)                  # Долгота
    waste_types = Column(String, nullable=False)               # Типы отходов (например: "пластик, стекло")
    schedule = Column(String, nullable=True)                   # Режим работы

    """Взаимодействие с бд"""

def init_db():
    """Создает таблицы в базе данных, если их еще нет"""
    Base.metadata.create_all(bind=engine)
    print("Database initialized")

def get_db_session():
    """Возвращает новую сессию для работы с БД"""
    return Session()

def create_user(user_id: int, username: str):
    """Создание пользователя в бд"""
    db = get_db_session()
    try:
        existing_user = db.query(User).filter(User.user_id == user_id).first()
        if existing_user:
            return existing_user  # Если пользователь то возвращаем его

        # Если нет создаем нового
        new_user = User(user_id=user_id, username=username, is_consent_pd=True)
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        return new_user
    finally:
        db.close()

def get_user(user_id: int):
    """Получает пользователя по ID"""
    db = get_db_session()
    try:
        return db.query(User).filter(User.user_id == user_id).first()
    finally:
        db.close()

def update_user_quiz_points(user_id: int, quiz_points_to_add: int):
    """Добавляет баллы пользователю викторин"""
    db = get_db_session()
    try:
        user = db.query(User).filter(User.user_id == user_id).first()
        if user:
            user.quiz_points += quiz_points_to_add
            db.commit()
            return True
        return False
    finally:
        db.close()

def update_user_challenge_points(user_id: int, challenge_points_to_add: int):
    """Добавляет баллы пользователю челеджи"""
    db = get_db_session()
    try:
        user = db.query(User).filter(User.user_id == user_id).first()
        if user:
            user.challenge_points += challenge_points_to_add
            db.commit()
            return True
        return False
    finally:
        db.close()

if __name__ == "__main__":
    print("DB test start\n")
    init_db()
    print("Creating user\n")
    test_user = create_user(user_id=123456789, username="TestUser_Eco")
    print(f"Find and Creating user with ID={test_user.user_id}, name = {test_user.username}, quiz_points = {test_user.quiz_points}, challenge_points = {test_user.challenge_points}")