from playwright.sync_api import sync_playwright, Page, expect, TimeoutError
import pandas as pd
import os
import logging

path = r"data/fragrance_links.csv"
get_elements = 99000
global_timeout = 5000
web_page = "https://www.fragrantica.com/search/?godina={}%3A{}"


def save_on_disk(link):
    file_exists = os.path.isfile("data/fragrance_links.csv")
    with open("data/fragrance_links.csv", "a", encoding="utf-8") as f:
        if not file_exists:
            f.write("link\n")
        f.write(link + "\n")


def drop_dupl(path):
    df = pd.read_csv(path).drop_duplicates()
    df.to_csv(path, index=False)


def close_baner(page: Page):
    """Закрывает баннер на текущей странице"""
    try:
        text_element = page.locator("h2")
        if text_element.count() > 0:  # Проверяем, найден ли элемент
            print(text_element.inner_text(), "Текст найден")
            print("Элемент найден!")
            close_button = page.get_by_text(
                "Продолжать, не поддерживая нас", timeout=global_timeout
            )

            close_button.click(timeout=global_timeout)
            print("Баннер закрыт.")
        else:
            print("Элемент не найден")
    except Exception as e:
        print(f"Не удалось нажать кнопку закрытия: {e}")


def get_links(context: Page):
    """получаем ссылки на ароматы"""
    for year in range(2024, 1920, -1):
        try:
            page = context.new_page()
            page.goto(
                web_page.format(year, year + 1),
                timeout=global_timeout,
            )
            print(f"Year: {year}")

            # закрываем баннер на этой странице
            close_baner(page)

            elements = page.locator("div[class='cell card fr-news-box']")

            for i in range(get_elements):
                try:
                    link_element = (
                        elements.nth(i).locator("div.card-section").nth(1).locator("a")
                    )
                    link = link_element.get_attribute("href", timeout=global_timeout)
                    save_on_disk(link)

                    if (i + 1) % 30 == 0 and i != 0:
                        page.get_by_text("Show more results").click(
                            timeout=global_timeout
                        )
                        print(f"нажал {i // 30} раз")
                    elif (i + 1) % 100 == 0:
                        # удаляем дубли
                        drop_dupl(path)

                        print(f"Собрано ссылок: {i + 1}")

                except Exception as e:
                    print(f"Ошибка при обработке элемента {i} для года {year}: {e}")
                    page.close()
                    break

            print(f"Собрано ссылок: {i}")
            page.close()
        except Exception as e:
            print(f"Ошибка при переходе на страницу для года {year}: {e}")
            continue


with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)

    # Контекст браузера
    # context = browser.new_context(
    #     viewport={"width": 1280, "height": 720},
    #     user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    # )

    mobile = p.devices["iPhone 12"]
    context = browser.new_context(**mobile)

    get_links(context)  # Передаем контекст в функцию

    input("Нажмите Enter, чтобы закрыть браузер...")
    browser.close()
