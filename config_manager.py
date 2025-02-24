import json
import os
import ast
from typing import Any, Dict, List
from prompt_toolkit import prompt
from prompt_toolkit.shortcuts import yes_no_dialog
from prompt_toolkit import print_formatted_text as print
from prompt_toolkit.formatted_text import FormattedText

class ConfigManager:
    def __init__(self, config_file: str):
        self.config_file = config_file
        self._load_config()

    def _load_config(self):
        """Загружает конфигурацию. Если файл не найден, предлагает создать его!"""
        if not os.path.exists(self.config_file):
            print(FormattedText([("bold red", f"Конфиг файл '{self.config_file}' не найден. 😢")]))
            if yes_no_dialog(
                title="Создать новый конфиг?",
                text="Хотите создать новый конфигурационный файл?"
            ).run():
                self._create_default_config()
            else:
                raise FileNotFoundError("Конфигурационный файл не создан. Программа завершена.")

        with open(self.config_file, 'r', encoding='utf-8') as file:
            self.config = json.load(file)

    def _create_default_config(self):
        print(FormattedText([("bold cyan", "Создание нового конфигурационного файла...")]))

        # Базовый шаблон конфига
        default_config = {
            "city_id": int(prompt("Введите ID города (по умолчанию 55): ", default="55")),
            "reg_name": prompt("Введите название региона (по умолчанию 'Екатеринбург'): ", default="Екатеринбург"),
            "categories": ["vsye-po-35"],
            "proxy": {
                "enabled": False,  
                "list": []  
            },
            "concurrency": {
                "max_threads": 3,
                "delay": 2,
                "retries": 3
            },
            "user_agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }

        with open(self.config_file, 'w', encoding='utf-8') as file:
            json.dump(default_config, file, ensure_ascii=False, indent=4)
        
        print(FormattedText([("bold green", f"Конфиг файл '{self.config_file}' успешно создан! 🎉")]))
        self.config = default_config

    def get(self, key: str, default: Any = None) -> Any:
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

    def set(self, key: str, value: Any):
        """Устанавливает значение по ключу в конфигурации."""
        self.config[key] = value
        self._save_config()

    def _save_config(self):
        """Сохраняет конфигурацию в файл."""
        with open(self.config_file, 'w', encoding='utf-8') as file:
            json.dump(self.config, file, ensure_ascii=False, indent=4)

def print_config(config: Dict[str, Any]):
    """Красивый вывод конфигурации."""
    print(FormattedText([("bold cyan", "Текущая конфигурация:")]))
    for key, value in config.items():
        print(FormattedText([("bold green", f"{key}:"), ("", f" {value}")]))

def parse_value(value: str) -> Any:
    """Преобразует ввод пользователя в правильный тип данных."""
    try:
        if value.lower() in ("true", "false"):
            return value.lower() == "true"
        return ast.literal_eval(value)
    except (ValueError, SyntaxError):
        return value

def edit_config(config_manager: ConfigManager):
    """Редактирование конфигурации."""
    while True:
        key = prompt("Введите ключ (или 'exit' для выхода): ")
        if key.lower() == "exit":
            break

        current_value = config_manager.get(key)
        if current_value is not None:
            print(FormattedText([("bold yellow", f"Текущее значение для '{key}':"), ("", f" {current_value}")]))
        else:
            print(FormattedText([("bold yellow", f"Ключ '{key}' не существует. Создать новый?")]))

        if isinstance(current_value, dict):
            print(FormattedText([("bold cyan", "Редактирование словаря. Введите ключи и значения.")]))
            new_dict = {}
            for sub_key, sub_value in current_value.items():
                new_value = prompt(f"Введите значение для '{sub_key}' (текущее: {sub_value}): ", default=str(sub_value))
                new_dict[sub_key] = parse_value(new_value)
            config_manager.set(key, new_dict)
        elif isinstance(current_value, list):
            print(FormattedText([("bold cyan", "Редактирование списка. Введите элементы через запятую.")]))
            new_list = prompt(f"Введите новые элементы списка (текущие: {current_value}): ", default=", ".join(map(str, current_value)))
            new_list = [parse_value(item.strip()) for item in new_list.split(",")]
            config_manager.set(key, new_list)
        else:
            value = prompt(f"Введите новое значение для '{key}': ", default=str(current_value))
            config_manager.set(key, parse_value(value))

        print(FormattedText([("bold green", f"Успешно: Ключ '{key}' обновлен.")]))

def main():
    config_manager = ConfigManager("config.json")

    while True:
        print(FormattedText([("bold cyan", "Меню:")]))
        print(FormattedText([("bold green", "1. Показать конфигурацию")]))
        print(FormattedText([("bold green", "2. Редактировать конфигурацию")]))
        print(FormattedText([("bold green", "3. Выйти")]))

        choice = prompt("Выберите действие (1-3): ")

        if choice == "1":
            print_config(config_manager.config)
        elif choice == "2":
            edit_config(config_manager)
        elif choice == "3":
            break
        else:
            print(FormattedText([("bold red", "Неверный выбор. Попробуйте снова.")]))

if __name__ == "__main__":
    main()