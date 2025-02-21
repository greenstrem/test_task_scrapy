import argparse
import logging
import json
from get_cities import CityFetcher
from get_catalogs import CategoryFetcher
from parser import Parser

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class Application:
    def __init__(self):
        self.parser = argparse.ArgumentParser(description="City and Category Fetcher")
        self.setup_arguments()

    def setup_arguments(self):
        subparsers = self.parser.add_subparsers(dest="command", help="Available commands")

        # Парсер для команды get_cities
        get_cities_parser = subparsers.add_parser("get_cities", help="Fetch cities")
        get_cities_parser.add_argument(
            "--all_cities",
            action="store_true",
            help="Fetch all cities"
        )

        # Парсер для команды get_cats
        get_cats_parser = subparsers.add_parser("get_cats", help="Fetch categories")
        get_cats_parser.add_argument(
            "--city_id",
            type=int,
            required=True,
            help="ID of the city to fetch categories for"
        )
        get_cats_parser.add_argument(
            "--nested_categories",
            action="store_true",
            help="Fetch nested categories"
        )

    def get_cities(self, args):
        fetcher = CityFetcher(
            logger=logger,
            all_cities=args.all_cities
        )
        fetcher.fetch_cities()

    def get_cats(self, args):
        fetcher = CategoryFetcher(
            logger=logger,
            city_id=args.city_id,
            nested_categories=args.nested_categories
        )
        categories = fetcher.fetch_categories()
        with open("cat_list.json", "w", encoding="utf-8") as f:
            json.dump(categories, f, ensure_ascii=False, indent=4)

    def run_parser(self):
        parser = Parser()
        parser.run()

    def run(self):
        args = self.parser.parse_args()

        if args.command == "get_cities":
            self.get_cities(args)
        elif args.command == "get_cats":
            self.get_cats(args)
        else:
            self.run_parser()


if __name__ == "__main__":
    app = Application()
    app.run()