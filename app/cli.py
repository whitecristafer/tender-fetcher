import argparse
import logging
import webbrowser
from app.scraper import fetch_tenders_from_web
from app.storage import SQLiteStorage, CSVStorage
from app.api import run_api_server
from app.logger import setup_logging

def main():
    # создаем парсер аргументов командной строки
    parser = argparse.ArgumentParser(description="Tender Fetcher CLI")
    parser.add_argument("--max", type=int, default=100, help="Сколько тендеров собрать")
    parser.add_argument("--output", help="Путь к CSV-файлу")
    parser.add_argument("--sqlite", default="tenders.db", help="Путь к SQLite-файлу")
    parser.add_argument("--both", action="store_true", help="Сохранять в оба формата")
    parser.add_argument("--open", action="store_true", help="Открыть API-доки в браузере")
    parser.add_argument("--serve", action="store_true", help="Запустить FastAPI сервер (после парса)")
    parser.add_argument("--sort", action="store_true", help="Сортировать по id от 0 до +бесконечности")
    parser.add_argument("--overwrite", action="store_true", help="Полностью перезаписать базу/CSV (стирает старое)")
    args = parser.parse_args()

    # инициализируем логирование
    setup_logging()
    logging.info("Парсим сайт...")

    # собираем тендеры с сайта
    tenders = fetch_tenders_from_web(max_items=args.max)
    logging.info(f"Найдено тендеров: {len(tenders)}")

    # если требуется сортировка значит сортируем по id
    if args.sort:
        # сортируем, если id = none считаем = 0
        tenders = sorted(tenders, key=lambda t: t.id if t.id is not None else 0)

    if args.both or args.sqlite:
        db = SQLiteStorage(args.sqlite)
        if args.overwrite:
            db.clear_all()
        db.save_all(tenders)
    if args.both or args.output:
        csv = CSVStorage(args.output or "tenders.csv")
        if args.overwrite:
            csv.clear_all()
        csv.save_all(tenders)
    if args.serve:
        run_api_server(args.sqlite)
    if args.open:
        webbrowser.open("http://127.0.0.1:8000/docs")