import requests
import logging
# import json

class ProductFetcher:
    
    def __init__(self, user_agent=None, proxy=None, logger=None, debug=False, city_id: int = 3):
        self.user_agent = user_agent or "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36"
        self.proxy = proxy
        self.logger = logger or logging.getLogger(__name__)
        self.debug = debug
        self.city_id = city_id
        self.headers = {
            'accept': 'application/json, text/plain, */*',
            'accept-language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
            'content-type': 'application/json',
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
            'x-key': 'bc84fec1c1b76b827965943d6dc04f1b',
            'x-language': 'ru',
        }

    def fetch_products(self, category, max_pages=None):
        products = []
        page = 1
        total_products = 0

        while True:
            params = {
                'page': str(page),
                'limit': '28', #!Имменно столько отдает API :-(
                'sort': 'sold',
            }

            json_data = {
                'category': category,
                'brand': [],
                'price': [],
                'isDividedPrice': False,
                'isNew': False,
                'isHit': False,
                'isSpecialPrice': False,
            }

            try:
                response = requests.post(
                    f'https://api.fix-price.com/buyer/v1/product/in/{category}',
                    params=params,
                    headers=self.headers,
                    json=json_data,
                    proxies={'https': self.proxy} if self.proxy else None
                )
                response.raise_for_status()
                data = response.json()

                if not data:
                    break

                products.extend(data)
                total_products += len(data)

                if self.debug and self.logger:
                    self.logger.info(f"Страница {page}: найдено {len(data)} товаров")

                if max_pages and page >= max_pages:
                    break

                page += 1

            except requests.exceptions.RequestException as e:
                if self.logger:
                    self.logger.error(f"Ошибка при запросе страницы {page}: {e}")
                break

        if self.debug and self.logger:
            self.logger.info(f"Всего найдено товаров: {total_products}")

        return products, total_products

if __name__ == "__main__":
    import logging
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)

    fetcher = ProductFetcher(
        logger=logger,
        debug=True,
        city_id=3
    )

    category = "vsye-po-35"
    #!Так как мы не знаем  число страниц хотя их и можно вычислить по количеству товаров в ответе от api (но там иногда не верные данные) мы выставляем 100 и оставляемваемся если пусто!
    products, total_products = fetcher.fetch_products(category, max_pages = 100)
    print(f"Всего найдено товаров: {total_products}")
    # print(json.dumps(products, indent=4, ensure_ascii=False))