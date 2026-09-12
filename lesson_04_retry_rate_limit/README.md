# Урок 4 — Retry-логіка та rate limiting

Беремо скрипт з уроку 3 ([lesson_03_requests_bs4](../lesson_03_requests_bs4)) і робимо його стійкішим до реальних мережевих проблем.

## Завдання

1. Написати функцію `get_with_retry(url, max_attempts=3)`, яка:
   - робить `requests.get(url, headers=..., timeout=10)`
   - викликає `response.raise_for_status()`
   - при помилці (`requests.exceptions.RequestException`) — пробує ще раз, до `max_attempts` спроб
   - на останній невдалій спробі — прокидає виняток далі (`raise`)
   - між спробами — пауза (`time.sleep(...)`), можна exponential backoff (`2 ** attempt`)
2. Використати `headers` з "людським" `User-Agent` замість дефолтного
3. Додати паузу `time.sleep(0.3)` **між сторінками** (не тільки між retry-спробами)
4. Замінити прямі виклики `requests.get(url)` в циклі пагінації на `get_with_retry(url)`
5. Логувати в консоль номер поточної сторінки, що обробляється (`print(f"Сторінка {page_num}...")`)

## Підказки

Структура функції — дивись приклад з теорії (конспект буде в Obsidian, глянь [[Retry & Rate Limiting]] якщо забудеш). Ключове:
```python
def get_with_retry(url, max_attempts=3):
    for attempt in range(1, max_attempts + 1):
        try:
            response = requests.get(url, headers=HEADERS, timeout=10)
            response.raise_for_status()
            return response
        except requests.exceptions.RequestException as e:
            print(f"Спроба {attempt} невдала: {e}")
            if attempt == max_attempts:
                raise
            time.sleep(2 ** attempt)
```

**Як перевірити, що retry дійсно працює** — тимчасово підстав неіснуючий URL (наприклад `http://quotes.toscrape.com/nonexistent/`) і подивись, чи скрипт справді робить 3 спроби з паузами перед тим, як впасти з помилкою, а не падає одразу.

## Критерій виконання

```bash
python lesson_04_retry_rate_limit/scraper.py
```
Працює як урок 3 (100 цитат у CSV), але з паузами між сторінками, "людським" User-Agent, і не падає одразу при першій мережевій похибці.
