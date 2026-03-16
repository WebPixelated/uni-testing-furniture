# Mebelmart GUI Test Automation Framework

Автоматизированное тестирование GUI для [mebelmart-saratov.ru](https://mebelmart-saratov.ru/myagkaya_mebel_v_saratove/divanyi_v_saratove).

![Python](https://img.shields.io/badge/Python-3.13-blue)
![Playwright](https://img.shields.io/badge/Playwright-latest-green)
![pytest](https://img.shields.io/badge/pytest-8.x-orange)
![Allure](https://img.shields.io/badge/Allure-2.x-yellow)

---

## Стек технологий

| Инструмент                       | Назначение                        |
| -------------------------------- | --------------------------------- |
| Python 3.13                      | Язык программирования             |
| Poetry                           | Управление зависимостями и сборка |
| Playwright (`pytest-playwright`) | Автоматизация браузера (Chrome)   |
| pytest                           | Тест-раннер                       |
| Allure (`allure-pytest`)         | HTML-отчёты со скриншотами        |
| Loguru                           | Логирование (консоль + файл)      |

---

## Структура проекта

```
mebelmart-tests/
├── .github/
│   └── workflows/
│       └── tests.yml          # CI/CD — GitHub Actions
│
├── pages/                     # Page Object Layer
│   ├── base_page.py           # Базовые действия, ожидания, скриншоты
│   ├── catalog_page.py        # Каталог диванов + ценовой фильтр
│   ├── product_page.py        # Страница товара
│   ├── cart_page.py           # Корзина
│   ├── favorite_page.py       # Избранное
│   ├── main_page.py           # Главная страница (поиск, меню)
│   └── search_results_page.py # Результаты поиска
│
├── tests/                     # Test Layer
│   ├── conftest.py            # Фикстуры Page Object
│   ├── test_filter.py         # 2.1 Фильтрация по цене
│   ├── test_product_card.py   # 2.2 Карточка товара
│   ├── test_favorites.py      # 2.3 Добавление в избранное
│   ├── test_search.py         # 2.4 Поиск по названию
│   └── test_cart.py           # 2.5 Корзина и цена
│
├── utils/
│   ├── logger.py              # Настройка Loguru
│   └── helpers.py             # parse_price(), parse_dimension()
│
├── logs/                      # Файлы логов (генерируются автоматически)
├── allure-results/            # Сырые данные Allure (генерируются автоматически)
├── conftest.py                # Конфигурация браузера, скриншот при падении
├── pytest.ini                 # Настройки pytest
└── pyproject.toml             # Poetry — зависимости проекта
```

---

## Архитектура (Layered Architecture)

```
┌─────────────────────────────────┐
│           Tests Layer           │  tests/*.py
│  (сценарии, assertions, шаги)   │
└────────────────┬────────────────┘
                 │ использует
┌────────────────▼────────────────┐
│        Page Object Layer        │  pages/*.py
│  (локаторы, действия, ожидания) │
└────────────────┬────────────────┘
                 │ наследует
┌────────────────▼────────────────┐
│           Base Page             │  pages/base_page.py
│  (click, fill, wait, screenshot)│
└────────────────┬────────────────┘
                 │ использует
┌────────────────▼────────────────┐
│         Playwright Page         │  (браузер Chrome)
└─────────────────────────────────┘
```

---

## Тестовые сценарии

| #   | Тест                   | Описание                                                   |
| --- | ---------------------- | ---------------------------------------------------------- |
| 2.1 | `test_filter.py`       | Фильтрация каталога по диапазону цен, проверка результатов |
| 2.2 | `test_product_card.py` | Открытие карточки товара, проверка характеристик           |
| 2.3 | `test_favorites.py`    | Добавление в избранное, проверка иконки и страницы         |
| 2.4 | `test_search.py`       | Поиск товара по названию                                   |
| 2.5 | `test_cart.py`         | Добавление в корзину, проверка цены                        |

---

## Установка

### Требования

- Python 3.13+
- Poetry ([инструкция по установке](https://python-poetry.org/docs/#installation))
- Allure CLI ([инструкция](https://allurereport.org/docs/install/))

### Шаги

```bash
# 1. Клонировать репозиторий
git clone https://github.com/WebPixelated/uni-testing-furniture.git
cd uni-testing-furniture

# 2. Установить зависимости
poetry install

# 3. Установить браузер Chromium
poetry run playwright install chromium
```

---

## Запуск тестов

```bash
# Все тесты (с открытым браузером)
poetry run pytest

# Один конкретный тест
poetry run pytest tests/test_search.py -v

# Headless-режим (без окна браузера, для CI)
poetry run pytest --headless

# С немедленным выводом логов в консоль
poetry run pytest -s
```

---

## Allure-отчёт

```bash
# После запуска тестов — открыть живой отчёт в браузере
allure serve allure-results

# Или сгенерировать статичный HTML (для архива или отправки)
allure generate allure-results -o allure-report --clean
# Затем открыть: allure-report/index.html
```

Каждый тест содержит скриншоты ключевых шагов:

| Тест            | Скриншоты                                                    |
| --------------- | ------------------------------------------------------------ |
| Фильтр          | Каталог → фильтр открыт → результаты                         |
| Карточка товара | Каталог → товар найден → страница → характеристики           |
| Поиск           | Главная → результаты поиска                                  |
| Избранное       | До клика → после клика → страница избранного → после очистки |
| Корзина         | Каталог → страница товара → корзина → после очистки          |

При падении любого теста автоматически прикрепляется дополнительный скриншот экрана.

---

## CI/CD (GitHub Actions)

Пайплайн запускается автоматически при каждом `push` и `pull request` в ветки `main` / `master`, а также вручную через вкладку **Actions** в GitHub.

### Шаги пайплайна

```
Checkout → Python + Poetry → Кэш venv → Зависимости
→ Playwright Chromium → Тесты (headless)
→ Allure Report → Публикация на GitHub Pages
→ Загрузка артефактов (сырые результаты, 14 дней)
```

### Настройка GitHub Pages для отчёта

1. Перейти в **Settings → Pages** репозитория
2. Source: **Deploy from a branch**
3. Branch: **gh-pages**, папка: **/ (root)**
4. После первого запуска CI отчёт будет доступен по адресу:  
   `https://<your-username>.github.io/<repo-name>/`

> **Важно:** ветка `gh-pages` создаётся автоматически при первом запуске — вручную создавать её не нужно.

---

## Логирование

Логи пишутся одновременно в два места:

- **Консоль** — уровень INFO и выше, с цветовой подсветкой
- **Файл** — `logs/test_YYYY-MM-DD.log`, уровень DEBUG, ротация по дням, хранение 7 дней

---

## .gitignore

```gitignore
# Виртуальное окружение
.venv/

# Сырые данные Allure (генерируются при каждом прогоне)
allure-results/

# Готовый HTML-отчёт
allure-report/

# Логи
logs/

# Кэш Python
__pycache__/
*.pyc
.pytest_cache/
```
