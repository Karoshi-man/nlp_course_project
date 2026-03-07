# Audit Summary Lab 4: Rule-based Information Extraction

## 1. Загальна інформація
* **Метод:** Rule-based (Regex + Dictionaries)
* **Поля для екстракції:** `SALARY`, `EXPERIENCE_YEARS`, `ENGLISH_LEVEL`

## 2. Метрики якості (Gold Subset)
| Field Type | Precision | True Positives | False Positives |
| :--- | :---: | :---: | :---: |
| **SALARY** | 0.67 | 2 | 1 |
| **EXPERIENCE_YEARS** | 0.86 | 6 | 0 |
| **ENGLISH_LEVEL** | 1.00 | 8 | 0 |

## 3. Error Analysis
Алгоритм успішно обробляє edge cases (B2B, вік 18 років, 4.5k зарплата) завдяки впровадженим евристикам та регулярним виразам із негативним lookbehind.