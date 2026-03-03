import re
import pandas as pd


# Rules

# rule 1: витягування років досвіду
EXP = re.compile(
    r"(?:досвід[уа]?|experience|exp)[\s\w]{0,20}?(\d+(?:[.,]\d+)?\s*(?:\+|-)?\s*(?:\d+)?(?:-х)?)\s*(?:рок|років|years|yrs|р\.)",
    re.IGNORECASE
)

# rule 2: витягування зарплати
SAL = re.compile(
    r"(?:зп|salary|дохід|rate)[\s\w]{0,15}?\$?\s*(\d{1,3}(?:[ \.,]\d{3})*(?:k)?\s*(?:-\s*\d{1,3}(?:[ \.,]\d{3})*(?:k)?)?)\s*(?:\$|usd|eur|₴)",
    re.IGNORECASE
)

def extract_entities(text: str) -> dict:
    exp_match = EXP.search(text)
    sal_match = SAL.search(text)
    
    return {
        "text": text,
        "extracted_exp": exp_match.group(1).strip() if exp_match else None,
        "extracted_salary": sal_match.group(1).strip() if sal_match else None
    }


# 2. Gold Set
gold_set = [
    {"text": "Шукаємо Data Engineer з досвідом від 2 років.", "expected_exp": "2", "expected_salary": None},
    {"text": "Пропонуємо ЗП 3000-4500$ на місяць.", "expected_exp": None, "expected_salary": "3000-4500"},

    # non-working
    {"text": "Наша компанія на ринку вже 10 років.", "expected_exp": None, "expected_salary": None},
    {"text": "Цей проєкт розрахований на 1.5 роки.", "expected_exp": None, "expected_salary": None},
    {"text": "Перегляд ЗП та бонусів кожні 6 місяців.", "expected_exp": None, "expected_salary": None},
    {"text": "Бонус за успішну рекомендацію кандидата 1000$.", "expected_exp": None, "expected_salary": None},
    {"text": "У нашій команді працює більше 2000+ спеціалістів.", "expected_exp": None, "expected_salary": None},
    
    # edge cases
    {"text": "Вимоги: 1.5+ роки досвіду з Python.", "expected_exp": "1.5+", "expected_salary": None},
    {"text": "Маєте досвід роботи 1,5-2 роки? Пишіть!", "expected_exp": "1,5-2", "expected_salary": None},
    {"text": "Очікувана ЗП: 3 000 - 4 000 $", "expected_exp": None, "expected_salary": "3 000 - 4 000"},
    {"text": "Salary for this position is up to 4k USD.", "expected_exp": None, "expected_salary": "4k"},
    {"text": "Шукаємо мідла, досвід від 2-х років обов'язковий.", "expected_exp": "2-х", "expected_salary": None}
]


if __name__ == "__main__":
    
    res = []
    for i in gold_set:
        extr = extract_entities(i["text"])
        exp_match = extr["extracted_exp"] == i["expected_exp"]
        sal_match = extr["extracted_salary"] == i["expected_salary"]
        status = "pass" if exp_match and sal_match else "fail"
        
        res.append({
            "Text": i["text"][:40] + "...",
            "Exp (Pred)": extr["extracted_exp"],
            "Exp (True)": i["expected_exp"],
            "Sal (Pred)": extr["extracted_salary"],
            "Sal (True)": i["expected_salary"],
            "Status": status
        })
        

    df_res = pd.DataFrame(res)
    print(df_res.to_string(index=False))
