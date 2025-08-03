from pydantic import BaseModel

class Tender(BaseModel):
    """
    модель одного тендера для удобной работы.
    Используется для хранения, сериализации, передачи через API.
    """
    id: int | None # ID тендера (может быть None если не найден)
    title: str # название тендера
    url: str # ссылка на тендер
    description: str # описание (иногда совпадает с title)
    customer: str # заказчик (может быть пусто)
    items: str # товары/услуги (иногда совпадает с title)
    date_pub: str # дата публикации (или начала)
    date_end: str # дата окончания тендера
    budget: float | None = None # бюджет (может быть None если нет данных)