# Job vacancies from DOU: extraction

![Python](https://img.shields.io/badge/Python-3.14-blue)
![NLP](https://img.shields.io/badge/NLP-Information%20Extraction-green)
![Status](https://img.shields.io/badge/Status-Active%20Development-orange)

Цей репозиторій містить курсовий проєкт з дисципліни **"Обробка людської мови"**. 
Мета проєкту - створення системи для автоматичного витягування інформації (Skill Extraction / NER) з описів вакансій на українському IT-ринку (платформа DOU.ua).

## 🎯 Мета
Розробити пайплайн для структуризації неструктурованих текстів вакансій. Фокус - виділення ключових сутностей:
- **Технології (Hard Skills)**: Python, SQL, Node.js, C++.
- **Доменні сутності**: бібліотеки, фреймворки, хмарні платформи.
- **Умови (IE)**: Зарплатні вилки, роки досвіду, рівень англійської мови.

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
│   ├── audit_summary_lab2.md   # Звіт про результати препроцесингу
│   ├── audit_summary_lab3.md   # Звіт з аналізу помилок лематизації та POS-тегінгу
│   └── audit_summary_lab4.md   # Звіт з Information Extraction (Regex + Dictionaries)
├── labs/
│   ├── lab01/               # Опис Лабораторної №1
│   ├── lab02/               # Опис Лабораторної №2
│   ├── lab03/               # Опис Лабораторної №3
│   └── lab04/               # Опис Лабораторної №4
├── notebooks/
│   ├── lab1_data_audit.ipynb               # Lab 1: Аналіз та аудит
│   ├── lab2_cleaning_normalization.ipynb   # Lab 2: Запуск пайплайну
│   ├── lab3_lemma_pos_baseline.ipynb       # Lab 3: Оцінка Lemma/POS
│   └── lab4_rule_based_ie.ipynb            # Lab 4: Екстракція сутностей
├── src/
│   ├── preprocess.py        # Детермінований модуль очистки (Regex, ftfy)
│   ├── ling_features.py     # Модуль витягування лінгвістичних ознак (Stanza)
│   ├── rule_based_baseline.py # Скрипт Regex-правил
│   └── ie_rules.py          # Модуль IE для Лаби 4
├── tests/
│   ├── edge_cases.jsonl        # Тестові сценарії для препроцесингу
│   ├── ling_edge_cases.jsonl   # Хардкорні приклади для Error Analysis (Lab 3)
│   ├── ie_edge_cases.jsonl     # Edge Cases для IE (Lab 4)
│   └── gold_subset_50.jsonl    # Gold Subset для вимірювання Precision
├── README.md
└── requirements.txt
```

## 🛠 Технологічний стек
Проєкт реалізовано без використання Generative AI для обробки даних (відповідно до вимог курсу). Використовуються класичні інженерні методи:
* **Data Collection:** `BeautifulSoup`, `requests`.
* **Preprocessing & Normalization:** `regex` (просунутий пошук), `ftfy` (виправлення mojibake), `pandas`.
* **Linguistic Processing:** `Stanza` (POS-тегінг, лематизація).
* **Information Extraction:** Rule-based підхід (Regex + Dictionaries) з фокусом на Precision-first.

## 📊 Етапи розробки
- [x] **Lab 1:** Збір датасету з DOU, базовий аудит, розробка правил розмітки.
- [x] **Lab 2:** Детермінована очистка, маскування PII, розумне розбиття на речення із захистом IT-термінів.
- [x] **Lab 3:** Інтеграція Stanza, проведення Error Analysis на ІТ-сутностях, побудова та тестування Rule-based Baseline на лематизованому та сирому текстах.
- [x] **Lab 4:** Реалізовано Rule-based Information Extraction (Regex + Dictionaries) для витягування полів SALARY, EXPERIENCE_YEARS, ENGLISH_LEVEL.

## 🚀 Як запустити

1. **Клонуйте репозиторій:**
   ```bash
   git clone https://github.com/Karoshi-man/nlp_course_project.git
   cd nlp_course_project
   ```

2. **Створіть віртуальне середовище та встановіть залежності:**
   ```bash
   python -m venv .venv
   
   # Для Windows:
   .venv\Scripts\activate
   # Для Linux/Mac:
   source .venv/bin/activate
   
   pip install -r requirements.txt
   ```

3. **Запуск специфічних етапів (Jupyter Notebooks):**
   Усі етапи пайплайну ізольовані у відповідних ноутбуках. Відкрийте папку `notebooks/` та запустіть потрібний файл у Jupyter або VS Code (виконайте "Run All"):
   * 🧹 Очистка даних: `lab2_cleaning_normalization.ipynb`
   * 📝 POS/Lemma Baseline: `lab3_lemma_pos_baseline.ipynb`
   * 🔍 Екстракція сутностей (IE): `lab4_rule_based_ie.ipynb`

---
*Author: Martin Fesenko, Group PMID-11*
