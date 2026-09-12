# Урок 5 — Pandas: обробка й аналіз зібраних даних

Беремо скрапер з [lesson_04_retry_rate_limit](../lesson_04_retry_rate_limit) (можна скопіювати логіку збору, або імпортувати) і замінюємо ручний `csv.writer` на pandas, плюс додаємо трохи аналізу.

## Завдання

1. Зібрати цитати так само, як в уроці 4 (`get_with_retry`, пагінація, `collected` — список кортежів `(text, author)`)
2. Створити `pd.DataFrame(collected, columns=["text", "author"])`
3. Прибрати дублікати — `df.drop_duplicates()`
4. Вивести в консоль:
   - `df.shape` — скільки рядків/колонок вийшло
   - `df["author"].value_counts()` — топ авторів за кількістю цитат
   - `df[df["author"] == "Albert Einstein"]` — всі цитати конкретного автора (обери будь-якого автора з списку)
5. Зберегти результат через `df.to_csv("output/quotes_pandas.csv", index=False)`

## Підказки

Імпорт:
```python
import pandas as pd
```

Якщо ліньки копіювати весь скрапер — можна прочитати вже готовий `output/quotes_retry.csv` з попереднього уроку:
```python
df = pd.read_csv("output/quotes_retry.csv")
```
і працювати з ним напряму (пункти 3-5), без повторного скрапінгу. Обидва підходи ок для цієї вправи.

## Критерій виконання

```bash
python lesson_05_pandas/scraper.py
```
Виводить в консоль форму таблиці, топ авторів і приклад фільтрації; створює `output/quotes_pandas.csv`.
