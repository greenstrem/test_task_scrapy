import requests
import json

#?titlePart=&sort=head
url = 'https://api.fix-price.com/buyer/v1/location/city'

response = requests.get(url)

if response.status_code == 200:
    cities = response.json()
    
    print("Полный ответ:")
    print(json.dumps(cities, indent=4))
    
    print("\nСписок городов:")
    for city in cities:
        print(f"ID: {city['id']}, Название: {city['name']}")
else:
    print(f"Ошибка при запросе: {response.status_code}")


