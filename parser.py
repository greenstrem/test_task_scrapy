import logging
import os
from time import sleep
from datetime import datetime
from config_manager import ConfigManager
from get_prod_list import ProductFetcher
from prod_parser import description_parser, product
import random

class Parser:
    def __init__(self):
        self.config_manager = ConfigManager("config.json")
        self._setup_logger()
        self.proxy_enabled = self.config_manager.get("proxy", {}).get("enabled", False)
        self.proxy_list = self.config_manager.get("proxy", {}).get("list", [])
        self.max_threads = self.config_manager.get("concurrency", {}).get("max_threads", 8)
        self.delay = self.config_manager.get("concurrency", {}).get("delay", 2)
        self.retries = self.config_manager.get("concurrency", {}).get("retries", 3)
        self.user_agent = self.config_manager.get("user_agent")
        self.city_id = self.config_manager.get_city_id()
        self.region_name = self.config_manager.get("reg_name")
        self.cat_list = self.config_manager.get_categories()

    def _setup_logger(self):
        if not os.path.exists("logs"):
            os.makedirs("logs")
        log_file = f"logs/parser_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"
        logging.basicConfig(
            level=logging.INFO,
            format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
            handlers=[
                logging.FileHandler(log_file, encoding="utf-8"),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger(__name__)

    def _get_proxy(self):
        if self.proxy_enabled and self.proxy_list:
            return self.proxy_list.pop(0)
        return None

    def _fetch_products(self):
        prod_list = []
        for cat in self.cat_list:
            self.logger.info(f"🚀 Начинаю парсинг категории: {cat}")
            fetcher = ProductFetcher(logger=self.logger, city_id=self.city_id, user_agent=self.user_agent)
            products, total_products = fetcher.fetch_products(cat, max_pages=100)
            prod_list.extend(products)
            self.logger.info(f"✅ Получил {total_products} товаров из категории {cat}")
            self.logger.info(f"😴 Сплю {self.delay} секунды между получением данных из категории")
            sleep(self.delay)
        return prod_list

    def _parse_and_save_products(self, prod_list):
        for prod in prod_list:
            try:
                self.logger.info(f"🔄 Обрабатываю товар: {prod['title']}")
                descript = description_parser.get_description(url=f"https://fix-price.com/catalog/{prod['url']}")
                self.logger.info(f"📝 Описание товара получено: {prod['title']}")

                product_data = {
                    "timestamp": int(datetime.now().timestamp()),
                    "RPC": str(prod['id']),
                    "url": f"https://fix-price.com/catalog/{prod['url']}",
                    "title": prod['title'],
                    "marketing_tags": [],
                    "brand": prod['brand']['title'],
                    "section": [prod['category']['title']],
                    "price_data": {
                        "current": float(prod['price']),
                        "original": float(prod['price']),
                        "sale_tag": ""
                    },
                    "stock": {
                        "in_stock": prod['inStock'] > 0,
                        "count": prod['inStock']
                    },
                    "assets": {
                        "main_image": prod['images'][0]['src'] if prod['images'] else "",
                        "set_images": [img['src'] for img in prod['images']],
                        "view360": [],
                        "video": []
                    },
                    "metadata": {
                        "__description": descript['description'],
                        "Код товара": prod['sku'],
                        "Вес, гр.": descript['properties'].get('Вес, гр.', ''),
                        "Страна производства": descript['properties'].get('Страна производства', '')
                    },
                    "variants": prod['variantCount']
                }

                settings = {
                    "region": self.region_name,
                    "timestamp": int(datetime.now().timestamp()),
                    "category": prod['category']['title']
                }

                saver = product.ProductSaver()
                saver.save_products(settings, [product_data])
                self.logger.info(f"💾 Сохранен товар: {prod['title']}")

            except Exception as e:
                self.logger.error(f"❌ Ошибка при обработке товара {prod['title']}: {e}")
                continue  

            self.logger.info(f"😴 Сплю {self.delay} секунды перед следующим товаром")
            sleep(random.uniform(2, 10)) #TODO! Сделать нормальный сон!

    def run(self):
        self.logger.info("🛠️ Запуск парсера")
        prod_list = self._fetch_products()
        self._parse_and_save_products(prod_list)
        self.logger.info("🏁 Парсинг завершен")


