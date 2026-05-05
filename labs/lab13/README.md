# Lab 13: Multi-Agent Extraction System (Crew Workflow)

## 1. Який use case обрано
Екстракція структурованих метаданих (формат JSON) з неструктурованих текстів ІТ-вакансій (наприклад, з DOU.ua). Ціль: автоматично витягувати посаду, необхідний досвід, навички та формат роботи.

## 2. Які агенти є в crew
Система складається з 4 спеціалізованих агентів:
1. **Triager** (Класифікатор)
2. **Extractor** (Парсер)
3. **QA Reviewer** (Контролер якості)
4. **Repair Agent** (Ремонтник)

## 3. Який workflow
Лінійний пайплайн з циклом виправлення:
`Input Text` ➔ `Triager` ➔ `Extractor` ➔ `QA Reviewer` ➔ `[Repair Loop]` ➔ `Final JSON`.

## 4. Які delegation rules
*   Якщо текст не є ІТ-вакансією (визначає Triager) ➔ пропускаємо Extractor, йдемо у Fallback.
*   Extractor генерує JSON ➔ обов'язково передає його QA Reviewer-у.
*   Якщо Reviewer дає `accept` ➔ зберігаємо результат.
*   Якщо Reviewer дає `repair_needed` ➔ делегуємо Repair Agent-у.
*   Якщо Reviewer знаходить критичні суперечності або Repair не справляється ➔ делегуємо у Fallback.

## 5. Як працює Reviewer
QA Reviewer не парсить текст, він порівнює згенерований JSON із початковим текстом та схемою. Він шукає:
*   Відсутність обов'язкових полів.
*   Невідповідність типів даних (наприклад, float замість integer).
*   Галюцинації (вигадані навички).
*   Логічні суперечності (вказано remote, хоча в тексті тільки офіс).

## 6. Як працює fallback
Впроваджено концепцію **Safe Failure**. Якщо система не може надійно розпарсити текст, вона не падає з Exception (краш), а створює Fallback-відповідь: повертає всі дані, які вдалося витягти (`partial_output`), і встановлює прапорець `needs_manual_review: true`.

## 7. Як запускати notebook
1. Встановіть залежності: `pip install groq python-dotenv tqdm pandas`
2. Отримайте ключ на `console.groq.com` і додайте його у файл `.env` як `GROQ_API_KEY=ваш_ключ`
3. Відкрийте Jupyter Notebook / Google Colab.
4. Запустіть усі комірки послідовно (або "Run All").

## 8. Де лежать logs
Всі артефакти генеруються та зберігаються у папці `docs/`:
*   `docs/crew_logs_lab13.jsonl` — детальні логи кожного кроку для всіх тест-кейсів.
*   `docs/audit_summary_lab13.md` — порівняння з Baseline та метрики.
*   `docs/crew_notes_lab13.md` — технічна рефлексія архітектури.

## 9. Які метрики
В результаті тестування ми відстежували:
*   **Valid final output rate**
*   **Missing required fields rate**
*   **Reviewer catch rate** (скільки помилок спіймав Reviewer)
*   **Fallback success rate** (чи успішно спрацював Safe Failure)
*   **Manual review rate**

## 10. Головний висновок
Перехід від Single-Agent Baseline до Multi-Agent Crew кардинально підвищує стабільність парсингу. Ізоляція ролей (парсинг окремо, перевірка окремо) дозволяє відловити галюцинації та помилки типізації, а використання Groq API вирішує проблему жорстких лімітів і довгого очікування.