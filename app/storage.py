import sqlite3
import csv
from app.models import Tender
class SQLiteStorage:
    """
    класс для работы с SQLite. Можно сохранять/получать/очищать тендеры
    """
    def __init__(self, path):
        # создаём соединение с базой
        self.conn = sqlite3.connect(path)
        self._init_db()

    def _init_db(self):
        # проверяем есть ли таблицу, нет то создаем
        c = self.conn.cursor()
        c.execute("""
            CREATE TABLE IF NOT EXISTS tenders (
                id INTEGER PRIMARY KEY,
                title TEXT,
                url TEXT,
                description TEXT,
                customer TEXT,
                items TEXT,
                date_pub TEXT,
                date_end TEXT,
                budget REAL
            )
        """)
        self.conn.commit()

    def save_all(self, tenders):
        """
        сохраняет все тендеры в базу (добавляем новые/обновляем старые)
        """
        c = self.conn.cursor()
        for t in tenders:
            c.execute("""
                INSERT OR REPLACE INTO tenders (id, title, url, description, customer, items, date_pub, date_end, budget)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                (t.id, t.title, t.url, t.description, t.customer, t.items, t.date_pub, t.date_end, t.budget))
        self.conn.commit()

    def fetch_all(self, limit=None):
        """
        получить все тендеры из базы (до лимита)
        """
        c = self.conn.cursor()
        q = "SELECT id, title, url, description, customer, items, date_pub, date_end, budget FROM tenders"
        if limit:
            q += " LIMIT ?"
            c.execute(q, (limit,))
        else:
            c.execute(q)
        rows = c.fetchall()
        # преобразуем строки из базы в объекты тендера
        return [Tender(**dict(zip([
            "id", "title", "url", "description", "customer", "items", "date_pub", "date_end", "budget"
        ], row))) for row in rows]

    def clear_all(self):
        """
        полностью очищает таблицу тендеров (удаляет всё)
        """
        c = self.conn.cursor()
        c.execute("DELETE FROM tenders")
        self.conn.commit()

class CSVStorage:
    """
    класс для работы с csv (сохраняет/очищает)
    """
    def __init__(self, path):
        self.path = path

    def save_all(self, tenders):
        """
        сохраняет все тендеры в csv (с заголовками)
        """
        with open(self.path, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["id", "title", "url", "description", "customer", "items", "date_pub", "date_end", "budget"])
            for t in tenders:
                writer.writerow([t.id, t.title, t.url, t.description, t.customer, t.items, t.date_pub, t.date_end, t.budget])

    def clear_all(self):
        """
        очищает csv оставляет только заголовки
        """
        with open(self.path, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["id", "title", "url", "description", "customer", "items", "date_pub", "date_end", "budget"])