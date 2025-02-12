from playwright.sync_api import sync_playwright, Page, expect, TimeoutError
import pandas as pd
import os
import logging
import random
import time
import yaml

# Настройка логгера
logging.basicConfig(
    filename="logs/error_log_links.log",  # Путь к файлу лога
    level=logging.ERROR,  # Уровень логирования (только ошибки)
    format="%(asctime)s - %(levelname)s - %(message)s",
    encoding="utf-8",
)

# Загрузка парметров
with open("config/config.yaml", "r") as file:
    config = yaml.safe_load(file)

web_page = config["web_page"]
get_elements = config["get_elements"]
global_timeout = config["global_timeout"]
path = config["path"]
user_agents = config["user_agents"]


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
        logging.error(f"Ошибка при закрытии баннера: {e}")


def get_links(context: Page):
    """получаем ссылки на ароматы"""
    for sex in ["male", "female", "unisex"]:
        for year in range(2024, 1920, -1):
            try:
                page = context.new_page()
                page.goto(
                    web_page.format(start_year=year, end_year=year + 1, gender=sex),
                    timeout=global_timeout,
                )
                print(f"Year: {year}")

                # закрываем баннер на этой странице
                close_baner(page)

                elements = page.locator("div[class='cell card fr-news-box']")

                for i in range(get_elements):
                    try:
                        link_element = (
                            elements.nth(i)
                            .locator("div.card-section")
                            .nth(1)
                            .locator("a")
                        )
                        link = link_element.get_attribute(
                            "href", timeout=global_timeout
                        )
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
                        error_message = (
                            f"Ошибка при обработке элемента {i} для года {year}: {e}"
                        )
                        print(error_message)
                        logging.error(error_message)  # Логируем ошибку
                        page.close()
                        break

                print(f"Собрано ссылок: {i}")
                page.close()
            except Exception as e:
                error_message = f"Ошибка при переходе на страницу для года {year}: {e}"
                print(error_message)
                logging.error(error_message)  # Логируем ошибку
                continue


with sync_playwright() as p:
    """
    - Попробовать добавить куки и поискать еще способы сделать сбор незаметным
    - вынести список user_agents в файл yaml
    - в тот же файл вынести другие параметры конфигурации
    """
    browser = p.chromium.launch(headless=False)

    # Контекст браузера
    context = browser.new_context(
        viewport={"width": 1280, "height": 720},
        user_agent=random.choice(user_agents),
    )

    # mobile = p.devices["iPhone 13"]
    # context = browser.new_context(**mobile)

    get_links(context)  # Передаем контекст в функцию

    # Случайная задержка перед закрытием
    time.sleep(random.uniform(2, 5))

    input("Нажмите Enter, чтобы закрыть браузер...")
    browser.close()
