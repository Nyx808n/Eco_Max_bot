"""
Модуль интеграции с Яндекс.Картами

"""

import requests
import webbrowser
import math
from typing import Tuple, Optional, Dict, List
import json


class YandexMapsIntegration:
    """
    Класс для работы с Яндекс.Картами 
    """
    
    def __init__(self, api_key: str = None):
        """
        Args:
            api_key (str): API ключ Яндекс.Карт
        """
        self.api_key = None
        self.base_url = "https://geocode-maps.yandex.ru/1.x/"
        self.maps_url = "https://yandex.ru/maps/"
        self.current_location = None
        
        # Получение текущей геолокации пользователя по IP. Словарь с информацией о местоположении
        
        try:
            # Используем сервис для определения местоположения по IP
            response = requests.get("http://ip-api.com/json/", timeout=5)
            if response.status_code == 200:
                data = response.json()
                self.current_location = {
                    'latitude': data['lat'],
                    'longitude': data['lon'],
                    'city': data['city'],
                    'country': data['country'],
                    'address': f"{data['city']}, {data['country']}"
                }
                print(f"Местоположение определено: {data['city']}, {data['country']}")
                return self.current_location
        except Exception as e:
            print(f"Ошибка получения геолокации: {e}")
        
        # Возвращаем дефолтное местоположение (Екб)
        return {
            'latitude': 56.8389,
            'longitude': 60.6057,
            'city': 'Екатеринбург',
            'country': 'Россия',
            'address': 'Екатеринбург, Россия'
        }
    
    def geocode_address(self, address: str) -> Optional[Dict]:
        """
        Определение координат по адресу
        
        Args:
            address (str): Адрес для геокодирования
            
        Returns:
            Dict: Координаты и информация о месте
        """
        try:
            params = {
                'apikey': self.api_key,
                'geocode': address,
                'format': 'json',
                'results': 1
            }
            
            response = requests.get(self.base_url, params=params, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                features = data.get('response', {}).get('GeoObjectCollection', {}).get('featureMember', [])
                
                if features:
                    geo_object = features[0]['GeoObject']
                    point = geo_object['Point']['pos']
                    lon, lat = map(float, point.split())
                    
                    result = {
                        'latitude': lat,
                        'longitude': lon,
                        'address': geo_object.get('name', address),
                        'full_address': geo_object.get('description', address)
                    }
                    
                    print(f"Адрес найден: {result['address']}")
                    return result
        except Exception as e:
            print(f"Ошибка геокодирования: {e}")
        
        print(f"Не удалось найти координаты для адреса: {address}")
        return None
    
    def reverse_geocode(self, lat: float, lon: float) -> Optional[str]:
        """
        Обратное геокодирование - определение адреса по координатам
        
        Args:
            lat (float): Широта
            lon (float): Долгота
            
        Returns:
            str: Адрес
        """
        try:
            params = {
                'apikey': self.api_key,
                'geocode': f'{lon},{lat}',
                'format': 'json',
                'results': 1,
                'sco': 'longlat'
            }
            
            response = requests.get(self.base_url, params=params, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                features = data.get('response', {}).get('GeoObjectCollection', {}).get('featureMember', [])
                
                if features:
                    return features[0]['GeoObject']['name']
        except Exception as e:
            print(f"Ошибка обратного геокодирования: {e}")
        
        return None
    
    def calculate_distance(self, point1: Tuple[float, float], 
                         point2: Tuple[float, float], 
                         method: str = 'haversine') -> float:
        """
        Расчет расстояния между двумя точками на карте
        
        Args:
            point1: Кортеж (широта, долгота) первой точки
            point2: Кортеж (широта, долгота) второй точки
            method: Метод расчета ('haversine' или 'euclidean')
            
        Returns:
            float: Расстояние в километрах
        """
        lat1, lon1 = point1
        lat2, lon2 = point2
        
        if method == 'haversine':
            # Формула Хаверсина для расчета расстояния на сфере
            R = 6371  # Радиус Земли в км
            
            lat1_rad = math.radians(lat1)
            lat2_rad = math.radians(lat2)
            delta_lat = math.radians(lat2 - lat1)
            delta_lon = math.radians(lon2 - lon1)
            
            a = (math.sin(delta_lat / 2) ** 2 + 
                 math.cos(lat1_rad) * math.cos(lat2_rad) * 
                 math.sin(delta_lon / 2) ** 2)
            c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
            
            distance = R * c
            
        elif method == 'euclidean':
            # Приближенное евклидово расстояние (для малых расстояний)
            lat_km = 111.32  # км в одном градусе широты
            lon_km = 111.32 * math.cos(math.radians((lat1 + lat2) / 2))
            
            delta_lat = lat2 - lat1
            delta_lon = lon2 - lon1
            
            distance = math.sqrt((delta_lat * lat_km) ** 2 + (delta_lon * lon_km) ** 2)
        else:
            raise ValueError(f"Неизвестный метод расчета: {method}")
        
        print(f"Расстояние между точками: {distance:.2f} км")
        return distance
    
    def create_map_link(self, points: List[Dict], 
                       center: Tuple[float, float] = None,
                       zoom: int = 15,
                       map_type: str = 'map') -> str:
        """
        Формирование ссылки на Яндекс.Карты с закрепленными точками
        
        Args:
            points: Список точек [{'lat': float, 'lon': float, 'name': str}]
            center: Центр карты (широта, долгота)
            zoom: Уровень масштабирования (1-19)
            map_type: Тип карты ('map', 'satellite', 'hybrid')
            
        Returns:
            str: URL ссылка на Яндекс.Карты
        """
        base_url = "https://yandex.ru/maps/"
        
        # Определяем центр карты
        if center is None and points:
            avg_lat = sum(p['lat'] for p in points) / len(points)
            avg_lon = sum(p['lon'] for p in points) / len(points)
            center = (avg_lat, avg_lon)
        elif center is None:
            center = (56.8389, 60.6057)  # Екб по умолчанию
        
        # Формируем параметры точек (метки)
        placemarks = []
        for i, point in enumerate(points):
            placemark = f"{point['lat']},{point['lon']}"
            if 'name' in point and point['name']:
                placemark += f",pm2rdm{i+1}"  # Метка с номером
            placemarks.append(placemark)
        
        # Базовые параметры
        params = f"?ll={center[1]},{center[0]}&z={zoom}"
        
        # Добавляем тип карты
        if map_type == 'satellite':
            params += "&l=sat"
        elif map_type == 'hybrid':
            params += "&l=sat,skl"
        
        # Добавляем метки
        if placemarks:
            params += f"&pt={'~'.join(placemarks)}"
        
        url = base_url + params
        print(f"Ссылка на карту создана: {url}")
        return url
    
    def create_route_link(self, start_point: Tuple[float, float],
                        end_point: Tuple[float, float],
                        waypoints: List[Tuple[float, float]] = None,
                        mode: str = 'auto') -> str:
        """
        Формирование ссылки на маршрут в Яндекс.Картах
        
        Args:
            start_point: Кортеж (широта, долгота) начальной точки
            end_point: Кортеж (широта, долгота) конечной точки
            waypoints: Список промежуточных точек
            mode: Режим передвижения ('auto', 'masstransit', 'pedestrian', 'bicycle')
            
        Returns:
            str: URL ссылка на маршрут
        """
        base_url = "https://yandex.ru/maps/"
        
        # Базовые координаты маршрута
        lat1, lon1 = start_point
        lat2, lon2 = end_point
        
        # Параметры маршрута
        route_params = f"{lat1},{lon1}~{lat2},{lon2}"
        
        # Добавляем промежуточные точки
        if waypoints:
            for wp in waypoints:
                route_params += f"~{wp[0]},{wp[1]}"
        
        # Определяем режим передвижения
        mode_param = {
            'auto': 'auto',
            'masstransit': 'mt',
            'pedestrian': 'pd',
            'bicycle': 'bc'
        }.get(mode, 'auto')
        
        url = f"{base_url}?rtext={route_params}&rtt={mode_param}"
        
        print(f"Ссылка на маршрут создана: {url}")
        return url
    
    def open_map_in_browser(self, url: str):
        """
        Открытие карты в браузере
        
        Args:
            url (str): URL для открытия
        """
        try:
            webbrowser.open(url)
            print(f"Карта открыта в браузере")
        except Exception as e:
            print(f"Ошибка открытия браузера: {e}")
    
    def find_places_nearby(self, lat: float, lon: float, 
                          place_type: str, radius: int = 1000) -> List[Dict]:
        """
        Поиск мест поблизости
        
        Args:
            lat (float): Широта
            lon (float): Долгота
            place_type (str): Тип места (metro, cafe, shop, etc.)
            radius (int): Радиус поиска в метрах
            
        Returns:
            List[Dict]: Список найденных мест
        """
        try:
            params = {
                'apikey': self.api_key,
                'geocode': f'{place_type}',
                'format': 'json',
                'results': 10,
                'll': f'{lon},{lat}',
                'spn': f'{radius/100000},{radius/100000}',
                'rspn': 1
            }
            
            response = requests.get(self.base_url, params=params, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                features = data.get('response', {}).get('GeoObjectCollection', {}).get('featureMember', [])
                
                places = []
                for feature in features:
                    geo_object = feature['GeoObject']
                    point = geo_object['Point']['pos']
                    place_lon, place_lat = map(float, point.split())
                    
                    # Рассчитываем расстояние до места
                    distance = self.calculate_distance(
                        (lat, lon), 
                        (place_lat, place_lon)
                    )
                    
                    if distance <= radius / 1000:  # Конвертируем метры в км
                        places.append({
                            'name': geo_object.get('name', 'Неизвестно'),
                            'latitude': place_lat,
                            'longitude': place_lon,
                            'distance': distance,
                            'address': geo_object.get('description', '')
                        })
                
                return sorted(places, key=lambda x: x['distance'])
                
        except Exception as e:
            print(f"Ошибка поиска мест: {e}")
        
        return []
    
    def get_building_info(self, lat: float, lon: float) -> Dict:
        """
        Получение информации о здании по координатам
        
        Args:
            lat (float): Широта
            lon (float): Долгота
            
        Returns:
            Dict: Информация о здании
        """
        try:
            params = {
                'apikey': self.api_key,
                'geocode': f'{lon},{lat}',
                'format': 'json',
                'results': 1,
                'sco': 'longlat',
                'kind': 'house'
            }
            
            response = requests.get(self.base_url, params=params, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                features = data.get('response', {}).get('GeoObjectCollection', {}).get('featureMember', [])
                
                if features:
                    geo_object = features[0]['GeoObject']
                    metadata = geo_object.get('metaDataProperty', {}).get('GeocoderMetaData', {})
                    
                    return {
                        'address': geo_object.get('name', ''),
                        'full_address': geo_object.get('description', ''),
                        'postal_code': metadata.get('Address', {}).get('postal_code', ''),
                        'building_type': metadata.get('kind', ''),
                        'precision': metadata.get('precision', '')
                    }
        except Exception as e:
            print(f"Ошибка получения информации о здании: {e}")
        
        return {}


# Пример использования в MaxScript через Python
"""
def maxscript_example():
    
    Пример использования модуля в контексте Max
    
    maps = YandexMapsIntegration(api_key="YOUR_API_KEY_HERE")
    
    # 1. Получаем текущее местоположение
    location = maps.get_current_location()
    print(f"Текущее местоположение: {location}")
    
    # 2. Геокодируем адрес
    point_a = maps.geocode_address("Екатеринбург, Площадь 1905 года")
    point_b = maps.geocode_address("Екатеринбург, Ельцин Центр")
    
    if point_a and point_b:
        # 3. Рассчитываем расстояние
        distance = maps.calculate_distance(
            (point_a['latitude'], point_a['longitude']),
            (point_b['latitude'], point_b['longitude'])
        )
        
        # 4. Создаем ссылку на карту с метками
        points = [
            {'lat': point_a['latitude'], 'lon': point_a['longitude'], 'name': 'Площадь 1905 года'},
            {'lat': point_b['latitude'], 'lon': point_b['longitude'], 'name': 'Ельцин Центр'}
        ]
        map_link = maps.create_map_link(points)
        
        # 5. Создаем ссылку на маршрут
        route_link = maps.create_route_link(
            (point_a['latitude'], point_a['longitude']),
            (point_b['latitude'], point_b['longitude'])
        )
        
        # 6. Открываем в браузере
        maps.open_map_in_browser(route_link)
        
        # 7. Ищем ближайшие метро
        metro_stations = maps.find_places_nearby(
            point_a['latitude'], 
            point_a['longitude'], 
            'метро', 
            500
        )
        print(f"Ближайшие станции метро: {metro_stations}")


# MaxScript интерфейс для использования в 3ds Max
MAXSCRIPT_INTERFACE = 
-- Пример MaxScript кода для вызова Python модуля
(
    python.Execute "from yandex_maps_integration import YandexMapsIntegration"
    python.Execute "maps = YandexMapsIntegration(api_key='YOUR_API_KEY')"
    
    -- Получить координаты текущего объекта в сцене
    local obj = selection[1]
    if obj != undefined then
    (
        local pos = obj.pos
        
        -- Создать ссылку на местоположение объекта
        python.Execute ("link = maps.create_map_link([{'lat': " + 
            pos.y as string + ", 'lon': " + pos.x as string + "}])")
        python.Execute "maps.open_map_in_browser(link)"
    )
)


if __name__ == "__main__":
    # Тестирование модуля
    maxscript_example()
"""