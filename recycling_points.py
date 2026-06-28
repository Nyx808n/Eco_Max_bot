from typing import List, Optional
from database import get_db_session, RecyclingPoint

"""
Мб это надо
"""

def find_points_by_waste_type(waste_type: str) -> List[RecyclingPoint]:
    """
    Поиск пунктов приёма по типу отходов
    """
    db = get_db_session()
    try:
        points = db.query(RecyclingPoint).filter(
            RecyclingPoint.waste_types.ilike(f"%{waste_type}%") #тип мусора
        ).all()
        return points
    finally:
        db.close()

def find_points_by_name(name: str) -> List[RecyclingPoint]:
    """
    Поиск пунктов приёма по названию или адресу
    """
    db = get_db_session()
    try:
        points = db.query(RecyclingPoint).filter(
            RecyclingPoint.name.ilike(f"%{name}%")
        ).all()
        return points
    finally:
        db.close()

def get_all_points() -> List[RecyclingPoint]:
    """
    Получение всех пунктов приёма
    """
    db = get_db_session()
    try:
        return db.query(RecyclingPoint).all()
    finally:
        db.close()


def format_point_info(point: RecyclingPoint) -> str:
    """
    Форматирование информации о пункте в читаемый текст для пользователя
    """
    text = f"{point.name}\n"
    text += f"Адрес: {point.address}\n"
    text += f"Принимает: {point.waste_types}\n"

    if point.schedule:
        text += f"Режим работы: {point.schedule}\n"

    text += f" Координаты: {point.latitude}, {point.longitude}\n"
    text += "-" * 30
    return text


if __name__ == "__main__":
    print("Запуск проверки recycling_points.py\n")

    db = get_db_session()
    try:
        if db.query(RecyclingPoint).count() == 0:
            print("")
            test_points = [
                RecyclingPoint(
                    name="ЭкоПункт №1",
                    address="ул. Ленина, 50",
                    latitude=56.8389, longitude=60.6057,
                    waste_types="пластик, стекло, бумага",
                    schedule="Пн-Пт 09:00-18:00"
                ),
                RecyclingPoint(
                    name="СдайБатарейку",
                    address="пр. Космонавтов, 10",
                    latitude=56.8500, longitude=60.5500,
                    waste_types="батарейки, аккумуляторы",
                    schedule="Ежедневно 10:00-20:00"
                ),
                RecyclingPoint(
                    name="ВторСырьё Центр",
                    address="ул. 8 Марта, 15",
                    latitude=56.8370, longitude=60.5970,
                    waste_types="пластик, металл, бумага",
                    schedule="Пн-Сб 08:00-17:00"
                )
            ]
            db.add_all(test_points)
            db.commit()
            print("+ места\n")
        else:
            print("места есть\n")

        print("поиск пластика\n")
        plastic_points = find_points_by_waste_type("пластик")
        if plastic_points:
            for p in plastic_points:
                print(format_point_info(p))
        else:
            print("Пункты не найдены\n")

        print("поиск батарейки\n")
        battery_points = find_points_by_waste_type("батарейки")
        if battery_points:
            for p in battery_points:
                print(format_point_info(p))
        else:
            print("Пункты не найдены\n")

        print("Эко названия")
        eco_points = find_points_by_name("Эко")
        if eco_points:
            for p in eco_points:
                print(format_point_info(p))
        else:
            print("Пункты не найдены\n")

    finally:
        db.close()