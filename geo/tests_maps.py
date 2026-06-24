# test_maps.py
from geo import YandexMapsIntegration
import time

def test_all_functions():
    """
    Тестирование всех функций модуля
    """
    print("=" * 60)
    print("ТЕСТИРОВАНИЕ МОДУЛЯ ИНТЕГРАЦИИ С ЯНДЕКС.КАРТАМИ")
    print("=" * 60)
    
    # Создаем экземпляр класса
    maps = YandexMapsIntegration()
    
    # Тест 1: Определение местоположения
    print("\n ТЕСТ 1: Определение текущего местоположения")
    print("-" * 40)
    location = maps.get_current_location()
    print(f"Результат: {location}")
    time.sleep(1)
    
    # Тест 2: Геокодирование адреса
    print("\n ТЕСТ 2: Поиск координат по адресу")
    print("-" * 40)
    
    # Тест с адресом в Екатеринбурге (без API ключа)
    print("\n2.1 Поиск без API ключа:")
    point_a = maps.geocode_address("Екатеринбург, Площадь 1905 года")
    if point_a:
        print(f"Координаты: {point_a['latitude']}, {point_a['longitude']}")
    
    time.sleep(1)
    
    # Тест 3: Расчет расстояния
    print("\n ТЕСТ 3: Расчет расстояния между точками")
    print("-" * 40)
    
    # Используем известные координаты
    ekb_center = (56.8389, 60.6057)  # Центр Екатеринбурга
    ekb_viz = (56.8500, 60.5500)     # ВИЗ-бульвар
    
    distance = maps.calculate_distance(ekb_center, ekb_viz)
    print(f"Расстояние от Площади 1905 года до ВИЗ-бульвара: {distance:.2f} км")
    
    # Дополнительные расчеты
    print("\nДополнительные расчеты расстояний:")
    
    # Москва - Санкт-Петербург
    moscow = (55.7558, 37.6173)
    spb = (59.9343, 30.3351)
    dist_msk_spb = maps.calculate_distance(moscow, spb)
    print(f"Москва - Санкт-Петербург: {dist_msk_spb:.2f} км")
    
    # Екатеринбург - Москва
    dist_ekb_msk = maps.calculate_distance(ekb_center, moscow)
    print(f"Екатеринбург - Москва: {dist_ekb_msk:.2f} км")
    
    time.sleep(1)
    
    # Тест 4: Создание ссылки на карту
    print("\n ТЕСТ 4: Создание ссылки на карту с метками")
    print("-" * 40)
    
    points = [
        {'lat': 56.8389, 'lon': 60.6057, 'name': 'Площадь 1905 года'},
        {'lat': 56.8370, 'lon': 60.5970, 'name': 'Плотинка'},
        {'lat': 56.8500, 'lon': 60.5500, 'name': 'ВИЗ-бульвар'}
    ]
    
    map_link = maps.create_map_link(points, zoom=14)
    print(f"Ссылка на карту: {map_link}")
    
    time.sleep(1)
    
    # Тест 5: Создание маршрута
    print("\n ТЕСТ 5: Создание маршрута")
    print("-" * 40)
    
    # Маршрут по центру Екатеринбурга
    start = (56.8389, 60.6057)  # Площадь 1905 года
    end = (56.8370, 60.5970)     # Плотинка
    
    # Автомобильный маршрут
    route_auto = maps.create_route_link(start, end, mode='auto')
    print(f"Автомобильный маршрут: {route_auto}")
    
    # Пешеходный маршрут
    route_walk = maps.create_route_link(start, end, mode='pedestrian')
    print(f"Пешеходный маршрут: {route_walk}")
    
    time.sleep(1)
    
    # Тест 6: Открытие карты в браузере (спросим пользователя)
    print("\n ТЕСТ 6: Открытие карты в браузере")
    print("-" * 40)
    choice = input("Открыть карту с маршрутом в браузере? (y/n): ").lower()
    if choice == 'y':
        maps.open_map_in_browser(route_auto)
    else:
        print("Пропущено")
    
    # Сводка результатов
    print("\n" + "=" * 60)
    print(" ТЕСТИРОВАНИЕ ЗАВЕРШЕНО")
    print("=" * 60)
    print("\nПроверенные функции:")
    print("Определение местоположения")
    print("Геокодирование адресов")
    print("Расчет расстояний")
    print("Создание ссылок на карту")
    print("Создание маршрутов")
    print("Открытие карты в браузере")
    print("\nПримечание: Для полного функционала геокодирования")
    print("требуется API ключ Яндекс.Карт")

if __name__ == "__main__":
    try:
        test_all_functions()
    except KeyboardInterrupt:
        print("\n\n Тестирование прервано пользователем")
    except Exception as e:
        print(f"\n Ошибка при тестировании: {e}")