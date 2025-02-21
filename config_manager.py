import json
import os

class ConfigManager:
    def __init__(self, config_file):
        self.config_file = config_file
        self._load_config()

    def _load_config(self):
        #TODO: Вот тут бы блин было бы круто авто создание конфига из шаблона НО на это не хватило времени :с 
        if not os.path.exists(self.config_file):
            raise FileNotFoundError(f"Конфигурационный файл '{self.config_file}' не найден.")
        
        with open(self.config_file, 'r', encoding='utf-8') as file:
            self.config = json.load(file)

    def get(self, key, default=None):
        """Получает значение по ключу из конфигурации.

        Args:
            key (str): Ключ для получения значения.
            default: Значение по умолчанию, если ключ не найден.

        Returns:
            Значение по ключу или значение по умолчанию.
        """
        return self.config.get(key, default)

    def get_city_id(self):
        return self.get("city_id")

    def get_categories(self):
        return self.get("categories", [])

    def get_proxy(self):
        return self.get("proxy", {})

    def get_concurrency(self):
        return self.get("concurrency", {})

    def get_user_agent(self):
        return self.get("user_agent")
    
    
    def get_delay(self):
        return self.get("concurrency", {}).get("delay", 0)

if __name__ == "__main__":
    config_manager = ConfigManager("config.json")
    city_id = config_manager.get_city_id()
    categories = config_manager.get_categories()
    proxy = config_manager.get_proxy()
    concurrency = config_manager.get_concurrency()
    user_agent = config_manager.get_user_agent()

    print(f"City ID: {city_id}")
    print(f"Categories: {categories}")
    print(f"Proxy: {proxy}")
    print(f"Concurrency: {concurrency}")
    print(f"User Agent: {user_agent}")