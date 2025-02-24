import logging
import os
from time import sleep
from datetime import datetime
from config_manager import ConfigManager
from get_prod_list import ProductFetcher
from prod_parser import description_parser, product
import random
import concurrent.futures
import json


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
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.INFO)
        formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
        file_handler = logging.FileHandler(log_file, encoding="utf-8")
        file_handler.setFormatter(formatter)
        stream_handler = logging.StreamHandler()
        stream_handler.setFormatter(formatter)
        self.logger.addHandler(file_handler)
        self.logger.addHandler(stream_handler)
        self.logger.info("✅ Логгер успешно настроен и готов к работе! ✅")



    # def __random_sleep(rezone_to_sleep):
    #     sleep(random.uniform(2, 10)) #TODO! Сделать нормальный сон!

        

    def _fetch_products(self):
        prod_list = []
        
        if self.cat_list is None:
            self.logger.info(
                "⚙️ Категории не заданы начинаю парсинг ВСЕХ категорий из файла cat_list.json"
                )
    
            with open('cat_list.json', 'r', encoding='utf-8') as file:
                self.cat_list = [item['url'] for item in json.load(file)]
        
        for cat in self.cat_list:
            self.logger.info(f"🚀 Начинаю парсинг категории: {cat}")
            fetcher = ProductFetcher(logger=self.logger, 
                                    city_id=self.city_id, 
                                    user_agent=self.user_agent
                                    )
            products, total_products = fetcher.fetch_products(cat, max_pages=100)
            prod_list.extend(products)
            self.logger.info(f"✅ Получил {total_products} товаров из категории {cat}")
            self.logger.info(
                f"😴 Сплю {self.delay} секунды между получением данных из категории")
            
            sleep(self.delay)
        
        return prod_list




    def _parse_product_data(self, prod):
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

            return settings, product_data

        except Exception as e:
            self.logger.error(f"❌ Ошибка при обработке товара {prod['title']}: {e}")
            return None, None

    def _save_product_data(self, settings, product_data):
        """Сохранение данных товара"""
        try:
            saver = product.ProductSaver()
            saver.save_products(settings, [product_data])
            self.logger.info(f"💾 Сохранен товар: {product_data['title']}")
        except Exception as e:
            self.logger.error(f"❌ Ошибка при сохранении товара {product_data['title']}: {e}")

    def _process_product(self, prod):
        """Обработка одного товара для много поток"""
        settings, product_data = self._parse_product_data(prod)
        if settings and product_data:
            self._save_product_data(settings, product_data)

    def _parse_and_save_products(self, prod_list):
        """Основная функция для обработки списка товаров"""
        with concurrent.futures.ThreadPoolExecutor(max_workers=self.max_threads) as executor:
            futures = [executor.submit(self._process_product, prod) for prod in prod_list]
            for future in concurrent.futures.as_completed(futures):
                try:
                    future.result()
                except Exception as e:
                    self.logger.error(f"❌ Ошибка в потоке: {e}")
        slp = random.uniform(2, 10)
        self.logger.info(f"😴 Сплю {slp} секунды перед следующим товаром")
        sleep(slp) #TODO! Сделать нормальный сон!

    def run(self):
        self.logger.info("🛠️ Запуск парсера")
        prod_list = self._fetch_products()
        self._parse_and_save_products(prod_list)
        self.logger.info("🏁 Парсинг завершен")


