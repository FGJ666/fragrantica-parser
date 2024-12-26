from playwright.sync_api import sync_playwright, Page
import pandas as pd
import random
import yaml

# Загрузка конфигурации из YAML
with open("config/config.yaml", "r") as file:
    config = yaml.safe_load(file)
paths = config["path"]
user_agents = config["user_agents"]

# Чтение ссылок из CSV файла
links = pd.read_csv(paths)[:10]


def close_baner(page: Page):
    """Закрывает баннер на текущей странице."""
    try:
        text_element = page.locator("h2")
        if text_element.count() > 0:
            print(text_element.inner_text(), "Текст найден")
            print("Элемент найден!")
            close_button = page.get_by_text(
                "Продолжать, не поддерживая нас", timeout=60000
            )
            close_button.click(timeout=60000)
            print("Баннер закрыт.")
        else:
            print("Элемент не найден")
    except Exception as e:
        print(f"Не удалось нажать кнопку закрытия: {e}")


def get_fragrantica_data(page: Page, link: str, df):
    """Собирает данные со страницы Fragrantica."""

    page.goto(link, timeout=60000)
    # Закрываем всплывающий банер
    close_baner(page)
    data = {}  # Создаем словарь для хранения данных

    try:
        # Заголовок страницы
        locator = page.locator("div#toptop h1")
        title_text = locator.inner_text()
        data["title"] = title_text

        # Основные аккорды
        accord_bars = page.locator("div.accord-bar")
        for i in range(accord_bars.count()):
            text = accord_bars.nth(i).inner_text().strip()
            style_attr = accord_bars.nth(i).get_attribute("style")
            if style_attr and "width:" in style_attr:
                width_value = (
                    style_attr.split("width:")[1].split(";")[0].strip().replace("%", "")
                )
                data[text] = width_value

        # Голосования
        rows = page.locator(
            "div[style='display: flex; flex-direction: row; align-items: center;']"
        )
        vote_buttons = rows.locator(".vote-button-name")
        for i in range(rows.count()):
            row = rows.nth(i)
            text = vote_buttons.nth(i).inner_text()
            chart = row.locator("..").locator(".voting-small-chart-size div div")
            style_attr = chart.get_attribute("style")
            if style_attr and "width:" in style_attr:
                width_value = (
                    style_attr.split("width:")[1].split(";")[0].strip().replace("%", "")
                )
                data[text] = width_value

        # Оценки
        rows = page.locator(
            "div[style='display: flex; justify-content: space-evenly;']"
        ).first
        name = rows.locator("div[style='display: flex; justify-content: center;']")
        evaluations = rows.locator(".voting-small-chart-size div div")
        for i in range(name.count()):
            text = name.nth(i).inner_text()
            chart = evaluations.nth(i).get_attribute("style")
            if chart and "width:" in chart:
                width_value = (
                    chart.split("width:")[1].split(";")[0].strip().replace("%", "")
                )
                data[text] = width_value

        # Сезонность
        rows = page.locator(
            "div[style='display: flex; justify-content: space-evenly;']"
        ).nth(1)
        name = rows.locator("div[style='display: flex; justify-content: center;']")
        evaluations = rows.locator(".voting-small-chart-size div div")
        for i in range(name.count()):
            text = name.nth(i).inner_text()
            chart = evaluations.nth(i).get_attribute("style")
            if chart and "width:" in chart:
                width_value = (
                    chart.split("width:")[1].split(";")[0].strip().replace("%", "")
                )
                data[text] = width_value

        # Рейтинг
        rating = page.locator("span[itemprop='ratingValue']").inner_text()
        votes = (
            page.locator("span[itemprop='ratingCount']").inner_text().replace(",", "")
        )
        data["rating"] = rating
        data["votes"] = votes

        # Пирамида аромата
        notes_selector = "div[style='display: flex; justify-content: center; text-align: center; flex-flow: wrap; align-items: flex-end; padding: 0.5rem;']"
        notes_elements = page.locator(notes_selector)
        notes_names = ["Top Notes", "Middle Notes", "Base Notes"]
        for i in range(notes_elements.count()):
            notes_text = notes_elements.nth(i).inner_text().split("\n")
            data[notes_names[i]] = notes_text

        # Отзывы о стойкости
        longevity = page.locator("div[class='grid-x grid-margin-x']")
        for i in range(2, 6):
            vote = longevity.nth(i).inner_text().split()
            data[vote[0]] = vote[1]

        # Отзывы о шлейфе
        sillage = page.locator("div[class='grid-x grid-margin-x']")
        for i in range(7, 10):
            vote = sillage.nth(i).inner_text().split()
            data[vote[0]] = vote[1]

        # Отзывы о гендере
        gender = page.locator("div[class='grid-x grid-margin-x']")
        for i in range(11, 15):
            vote = gender.nth(i).inner_text().split()
            data[vote[0]] = vote[1]

        # Отзывы о соотношении цены и качества
        price_value = page.locator("div[class='grid-x grid-margin-x']")
        for i in range(16, 20):
            vote = price_value.nth(i).inner_text().split()
            data[vote[0]] = vote[1]

    except Exception as e:
        print(f"Ошибка при сборе данных с {link}: {e}")
        return df

    df = pd.concat(
        [df, pd.DataFrame([data])], ignore_index=True
    )  # Добавление данных в DataFrame
    return df


# Основной блок
with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)

    # Контекст браузера
    context = browser.new_context(
        viewport={"width": 1280, "height": 720},
        user_agent=random.choice(user_agents),
    )
    df = pd.DataFrame()  # Создаем пустой DataFrame
    page = context.new_page()
    # Итерация по всем ссылкам в файле
    for link in links["link"]:
        df = get_fragrantica_data(page, link, df)

    # Сохранение DataFrame в CSV
    df.to_csv("data/fragrance_data.csv", index=False)
    print("Данные успешно собраны и сохранены в fragrance_data.csv")

    input("Нажмите Enter, чтобы закрыть браузер...")
    context.close()
    browser.close()
