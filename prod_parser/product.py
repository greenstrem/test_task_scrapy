import json
import os
import random
from datetime import datetime


class ProductSaver:
    """
    Класс для сохранения данных о товарах в формате JSON.
    В качестве имени файла используется название продукта и случайное число.
    """

    def __init__(self, output_dir="out"):
        self.output_dir = output_dir
        os.makedirs(self.output_dir, exist_ok=True)

    def save_products(self, settings, products):
        """
        Сохраняет данные о товарах в JSON-файл.

        Args:
            settings (dict): Словарь с настройками. Пример:
                {
                    "region": "Екатеринбург",  # Регион для парсинга.
                    "timestamp": int,  # Временная метка создания данных.
                    "category": "Косметика и гигиена"  # Категория товаров.
                }
            products (list): Список словарей с данными о товарах. Каждый словарь соответствует одному товару.
        """
        for product_data in products:
            try:
                # Извлекаем название продукта
                product_name = product_data.get("title", "unknown_product")
                # Генерируем случайное число
                random_number = random.randint(1000, 9999)
                # Формируем имя файла
                filename = f"{product_name}_{random_number}.json"
                # Убираем запрещенные символы в имени файла
                filename = "".join(c for c in filename if c.isalnum() or c in (' ', '.', '_')).rstrip()
                filepath = os.path.join(self.output_dir, filename)

                # Сохраняем данные в файл
                with open(filepath, "w", encoding="utf-8") as f:
                    json.dump([product_data], f, ensure_ascii=False, indent=4)

                print(f"💾 Данные успешно сохранены в файл: {filepath}")
            except Exception as e:
                print(f"❌ Ошибка при сохранении товара {product_name}: {e}")




if __name__ == "__main__":
    settings = {
        "region": "Екатеринбург",
        "timestamp": 1698765432,
        "category": "Косметика и гигиена"
    }

    products = [
        {
            "timestamp": 1698765432,
            "RPC": "12345",
            "url": "https://fix-price.com/product/12345",
            "title": "Пирожное рисовое Моти, 120 г",
            "marketing_tags": ["Популярный", "Акция"],
            "brand": "Moti",
            "section": ["Продукты", "Десерты"],
            "price_data": {
                "current": 99.99,
                "original": 120.00,
                "sale_tag": "Скидка 17%"
            },
            "stock": {
                "in_stock": True,
                "count": 10
            },
            "assets": {
                "main_image": "https://fix-price.com/image1.jpg",
                "set_images": ["https://fix-price.com/image1.jpg", "https://fix-price.com/image2.jpg"],
                "view360": [],
                "video": []
            },
            "metadata": {
                "__description": "Пирожное рисовое Моти – это традиционный японский десерт...",
                "Вес": "120 г",
                "Страна производства": "Китай"
            },
            "variants": 2
        }
    ]

    saver = ProductSaver()
    saver.save_products(settings, products)