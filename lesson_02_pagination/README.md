# Урок 2 — Пагінація та збереження в CSV

Продовжуємо з [quotes.toscrape.com](http://quotes.toscrape.com), але тепер збираємо цитати з **усіх** сторінок (не тільки першої) і зберігаємо результат у файл.

## Завдання

1. Почати з `http://quotes.toscrape.com` (сторінка 1)
2. Зібрати всі цитати (текст + автор), як в уроці 1
3. Перевірити, чи є на сторінці кнопка "Next" — якщо є, перейти на наступну сторінку і повторити збір
4. Зупинитись, коли кнопки "Next" більше немає (остання сторінка)
5. Зберегти всі зібрані цитати у файл `output/quotes.csv` з колонками `text,author`

## Підказки

**Перевірка наявності елемента** — локатор не кидає помилку, якщо елемента немає, можна перевірити кількість:
```python
next_button = page.locator(".next a")
if next_button.count() > 0:
    next_button.click()
```

**Або простіше — просто змінювати URL сторінки:**
```python
# сайт має адреси виду /page/2/, /page/3/ ...
page.goto(f"{URL}/page/{page_num}/")
```
Спробуй обидва підходи подумки — котрий надійніший, якщо структура сайту трохи зміниться?

**Запис у CSV** — стандартна бібліотека `csv`, без зовнішніх залежностей:
```python
import csv

with open("output/quotes.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(["text", "author"])
    for text, author in collected:
        writer.writerow([text, author])
```

Не забудь створити папку `output/` (вона вже в `.gitignore` — дані скрапінгу не комітяться, тільки код).

## Критерій виконання

```bash
python lesson_02_pagination/scraper.py
```
Створює `output/quotes.csv` з усіма цитатами сайту (їх там більше 10 — сайт має кілька сторінок).
