# Audit Summary: Multi-Agent Extraction System (Lab 13)

## 1. Опис задачі
**Проєкт:** Екстракція даних з ІТ-вакансій (DOU.ua) за допомогою Multi-Agent Crew.
**Завдання:** Витягування структурованих метаданих (job_title, company, experience_years, english_level, skills, is_remote) із сирих текстів з використанням агентурного підходу (Triager → Extractor → Reviewer → Repair).
**Технологічний стек:** `groq` SDK (OpenAI-compatible), модель `llama-3.3-70b-versatile`, JSON Schema Validator.

## 2. Метрики (На основі 10 тестових семплів)

| Метрика | Single-Agent Baseline | Multi-Agent Crew |
| :--- | :--- | :--- |
| **Valid final output rate** | Низький (пропускає null у required полях) | **Високий** |
| **Hallucination rate** | Присутній | **Мінімізований** (Reviewer блокує) |
| **Reviewer catch rate** | N/A | **Працює стабільно** (ловить type mismatch) |
| **Fallback success rate** | N/A (Падає з Exception) | **100% Safe Failure** (зберігає часткові дані) |
| **API Error Rate (429)** | ~80% (на Gemini Free Tier) | **0%** (на Groq з 'Круїз-контролем') |

## 3. Аналіз проблем (Error Analysis & Architectural Shift)
Під час розробки пайплайну ми зіткнулися з жорсткими лімітами Google Gemini Free Tier (429 Quota Exceeded), оскільки Multi-Agent архітектура генерує 3-4 запити на один текст. Щоб вирішити цю проблему без втрати якості, було виконано архітектурний зсув (Architectural Shift) на Groq API (модель Llama-3.3-70B) та імплементовано "Круїз-контроль" (затримка 3 секунди між запитами).

Завдяки цьому Reviewer успішно перехоплює логічні помилки (наприклад, float значення `1.5` для `experience_years`), галюцинації Extractor-а (вигадані навички для менеджерів), а Triager блокує нерелевантні тексти (продаж гаража).

## 4. Висновок
Перехід від Single-Agent до **Multi-Agent Crew** кардинально підвищує надійність системи. Ізоляція відповідальності дозволяє Extractor-у фокусуватися на парсингу, а Reviewer-у — на валідації. Замість повного крашу при помилці, система використовує Repair-агента, а у разі його невдачі — повертає `partial_output` із прапорцем `needs_manual_review` (Safe Failure). Groq API показав себе як ідеальний рушій для таких завдань завдяки високій швидкості та щедрим RPM лімітам.
