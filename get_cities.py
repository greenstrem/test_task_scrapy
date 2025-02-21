import requests
import json

class CityFetcher:
    def __init__(self, user_agent=None, 
                 proxy=None, 
                 logger=None, 
                 all_cities = True, 
                 debug = False
                 ):
        
        self.user_agent = user_agent or "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        self.proxy = proxy
        self.logger = logger or logging.getLogger(__name__)
        self.all_cities = all_cities
        self.debug = debug

    def fetch_cities(self):
        url = "https://api.fix-price.com/buyer/v1/location/city" if self.all_cities \
            else "https://api.fix-price.com/buyer/v1/location/city?titlePart=&sort=head"
        
        headers = {'User-Agent': self.user_agent}
        proxies = {'https': self.proxy} if self.proxy else None

        try:
            response = requests.get(url, headers=headers, proxies=proxies)
            response.raise_for_status()
            cities = response.json()
            
            if self.debug and self.logger:
                self.logger.info("Полный ответ:\n%s", json.dumps(cities, indent=4))
                self.logger.info("\nСписок городов:")
                for city in cities:
                    self.logger.info(f"ID: {city['id']}, Название: {city['name']}")

            cleaned_cities = [{"id": city["id"], "name": city["name"]} for city in cities]

            with open("cities.json", "w", encoding="utf-8") as f:
                json.dump(cleaned_cities, f, indent=4, ensure_ascii=False)

            return cleaned_cities

        except requests.exceptions.RequestException as e:
            if self.logger:
                self.logger.error(f"Ошибка при запросе: {e}")
            return None


if __name__ == "__main__":
    import logging
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)

    fetcher = CityFetcher(
        logger=logger,
        all_cities = True
    )

    cities = fetcher.fetch_cities()
    # if cities:
        # print(json.dumps(cities, indent=4, ensure_ascii=False).encode('utf-8').decode('utf-8'))