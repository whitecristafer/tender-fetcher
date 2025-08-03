import requests
from bs4 import BeautifulSoup
from app.models import Tender
import logging

BASE_URL = "https://rostender.info/extsearch"

def fetch_tenders_from_web(max_items=100):
    tenders = [] # список для хранения тендеров
    page = 1 # с какой страницы начинать
    count = 0 # сколько тендеров уже собрали

    while count < max_items:
        params = {'page': page} # параметры для get-запроса   
        resp = requests.get(BASE_URL, params=params)   
        resp.raise_for_status()
        soup = BeautifulSoup(resp.text, "html.parser") # парсим HTML
        articles = soup.select("article.tender-row") # делаем запрос

        if not articles: # eсли тендеров нет = прекращаем парсинг
            break

        for tender in articles:
            if count >= max_items:
                break
            try:
                # номер тендера (аля id)
                num = tender.select_one(".tender__number")
                id = None
                if num:
                    id_str = ''.join(filter(str.isdigit, num.text))
                    id = int(id_str) if id_str else None

                # название тендера и ссылка на него
                name = tender.select_one(".tender-info__description")
                title = name.text.strip() if name else "Нет названия"
                link = name['href'] if name and name.has_attr('href') else None
                url = f"https://rostender.info{link}" if link else "Нет ссылки"

                # описание
                description = title

                # заказчик (пробуем вытащить если есть)
                customer = ""
                cust = tender.select_one(".customer-branches-column .list-branches__link")
                if cust:
                    customer = cust.text.strip()

                # товары/услуги обычно совпадает с названием
                items = title

                # дата публикации (берем дату начала)
                date_pub = None
                date_start = tender.select_one(".tender__date-start")
                if date_start:
                    date_pub = date_start.text.strip().replace("от", "").strip()
                else:
                    date_pub = ""

                # дата окончания ищем в (.tender__countdown-text)
                date_end = ""
                dt = tender.select_one(".tender__countdown-text")
                if dt:
                    # берем первую дату из текста (по мск)
                    import re
                    m = re.search(r"(\d{2}\.\d{2}\.\d{4})", dt.text)
                    if m:
                        date_end = m.group(1)

                # бюджет
                price = tender.select_one(".starting-price__price")
                budget = None
                if price:
                    pr_text = price.text.strip().replace("—", "").replace("\u20bd", "").replace("\xa0", "").replace("₽", "").replace("руб.", "")
                    pr_text = pr_text.replace(" ", "")
                    try:
                        budget = float(pr_text) if pr_text else None
                    except ValueError:
                        budget = None

                tenders.append(Tender(
                    id=id,
                    title=title,
                    url=url,
                    description=description,
                    customer=customer,
                    items=items,
                    date_pub=date_pub,
                    date_end=date_end,
                    budget=budget,
                ))
                count += 1
            except Exception as e:
                logging.error(f"Ошибка парсинга: {e}")
        page += 1

    return tenders