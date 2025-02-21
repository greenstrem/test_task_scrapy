import requests
import json
import logging

class CategoryFetcher:
    def __init__(self,
                 city_id,
                 user_agent=None,
                 proxy=None,
                 logger=None,
                 debug=False,
                 nested_categories=False,  
                 save_response=False):  
        
        self.user_agent = user_agent or "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36"
        self.proxy = proxy
        self.logger = logger or logging.getLogger(__name__)
        self.debug = debug
        self.city_id = city_id
        self.nested_categories = nested_categories  #!Флаг для двухуровневой структуры
        self.save_response = save_response  #!Флаг для сохранения ответа
        self.headers = {
            'accept': 'application/json, text/plain, */*',
            'accept-language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
            'origin': 'https://fix-price.com',
            'priority': 'u=1, i',
            'referer': 'https://fix-price.com/',
            'sec-ch-ua': '"Not(A:Brand";v="99", "Google Chrome";v="133", "Chromium";v="133"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-site',
            'user-agent': self.user_agent,
            'x-city': str(self.city_id),
            'x-delivery-type': 'store',
            'x-key': 'bc84fec1c1b76b827965943d6dc04f1b',
            'x-language': 'ru',
            'x-pfm': '5528',
        }

    def fetch_categories(self):
        url = 'https://api.fix-price.com/buyer/v1/category/menu'
        proxies = {'https': self.proxy} if self.proxy else None

        try:
            response = requests.get(url, headers=self.headers, proxies=proxies)
            response.raise_for_status()
            categories = response.json()

            if self.save_response:
                self._save_response(categories)

            if self.debug:
                if self.logger:
                    self.logger.info("Полный ответ:\n%s", json.dumps(categories, indent=4))
                    self.logger.info("\nСписок категорий:")

            category_data = self._extract_category_data(categories)
            return category_data

        except requests.exceptions.RequestException as e:
            if self.logger:
                self.logger.error(f"Ошибка при запросе: {e}")
            return None

    def _extract_category_data(self, categories):
        result = []

        for category in categories:
            category_info = {
                "title": category["title"],
                "url": category["url"],
            }

            if self.nested_categories and category.get("items"):
                category_info["items"] = self._extract_category_data(category["items"])

            result.append(category_info)

            if self.debug and self.logger:
                self.logger.info(f"Категория: {category_info['title']}, Товаров: {category_info['productCount']}")

        return result

    def _save_response(self, data):
        """
        Сохраняет ответ от API в файл test.json с отступами и кодировкой UTF-8!
        """
        try:
            with open("test.json", "w", encoding="utf-8") as f:
                json.dump(data, f, indent=4, ensure_ascii=False)
            if self.logger:
                self.logger.info("Ответ от API сохранен в файл test.json")
        except Exception as e:
            if self.logger:
                self.logger.error(f"Ошибка при сохранении ответа: {e}")

if __name__ == "__main__":
    import logging
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)

    fetcher = CategoryFetcher(
        logger=logger,
        debug=False,
        city_id=3,
        nested_categories=True,
        save_response=False
    )

    categories = fetcher.fetch_categories()
    if categories:
        # print(json.dumps(categories, indent=4, ensure_ascii=False))

        with open("cat_list.json", "w", encoding="utf-8") as f:
            json.dump(categories, f, ensure_ascii=False, indent=4)