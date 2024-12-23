from playwright.sync_api import sync_playwright, Page, expect, TimeoutError
import pandas as pd
import os

path = r"data/fragrance_links.csv"
get_elements = 99000


def save_on_disk(link):
    """Проверяем, существует ли файл"""
    file_exists = os.path.isfile("data/fragrance_links.csv")

    # Открываем файл в режиме добавления
    with open("data/fragrance_links.csv", "a", encoding="utf-8") as f:
        # Если файл не существует, добавляем заголовок
        if not file_exists:
            f.write("link\n")  # Заголовок для CSV
        f.write(link + "\n")  # Записываем ссылку


def drop_dupl(path):
    df = pd.read_csv(path).drop_duplicates()
    df.to_csv(path, index=False)


def get_links(page: Page):
    """получаем ссылки на ароматы"""

    page.goto("https://www.fragrantica.com/search/", timeout=60000)

    elements = page.locator("div[class='cell card fr-news-box']")

    for i in range(get_elements):
        link_element = elements.nth(i).locator("div.card-section").nth(1).locator("a")
        link = link_element.get_attribute("href")
        save_on_disk(link)  # Сохраняем ссылку на диск

        if (i + 1) % 30 == 0 and i != 0:
            page.get_by_text("Show more results").click()
            print(f"нажал {i // 30} раз")
            print(f"Собрано ссылок: {i+1}")

    print(f"Собрано ссылок: {i+1}")
    drop_dupl(path)


def close_baner(page: Page):
    text = page.locator("h2:has-text('Похоже, у вас включен блокировщик рекламы.')")
    print(text, "Текст найден")
    if text.count() > 0:  # Проверяем, найден ли элемент
        print("Элемент найден!")
        try:
            # Находим и нажимаем на кнопку закрытия баннера
            close_button = page.get_by_text("Продолжать, не поддерживая нас")
            close_button.click()
            print("Баннер закрыт.")
        except Exception as e:
            print(f"Не удалось нажать кнопку закрытия: {e}")
    else:
        print("Элемент не найден.")


with sync_playwright() as p:
    # Запуск браузера в режиме с графическим интерфейсом
    browser = p.chromium.launch(headless=False)
    context = browser.new_context(
        # ignore_default_args=["--enable-automation"],
        viewport={"width": 1280, "height": 720},
        user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    )
    # mobile = p.devices["iPhone 12"]
    # context = browser.new_context(**mobile)

    page = context.new_page()

    get_links(page)
    # close_baner(page)

    # Ожидание перед закрытием браузера
    input("Нажмите Enter, чтобы закрыть браузер...")

    # Закрытие браузера
    # browser.close()
