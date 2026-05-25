# 🇺🇦 DOU Vacancies Analytics Pipeline

## Release Info

- **Тег версії:** `final-project`
- **Глобальний статус:** `v1.0.0 (Production Ready)`
- **Призначення:** Моніторинг, збір та аналітика українського ІТ-ринку праці на основі даних порталу DOU.ua.

---

# 📌 Опис проєкту (Project Overview)

**DOU Vacancies Analytics Pipeline** — це надійний, повністю автоматизований інженерний конвеєр обробки даних (Data Pipeline), призначений для збору вакансій з порталу DOU, їх структурування, очищення від лінгвістичного шуму та виявлення прихованих ринкових трендів за допомогою методів NLP (*Natural Language Processing*) та EDA.

Система спроєктована за принципом класичного ETL (*Extract, Transform, Load*) циклу, що дозволяє регулярно оновлювати аналітичні метрики ринку без ручного втручання.

---

# 🏗 Архітектура системи (Pipeline Workflow)

Конвеєр складається з чотирьох послідовних ізольованих етапів:

## 1. Extraction (Модуль скрапінгу)

Автоматизований збір HTML-сторінок категорій вакансій (*Data Science, ML, Data Engineering, Python* тощо).

Використовує:
- `requests` — для швидких HTTP-запитів
- `BeautifulSoup4` — для стабільного парсингу DOM-дерева

Реалізовано:
- обробку таймаутів
- базовий захист від блокування IP

---

## 2. Transformation & Cleaning (Очищення та структурування)

Виконується:
- видалення HTML-тегів
- очищення від JavaScript та CSS
- нормалізація назв міст
- уніфікація форматів роботи

Також реалізований парсинг зарплатних вилок:

```text
$2000-3500
```

у два окремі числові поля:

- `salary_min`
- `salary_max`

---

## 3. NLP Skills Extraction (Семантичний аналіз)

Застосування:
- гнучких регулярних виразів
- словникових мапінгів

для автоматичного витягування Hard Skills безпосередньо з тексту вакансії.

Система розпізнає понад **150 технологій**.

---

## 4. Exploratory Data Analysis & Export (Аналітика та візуалізація)

Фінальний етап включає:
- генерацію зведених таблиць
- розрахунок медіанних зарплат
- частотний аналіз технологій
- побудову інтерактивних графіків

---

# 📂 Структура репозиторію

```text
project_root/
│
├─ data/
│  ├─ raw/                  # Сирі HTML-дампи сторінок DOU
│  └─ processed_v2/         # Очищений фінальний CSV-датасет
│
├─ src/
│  ├─ __init__.py
│  ├─ scraper.py            # Логіка збору вакансій
│  ├─ cleaner.py            # Очищення тексту та зарплат
│  └─ skills_extractor.py   # NLP-модуль витягування технологій
│
├─ notebooks/
│  └─ final_demo.ipynb      # Google Colab demo
│
├─ requirements.txt         # Залежності проєкту
│
└─ README.md                # Технічна документація
```

---

# 🛠 Технологічний стек

## Базова мова
- Python 3.9+

## Збір даних
- `requests`
- `beautifulsoup4`
- `lxml`

## Аналіз та трансформація
- `pandas`
- `numpy`
- `regex`

## Візуалізація
- `matplotlib`
- `seaborn`

---

# 🚀 Інструкція із розгортання та запуску

## 1. Клонування репозиторію

```bash
git clone https://github.com/your-username/dou-vacancies-pipeline.git
cd dou-vacancies-pipeline
```

---

## 2. Створення virtual environment

### Linux / macOS

```bash
python -m venv venv
source venv/bin/activate
```

### Windows

```bash
python -m venv venv
venv\Scripts\activate
```

---

## 3. Встановлення залежностей

```bash
pip install -r requirements.txt
```

---

## 4. Запуск pipeline

```bash
python src/scraper.py
python src/cleaner.py
```

---

# 📊 Структура фінального датасету (Data Schema)

Файл `processed_dou_vacancies.csv` містить такі поля:

| Поле | Тип | Опис |
|---|---|---|
| `id` | Int64 | Унікальний ID вакансії |
| `title` | String | Назва посади |
| `company` | String | Назва компанії |
| `location` | String | Місто або Remote |
| `experience` | Int64 | Мінімальний required experience |
| `salary_min` | Float64 | Нижня межа зарплати |
| `salary_max` | Float64 | Верхня межа зарплати |
| `extracted_skills` | String | Список знайдених технологій |

---

# 🔗 Демонстрація в Google Colab

Повну інтерактивну аналітику та графіки можна запустити в Google Colab:

```text
👉 Відкрити DOU Vacancies Analytics Demo у Google Colab
```

---

# ✍️ Висновок та результати аудиту

Конвеєр успішно вирішує задачу швидкого моніторингу українського ІТ-ринку праці.

Ключові переваги системи:

- модульна ETL-архітектура
- ізольовані компоненти pipeline
- масштабованість NLP-модуля
- простота інтеграції нових джерел даних
- готовність до інтеграції з BI-платформами

Завдяки слабкому зв’язуванню компонентів, оновлення scraper-модуля або розширення правил NLP-екстракції не потребує перебудови всієї системи.