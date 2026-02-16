# Labeling Guidelines for Skill Extraction

## Entities to Extract
Ми розмічаємо одну категорію сутностей: **SKILL**.

### SKILL (Технологія / Навичка)
**Включає:**
- Мови програмування (Python, C++, Java)
- Бібліотеки та фреймворки (Pandas, PyTorch, Django, React)
- Бази даних (PostgreSQL, MongoDB)
- Хмарні платформи (AWS, Azure, GCP)
- Інструменти (Docker, Kubernetes, Git)
- Концепції CS/DS (OOP, Machine Learning, NLP, CI/CD)

**Не включає:**
- Soft skills (communication, teamwork, English level)
- Загальні слова (software, database, computer, algorithm)
- Назви компаній (якщо це не назва їхнього інструменту)

### Examples
1. "Experience with **Python** and **Pandas** is required." -> [SKILL, SKILL]
2. "Knowledge of **AWS** cloud services." -> [SKILL]
3. "Good communication skills and upper-intermediate English." -> [NO TAGS]