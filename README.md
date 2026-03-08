# Job vacancies from DOU: extraction

![Python](https://img.shields.io/badge/Python-3.14-blue)
![NLP](https://img.shields.io/badge/NLP-Information%20Extraction-green)
![Status](https://img.shields.io/badge/Status-Lab%202%3A%20Cleaning%20Pipeline-orange)

> **📍 Поточна гілка: `lab02`**
> Ця гілка містить результати виконання Лабораторної роботи №2. Головний фокус — побудова детермінованого пайплайну для очищення "сирого" HTML-тексту, нормалізації кодувань, маскування персональних даних (PII) та безпечного розбиття на речення (Sentence Splitting) із збереженням специфічних IT-термінів (наприклад, `Node.js`, `C++`). Звіти та метрики очистки знаходяться у `docs/audit_summary_lab2.md`.

Цей репозиторій містить курсовий проєкт з дисципліни **"Обробка людської мови" (NLP)**. 
Мета проєкту - створення системи для автоматичного витягування інформації (Skill Extraction / NER) з описів вакансій на українському IT-ринку (платформа DOU.ua).

## 🎯 Мета
Розробити пайплайн для структуризації неструктурованих текстів вакансій. Фокус - виділення ключових сутностей:
- **Технології (Hard Skills)**: Python, SQL, Node.js, C++.
- **Доменні сутності**: бібліотеки, фреймворки, хмарні платформи.
- **Умови (IE)**: Зарплатні вилки, роки досвіду.

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
│   └── lab2_cleaning_normalization.ipynb   # Lab 2: Запуск пайплайну очистки
├── src/
│   └── preprocess.py        # Детермінований модуль очистки (Regex, ftfy)
├── tests/
│   └── edge_cases.jsonl     # Тестові сценарії для перевірки пайплайну
├── README.md
└── requirements.txt
```

## 🛠 Технологічний стек
Проєкт реалізовано без використання Generative AI для обробки даних (відповідно до вимог курсу). Використовуються класичні інженерні методи:
* **Data Collection:** `BeautifulSoup`, `requests`.
* **Preprocessing & Normalization:** `regex` (просунутий пошук), `ftfy` (виправлення mojibake), `pandas`.
* **Testing:** Детерміновані тести на ідемпотентність та збереження контексту (Custom Sentence Splitter).

## 📊 Етапи розробки
- [x] **Lab 1:** Збір датасету з DOU, базовий аудит, розробка правил розмітки.
- [x] **Lab 2:** Детермінована очистка, маскування PII, розумне розбиття на речення із захистом IT-термінів.
- [ ] **Lab 3:** Інтеграція Stanza, проведення Error Analysis... (у розробці)

## 🚀 Як запустити

1. **Клонуйте репозиторій:**
   ```bash
   git clone [https://github.com/Karoshi-man/nlp_course_project.git](https://github.com/Karoshi-man/nlp_course_project.git)
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

3. **Запустіть пайплайн очистки:**
   Відкрийте файл `notebooks/lab2_cleaning_normalization.ipynb` у Jupyter або VS Code та виконайте всі клітинки ("Run All"). Ноутбук автоматично імпортує правила з `src/preprocess.py` та збереже очищені дані у папку `processed_v2`.

---
*Author: Martin Fesenko, Group PMID-11*
