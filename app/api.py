from fastapi import FastAPI
from app.storage import SQLiteStorage
import uvicorn

def run_api_server(sqlite_path):
    """
    Запускает FastAPI сервер для выдачи тендеров по API
    """
    app = FastAPI(title="Tender Fetcher API")

    @app.get("/tenders")
    def get_tenders(limit: int = 100):
        """
        Endpoint для получения тендеров.
        @:param limit — сколько тендеров вернуть (по умолчанию 100).
        @:return список тендеров в формате JSON.
        """
        db = SQLiteStorage(sqlite_path)
        tenders = db.fetch_all(limit=limit)
        return [t.dict() for t in tenders]

    uvicorn.run(app, host="127.0.0.1", port=8000)