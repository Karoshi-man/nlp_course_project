# Job vacancies from DOU: extraction

![Python](https://img.shields.io/badge/Python-3.14-blue)
![NLP](https://img.shields.io/badge/NLP-Extraction-green)
![Status](https://img.shields.io/badge/Status-Lab%202%3A%20Cleaning%20Pipeline-orange)

Цей репозиторій містить курсовий проєкт з дисципліни **"Обробка людської мови" (NLP)** у Львівській політехніці. 
Мета проєкту - створення системи для автоматичного витягування інформації (Skill Extraction / NER) з описів вакансій на українському IT-ринку (платформа DOU).

## 🎯 Мета
Розробити пайплайн для структуризації неструктурованих текстів вакансій. Фокус — виділення ключових сутностей:
- **Технології (Hard Skills)**: Python, SQL, Node.js, C++.
- **Доменні сутності**: бібліотеки, фреймворки, хмарні платформи.

## 📂 Структура репозиторію

```text
├── data/
│   ├── raw/                 # "Сирі" дані від скрейпера (з HTML-артефактами)
│   ├── sample/              # Вибірки для тестування пайплайну (sample_raw.csv)
│   └── processed_v2/        # Очищені тексти після Лаби 2
├── docs/
│   ├── dataset_card.md         # Документація та аудит датасету
│   ├── labeling_guidelines.md  # Правила розмітки сутностей
│   ├── preprocess_policy.md    # Політика очистки та нормалізації
│   └── audit_summary_lab2.md   # Звіт про результати препроцесингу
├── labs/
│   ├── lab01/               # Опис Лабораторної №1
│   └── lab02/               # Опис Лабораторної №2
├── notebooks/
│   ├── lab1_data_audit.ipynb               # Lab 1: Аналіз та аудит
│   └── lab2_cleaning_normalization.ipynb   # Lab 2: Запуск пайплайну
├── src/
│   └── preprocess.py        # Детермінований модуль очистки (Regex, ftfy)
├── tests/
│   └── edge_cases.jsonl     # Тестові сценарії для перевірки пайплайну
├── README.md
└── requirements.txt

## 🛠 Технологічний стек
Проєкт реалізовано без використання Generative AI для обробки даних (відповідно до вимог курсу). Використовуються класичні інженерні методи:
* **Data Collection:** `BeautifulSoup`, `requests`.
* **Preprocessing & Normalization:** `regex` (просунутий пошук), `ftfy` (виправлення mojibake), `pandas`.
* **Testing:** Детерміновані тести на ідемпотентність та збереження контексту (Custom Sentence Splitter).

## 📊 Етапи розробки
- [x] **Lab 1:** Збір датасету з DOU, базовий аудит, розробка правил розмітки.
- [x] **Lab 2:** Детермінована очистка, маскування PII, розумне розбиття на речення із захистом IT-термінів.
- [ ] **Lab 3:** ...

## 🚀 Як запустити
1. Клонуйте репозиторій:
   ```bash
   git clone [https://github.com/Karoshi-man/nlp_course_project.git](https://github.com/Karoshi-man/nlp_course_project.git)
   ```
2. Створіть віртуальне середовище та встановіть залежності:
   ```bash
   python -m venv .venv
   .venv\Scripts\activate
   pip install -r requirements.txt
   ```
3. Запустіть пайплайн очистки:
   Відкрийте `notebooks/lab2_cleaning_normalization.ipynb` у Jupyter або VS Code та виконайте всі клітинки.

---
*Author: Martin Fesenko, Group PMID-11*