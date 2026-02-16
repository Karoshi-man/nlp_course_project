# Dataset Card: DOU Vacancies for Skill Extraction

## Project Info
- **Task:** B. Extraction / NER
- **Input:** Текст вакансії (description)
- **Output:** Список технічних скілів та технологій

## Data Source
- **Source:** https://jobs.dou.ua/
- **Tooling:** Selenium + Python

## Volume & Stats
- **Total Texts:** 583 (raw), 583 (processed)
- **Mean Length:** ~463 words
- **Classes:** AI/ML, Python, Data Engineer, Data Science

## Cleaning Process
- Removed HTML tags (via Selenium .text)
- Replaced URLs with `<URL>`
- Replaced Emails with `<EMAIL>`
- Replaced Phone numbers with `<PHONE>`
- Filtered out short texts (< 10 words) - *None found in this batch*

## Risks
- Bilingual texts (UA/EN mix) - might confuse simple NER models.
- Non-standard formatting of lists - some bullet points merged into sentences.