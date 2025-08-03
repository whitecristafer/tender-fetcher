# Tender Fetcher

## Кратко: что за проект?

CLI и FastAPI парсер тендеров сайта [rostender.info/extsearch](https://rostender.info/extsearch).  
Парсит тендеры, сохраняет в SQLite/CSV, отдаёт через API.

---

## Как использовать

1. **Убедись, что есть Python 3.9+**
2. **Установи зависимости:**
   ```bash
   pip install -r requirements.txt
   ```

---

## Как запускать

**Максимально быстрый старт (всё и сразу):**
```bash
python main.py --max 50 --output tenders.csv --sqlite tenders.db --both --sort --overwrite --serve
```
- `--max N` — сколько тендеров собрать
- `--output` — путь к CSV
- `--sqlite` — путь к SQLite
- `--both` — сохранить в оба формата
- `--sort` — сортировать по id
- `--overwrite` — перезаписать хранилище (стереть старое)
- `--serve` — запустить FastAPI сервер

<details>

<summary>Примеры:</summary>

- Только SQLite:
  ```bash
  python main.py --sqlite tenders.db
  ```
- Только CSV:
  ```bash
  python main.py --output tenders.csv
  ```
- Сортировка и очистка:
  ```bash
  python main.py --both --sort --overwrite
  ```
- Запуск API после парса:
  ```bash
  python main.py --serve
  ```
- Сохранить 20 тендеров в SQLite (по умолчанию)
  ```bash
  python main.py --max 20 --output tenders.db
  ```
- Сохранить 20 тендеров в CSV
  ```bash
  python main.py --max 20 --csv tenders.csv
  ```
- Сохранить сразу и в SQLite, и в CSV (Сохранит последние 100)
  ```bash
  python main.py --both
  ```
  
</details>

---

## Как получить тендеры через API

- **Основная ссылка (JSON-выдача):**  
  [http://127.0.0.1:8000/tenders](http://127.0.0.1:8000/tenders?limit=10)  
  (Можно добавить `?limit=N` для ограничения количества)

- **Swagger-доки (по желанию):**  
  [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

---

## Использованные технологии

- **Python 3.13**
- **requests** — HTTP-запросы
- **BeautifulSoup** — парсинг HTML
- **sqlite3** — база
- **csv** — запись в файл
- **FastAPI, uvicorn** — API
- **argparse, logging** — CLI и логи
- **Pydantic** — структура тендера

---

## Как бы улучшил

- Добавил бы фильтры по региону/отрасли/дате/статусу/организации (CLI и API)
- Для ускорения попробовал бы внедрить асинхронность (aiohttp) 
- Добавить unit-тесты для функций парсинга и сохранения
- Сделать обработку ошибок более информативной
- Регулярный автосбор по расписанию (cron)
- Расширение на другие тендерные площадки

---

## Контакты, вопросы, баги

- GitHub Issues: [github.com/whitecristafer/tender-fetcher/issues](https://github.com/whitecristafer/tender-fetcher/issues)
