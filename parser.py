from playwright.sync_api import sync_playwright, Page, expect, TimeoutError


def navigate_to_fragrantica(page: Page):
    """
    Получение названия парфюма
    """
    page.goto(
        "https://www.fragrantica.com/perfume/Giorgio-Armani/Emporio-Armani-Stronger-With-You-Intensely-52802.html",
        # "https://www.fragrantica.com/perfume/By-Kilian/Angels-Share-62615.html",
        timeout=60000,
    )

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
            width_value = (
                style_attr.split("width:")[1].split(";")[0].strip().replace("%", "")
            )

        # Добавляем текст и ширину в словарь
        if text and width_value:
            accord_data[text] = width_value

    # Вывод результата
    print("Main accords:", accord_data)


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
            width_value = (
                style_attr.split("width:")[1].split(";")[0].strip().replace("%", "")
            )

            # Добавляем данные в словарь
            if text and width_value:
                result[text] = width_value
    print("Желания:", result)


def get_fragrance_evaluation(page: Page):
    """
    Получаем оценки пользователей о парфюме.
    """
    # Получаем первый набор строк, представляющий блоки с оценками.
    rows = page.locator(
        "div[style='display: flex; justify-content: space-evenly;']"
    ).first

    # Ищем названия критериев оценки внутри строк.
    name = rows.locator("div[style='display: flex; justify-content: center;']")

    # Ищем графики оценок (ширину блоков, представляющих процентные значения).
    evaluations = rows.locator(".voting-small-chart-size div div")

    # Считаем количество критериев оценки.
    count = name.count()

    # Инициализируем пустой словарь для сохранения результатов.
    result = {}

    # Проходим по каждому критерию.
    for i in range(count):
        # Получаем текстовое название критерия оценки.
        text = name.nth(i).inner_text()

        # Получаем стиль графика, чтобы извлечь процентное значение.
        chart = evaluations.nth(i).get_attribute("style")

        # Проверяем, если в стиле есть параметр "width".
        if "width:" in chart:
            # Извлекаем значение ширины графика (процент).
            width_value = (
                chart.split("width:")[1].split(";")[0].strip().replace("%", "")
            )

            # Добавляем текст и значение в результат, если они не пустые.
            if text and width_value:
                result[text] = width_value

    # Выводим словарь с результатами оценок.
    print("Оценки:", result)


def get_fragrance_season(page: Page):
    """
    Получаем оценки пользователей о подходящем сезоне.
    """
    # Получаем первый набор строк, представляющий блоки с оценками.
    rows = page.locator(
        "div[style='display: flex; justify-content: space-evenly;']"
    ).nth(1)

    # Ищем названия критериев оценки внутри строк.
    name = rows.locator("div[style='display: flex; justify-content: center;']")

    # Ищем графики оценок (ширину блоков, представляющих процентные значения).
    evaluations = rows.locator(".voting-small-chart-size div div")

    # Считаем количество критериев оценки.
    count = name.count()

    # Инициализируем пустой словарь для сохранения результатов.
    result = {}

    # Проходим по каждому критерию.
    for i in range(count):
        # Получаем текстовое название критерия оценки.
        text = name.nth(i).inner_text()

        # Получаем стиль графика, чтобы извлечь процентное значение.
        chart = evaluations.nth(i).get_attribute("style")

        # Проверяем, если в стиле есть параметр "width".
        if "width:" in chart:
            # Извлекаем значение ширины графика (процент).
            width_value = (
                chart.split("width:")[1].split(";")[0].strip().replace("%", "")
            )

            # Добавляем текст и значение в результат, если они не пустые.
            if text and width_value:
                result[text] = width_value

    # Выводим словарь с результатами оценок.
    print("Сезонность:", result)


def get_rating(page: Page):
    """
    Получение рейтинга
    """
    rating = page.locator("span[itemprop='ratingValue']").inner_text()
    votes = page.locator("span[itemprop='ratingCount']").inner_text().replace(",", "")

    print(f"Рейтинг: {rating}\nГолосов: {votes}")


def get_perfume_pyramid(page: Page):
    """
    Получение пирамиды аромата
    """
    # Селектор для всех нот
    notes_selector = "div[style='display: flex; justify-content: center; text-align: center; flex-flow: wrap; align-items: flex-end; padding: 0.5rem;']"

    # Получаем все ноты
    notes_elements = page.locator(notes_selector)

    # Имена нот
    notes_names = ["Top Notes", "Middle Notes", "Base Notes"]

    # Создаем словарь с нотами
    pyramid = {
        notes_names[i]: notes_elements.nth(i).inner_text().split("\n")
        for i in range(notes_elements.count())
    }

    print(pyramid)


def get_longevity(page: Page):
    """
    получение отзывов о стойкости аромата
    """
    longevity = page.locator("div[class='grid-x grid-margin-x']")
    longevity_vote = {}
    for i in range(2, 6):
        vote = longevity.nth(i).inner_text().split()
        longevity_vote[vote[0]] = vote[1]
    print(longevity_vote)


def get_sillage(page: Page):
    """
    получение отзывов о шлейфе аромата
    """
    sillage = page.locator("div[class='grid-x grid-margin-x']")
    sillage_vote = {}
    for i in range(7, 10):
        vote = sillage.nth(i).inner_text().split()
        sillage_vote[vote[0]] = vote[1]
    print(sillage_vote)


def get_gender(page: Page):
    """
    получение отзывов о гендерной принадлежности аромата
    """
    gender = page.locator("div[class='grid-x grid-margin-x']")
    gender_vote = {}
    for i in range(11, 15):
        vote = gender.nth(i).inner_text().split()
        gender_vote[vote[0]] = vote[1]
    print(gender_vote)


def get_price_value(page: Page):
    """
    получение отзывов о соответствии цены и качества аромата
    """
    price_value = page.locator("div[class='grid-x grid-margin-x']")
    price_value_vote = {}
    for i in range(16, 20):
        vote = price_value.nth(i).inner_text().split()
        price_value_vote[vote[0]] = vote[1]
    print(price_value_vote)


# Основной блок
with sync_playwright() as p:
    # Запуск браузера в режиме с графическим интерфейсом
    browser = p.chromium.launch(headless=False)
    page = browser.new_page()

    # Выполнение шагов
    navigate_to_fragrantica(page)
    get_main_accords(page)
    get_wish(page)
    get_fragrance_evaluation(page)
    get_fragrance_season(page)
    get_rating(page)
    get_perfume_pyramid(page)
    get_longevity(page)
    get_sillage(page)
    get_gender(page)
    get_price_value(page)

    # Ожидание перед закрытием браузера
    input("Нажмите Enter, чтобы закрыть браузер...")

    # Закрытие браузера
    browser.close()
