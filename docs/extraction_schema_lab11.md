# Специфікація Extraction Schema: Lab 11 (DOU Vacancies)

Цей документ описує структуру даних та правила валідації для автоматизованого витягування метаданих з ІТ-вакансій за допомогою LLM.

### 1. Extraction-задача
**Мета:** Перетворення неструктурованого тексту вакансій (мікс укр/англ, сленг) у структурований профіль для HR-аналітики.
**Кейс:** Парсинг вимог та умов праці з порталу DOU.ua.

### 2. Склад полів JSON
1. `position` (string): Повна назва посади.
2. `skills` (array of strings): Набір технологій та хард-скілів.
3. `years_of_experience` (number): Мінімальний необхідний стаж (число).
4. `salary_range` (string): Текстовий опис зарплатної вилки.
5. `work_format` (enum): Формат роботи (remote, office, hybrid, not_specified).
6. `english_level` (string): Вимоги до рівня володіння мовою.

### 3. Обов'язкові поля (Required)
Для успішної валідації об'єкт **мусить** містити ключі: `position`, `skills`, `work_format`.

### 4. JSON Schema (Draft 7)
```json
{
  "$schema": "[http://json-schema.org/draft-07/schema#](http://json-schema.org/draft-07/schema#)",
  "type": "object",
  "properties": {
    "position": { "type": "string" },
    "skills": { "type": "array", "items": { "type": "string" } },
    "years_of_experience": { "type": ["number", "null"] },
    "salary_range": { "type": ["string", "null"] },
    "work_format": { "type": "string", "enum": ["remote", "office", "hybrid", "not_specified"] },
    "english_level": { "type": ["string", "null"] }
  },
  "required": ["position", "skills", "work_format"],
  "additionalProperties": false
}
```

### 5. Правила для Null / Missing Values
* Якщо параметр (наприклад, зарплата) не згадується — поле отримує значення `null`.
* Якщо список скілів порожній — поле отримує `[]`.
* Моделі суворо заборонено домислювати значення (hallucination control).

### 6. Проблемні поля (Критичні точки)
* **years_of_experience**: Найскладніше поле. Модель схильна повертати рядок (напр. "3+") замість чистого числа `3`, що призводить до Schema Error.
* **work_format**: Помилки виникають через переклад значень українською (напр. "віддалено") замість використання суворих ключів Enum, визначених у схемі.

### 7. Ефективність Repair Loop
Цикл відновлення (Repair Loop) у нашому пайплайні успішно виправляє помилки форматування (наприклад, наявність зайвого тексту навколо JSON), проте виявився менш ефективним у виправленні системних помилок типізації. Найкращим рішенням для таких випадків є впровадження Structured Outputs на рівні системних інструкцій моделі.