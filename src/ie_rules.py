import re
import json
import os

def load_english_dict():
    base_dir = os.path.dirname(os.path.dirname(__file__))
    dict_path = os.path.join(base_dir, 'resources', 'english_levels.json')
    
    try:
        with open(dict_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"⚠️ Словник не знайдено за шляхом: {dict_path}")
        return {}

ENGLISH_DICT = load_english_dict()

def extract_salary(text: str) -> list:
    results = []
    pattern = r'(?i)(?:\$|usd)?\s*(?<![\d.])(\d{1,3}(?:[ .,]\d{3})*|\d{1,2}(?:[.,]\d{1,2})?[kк])\s*(?:-|–|до|to)?\s*(?:\$|usd)?\s*(\d{1,3}(?:[ .,]\d{3})*|\d{1,2}(?:[.,]\d{1,2})?[kк])?\s*(usd|\$|uah|грн)'
    
    for match in re.finditer(pattern, text):
        raw_min = match.group(1)
        raw_max = match.group(2)
        raw_curr = match.group(3).lower() if match.group(3) else '$'
        
        def clean_num(num_str):
            if not num_str: return None
            num_str = num_str.lower().replace(' ', '').replace(',', '.')
            if 'k' in num_str or 'к' in num_str:
                num_str = re.sub(r'[kк]', '', num_str)
                return int(float(num_str) * 1000)
            num_str = num_str.replace('.', '')
            return int(num_str)

        try:
            val_min = clean_num(raw_min)
            val_max = clean_num(raw_max) if raw_max else val_min
            currency = 'UAH' if 'uah' in raw_curr or 'грн' in raw_curr else 'USD'
            
            if val_min < 200 or val_min > 200000:
                continue

            results.append({
                "field_type": "SALARY",
                "value": {"min": val_min, "max": val_max, "currency": currency},
                "start_char": match.start(),
                "end_char": match.end(),
                "method": "regex_salary"
            })
        except ValueError:
            continue
            
    return results


def extract_experience(text: str) -> list:
    results = []
    pattern = r'(?i)(?:досвід[а-я]*|experience|від|from)?\s*(?<!\d)(\d+[,.]?\d*)\s*(?:\+|[-–]\s*\d+)?\s*(роки|років|року|years|year|yrs)\b'
    
    for match in re.finditer(pattern, text):
        num_str = match.group(1).replace(',', '.')
        try:
            exp_val = float(num_str)
            if exp_val > 15 or exp_val < 0.5:
                continue
                
            results.append({
                "field_type": "EXPERIENCE_YEARS",
                "value": exp_val,
                "start_char": match.start(),
                "end_char": match.end(),
                "method": "regex_experience"
            })
        except ValueError:
            continue
            
    return results


def extract_english(text: str) -> list:
    results = []
    if not ENGLISH_DICT:
        return results
    sorted_keys = sorted(ENGLISH_DICT.keys(), key=len, reverse=True)
    escaped_keys = [re.escape(k) for k in sorted_keys]
    pattern = r'(?i)\b(' + '|'.join(escaped_keys) + r')\b'
    
    for match in re.finditer(pattern, text):
        raw_val = match.group(1).lower()
        normalized_val = ENGLISH_DICT.get(raw_val)   
        results.append({
            "field_type": "ENGLISH_LEVEL",
            "value": normalized_val,
            "start_char": match.start(),
            "end_char": match.end(),
            "method": "dictionary_match"
        })
        
    return results

def extract_all(text: str) -> list:
    """
    Проганяє текст через усі правила та повертає 
    відсортований список знайдених сутностей
    """
    if not isinstance(text, str) or not text.strip():
        return []
    all_entities = []
    all_entities.extend(extract_salary(text))
    all_entities.extend(extract_experience(text))
    all_entities.extend(extract_english(text))
    all_entities.sort(key=lambda x: x['start_char'])
    return all_entities

if __name__ == "__main__":
    sample = "Шукаємо Data Engineer з досвідом 2.5 роки. Зарплата від 3k до 4.5k USD. English: Upper-Intermediate."
    print("Тестовий текст:", sample)
    print(json.dumps(extract_all(sample), indent=2, ensure_ascii=False))