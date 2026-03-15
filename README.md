# Job vacancies from DOU: extraction

![Python](https://img.shields.io/badge/Python-3.14-blue)
![NLP](https://img.shields.io/badge/NLP-Extraction-green)
![Status](https://img.shields.io/badge/Status-Lab%205%3A%20Split%20%26%20Leakage-orange)

Цей репозиторій містить курсовий проєкт з дисципліни **"Обробка людської мови" (NLP)**. 
Мета проєкту - створення системи для автоматичного витягування інформації (Skill Extraction / NER) з описів вакансій на українському IT-ринку (платформа DOU).

## 🎯 Мета
Розробити пайплайн для структуризації неструктурованих текстів вакансій. Фокус - виділення ключових сутностей:
- **Технології (Hard Skills)**: Python, SQL, Node.js, C++.
- **Доменні сутності**: бібліотеки, фреймворки, хмарні платформи.
- **Метадані**: Зарплатна вилка, необхідний досвід роботи, рівень англійської.

## 📂 Структура репозиторію

```text
├── data/
│   ├── raw/                 # "Сирі" дані від скрейпера (з HTML-артефактами)
│   ├── sample/              # Вибірки для тестування та ID сплітів (splits_*_ids.txt)
│   └── processed_v2/        # Очищені тексти після Лаби 2
├── docs/
│   ├── dataset_card.md             # Документація та аудит датасету
│   ├── labeling_guidelines.md      # Правила розмітки сутностей
│   ├── preprocess_policy.md        # Політика очистки та нормалізації
│   ├── leakage_risk_report_lab5.md # Звіт про ризики витоку даних
│   └── splits_manifest_lab5.json   # Маніфест розбиття даних
├── notebooks/
│   ├── lab1_data_audit.ipynb               # Lab 1: Аналіз та аудит
│   ├── lab2_cleaning_normalization.ipynb   # Lab 2: Запуск пайплайну очистки
│   ├── lab3_ling_features.ipynb            # Lab 3: Тестування лематизації (Stanza)
│   ├── lab4_rule_based_ie.ipynb            # Lab 4: Витяг сутностей (Regex + Dictionaries)
│   └── lab5_split_leakage_checks.ipynb     # Lab 5: Stratified Split та Leakage Checks
├── src/
│   ├── preprocess.py        # Детермінований модуль очистки (Regex, ftfy)
│   ├── extract.py           # Модуль rule-based екстракції (Lab 4)
│   └── split.py             # Модуль розбиття даних (Lab 5)
├── tests/
│   └── edge_cases.jsonl     # Тестові сценарії для перевірки пайплайну
├── README.md
└── requirements.txt
```

## 🛠 Технологічний стек
Проєкт реалізовано без використання Generative AI для обробки даних (відповідно до вимог курсу). Використовуються класичні інженерні ML/NLP методи:
* **Data Collection:** `BeautifulSoup`, `requests`.
* **Preprocessing & Normalization:** `regex` (просунутий пошук), `ftfy` (виправлення mojibake), `pandas`.
* **Information Extraction:** Rule-based методи (словники, window rules).
* **Machine Learning & Audit:** `scikit-learn` (TF-IDF, Cosine Similarity, Stratified Split).

## 📊 Етапи розробки
- [x] **Lab 1:** Збір датасету з DOU, базовий аудит, розробка правил розмітки.
- [x] **Lab 2:** Детермінована очистка, маскування PII, розумне розбиття на речення із захистом IT-термінів.
- [x] **Lab 3:** Тестування лінгвістичних ознак (Stanza). Відмова від лематизації для збереження цілісності IT-сутностей (C++, Node.js).
- [x] **Lab 4:** Впровадження Rule-based Information Extraction. Витяг `SALARY`, `EXPERIENCE_YEARS` та `ENGLISH_LEVEL` за допомогою словників та regex.
- [x] **Lab 5:** Детермінований Stratified Split (70/15/15) та глибокий аудит витоку даних (Data Leakage: Exact, Near-duplicates, Group, Metadata).

## 🚀 Як запустити
1. Клонуйте репозиторій:
   ```bash
   git clone https://github.com/Karoshi-man/nlp_course_project.git
   ```
2. Створіть віртуальне середовище та встановіть залежності:
   ```bash
   python -m venv .venv
   .venv\Scripts\activate   # Для Windows
   # source .venv/bin/activate # Для Linux/Mac
   pip install -r requirements.txt
   ```
3. Для перевірки останнього етапу (Lab 5), відкрийте та запустіть усі клітинки у `notebooks/lab5_split_leakage_checks.ipynb`. Ноутбук підтримує автоматичне завантаження даних у Google Colab.

---
*Author: Martin Fesenko, Group PMID-11*
