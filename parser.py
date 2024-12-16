from playwright.sync_api import sync_playwright, Page, expect, TimeoutError


def navigate_to_fragrantica(page: Page):
    """
    Получение названия парфюма
    """
    page.goto("https://www.fragrantica.com/perfume/By-Kilian/Angels-Share-62615.html")

    locator = page.locator("div#toptop h1")
    title_text = locator.inner_text()  # или text_content()
    print("Заголовок страницы:", title_text)


def get_main_accords(page: Page):
    """
    Получение списка main accords
    """
    accord_bars = page.locator("div.accord-bar")
    count = accord_bars.count()

    accord_data = {}
    for i in range(count):
        # Получаем текст из элемента
        text = accord_bars.nth(i).inner_text().strip()

        # Получаем атрибут style
        style_attr = accord_bars.nth(i).get_attribute("style")
        width_value = None

        # Извлекаем значение width
        if style_attr and "width:" in style_attr:
            width_value = style_attr.split("width:")[1].split(";")[0].strip()

        # Добавляем текст и ширину в словарь
        if text and width_value:
            accord_data[text] = width_value

    # Вывод результата
    print("Результат в виде словаря:", accord_data)


def get_wish(page: Page):
    """
    Находим контейнеры для голосовалок "I have it", "I had it", "I want it"
    """
    # Находим блоки с текстами и прогресс-барами
    rows = page.locator(
        "div[style='display: flex; flex-direction: row; align-items: center;']"
    )
    vote_buttons = rows.locator(".vote-button-name")
    count = rows.count()
    # Словарь для данных
    result = {}
    for i in range(count):
        # Берем текущий элемент из rows
        row = rows.nth(i)
        # Получаем текст название кнопки
        text = vote_buttons.nth(i).inner_text()
        # Поднимаемся на уровень выше и ищем по классу
        chart = row.locator("..").locator(".voting-small-chart-size div div")
        # Получаем информацию о стиле
        style_attr = chart.get_attribute("style")
        # width_value = style_attr.split("width:")[1].split(";")[0].strip()

        if "width:" in style_attr:
            width_value = style_attr.split("width:")[1].split(";")[0].strip()

            # Добавляем данные в словарь
            if text and width_value:
                result[text] = width_value
    print("Результат в виде словаря:", result)


def flavor_evaluation():
    pass


# Основной блок
with sync_playwright() as p:
    # Запуск браузера в режиме с графическим интерфейсом
    browser = p.chromium.launch(headless=False)
    page = browser.new_page()

    # Выполнение шагов
    navigate_to_fragrantica(page)
    get_main_accords(page)
    get_wish(page)

    # Ожидание перед закрытием браузера
    input("Нажмите Enter, чтобы закрыть браузер...")

    # Закрытие браузера
    browser.close()
