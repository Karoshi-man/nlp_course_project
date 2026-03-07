"""
Rule-based Information Extraction module for DOU.ua vacancies.
Extracts: SALARY, EXPERIENCE_YEARS, ENGLISH_LEVEL.
"""

import re
import json
import os

# Завантаження словника для англійської
def load_english_dict():
    # Розраховуємо шлях відносно розташування цього скрипта
    base_dir = os.path.dirname(os.path.dirname(__file__))
    dict_path = os.path.join(base_dir, 'resources', 'english_levels.json')
    
    try:
        with open(dict_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"⚠️ Словник не знайдено за шляхом: {dict_path}")
        return {}

ENGLISH_DICT = load_english_dict()

# --- 1. ПРАВИЛА ДЛЯ ЗАРПЛАТИ (SALARY) ---
def extract_salary(text: str) -> list:
    results = []
    # Патерн шукає: числа (з можливими 'k' та пробілами/комами) поруч із валютою $, USD, UAH, грн
    # Приклади: "$2000-4000", "від 3k до 4k USD", "3000 $"
    # (?<!\d) - негативний lookbehind, щоб не витягувати кінцівки довгих чисел
    pattern = r'(?i)(?:\$|usd)?\s*(?<!\d)(\d{1,3}(?:[ .,]\d{3})*|\d{1,2}[kк])\s*(?:-|–|до|to)?\s*(?:\$|usd)?\s*(\d{1,3}(?:[ .,]\d{3})*|\d{1,2}[kк])?\s*(usd|\$|uah|грн)'
    
    for match in re.finditer(pattern, text):
        raw_min = match.group(1)
        raw_max = match.group(2)
        raw_curr = match.group(3).lower() if match.group(3) else '$'
        
        # Функція для очищення чисел (видалення пробілів, переведення 'k' у 000)
        def clean_num(num_str):
            if not num_str: return None
            num_str = num_str.lower().replace(' ', '').replace(',', '').replace('.', '')
            if 'k' in num_str or 'к' in num_str:
                return int(re.sub(r'[kк]', '', num_str)) * 1000
            return int(num_str)

        try:
            val_min = clean_num(raw_min)
            val_max = clean_num(raw_max) if raw_max else val_min
            currency = 'UAH' if 'uah' in raw_curr or 'грн' in raw_curr else 'USD'
            
            # Валідація "на здоровий глузд" (щоб відсіяти випадкові версії ПЗ або відсотки)
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

# --- 2. ПРАВИЛА ДЛЯ ДОСВІДУ (EXPERIENCE_YEARS) ---
def extract_experience(text: str) -> list:
    results = []
    # Шукаємо контекст досвіду: цифра (можливо з дробом) + слово "роки", "years" тощо
    pattern = r'(?i)(?:досвід[а-я]*|experience|від|from)?\s*(?<!\d)(\d+[,.]?\d*)\s*(?:\+|[-–]\s*\d+)?\s*(роки|років|року|years|year|yrs)\b'
    
    for match in re.finditer(pattern, text):
        num_str = match.group(1).replace(',', '.')
        try:
            exp_val = float(num_str)
            # Фільтруємо вік (від 18 років) та дивні числа
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

# --- 3. ПРАВИЛА ДЛЯ АНГЛІЙСЬКОЇ (ENGLISH_LEVEL) ---
def extract_english(text: str) -> list:
    results = []
    if not ENGLISH_DICT:
        return results

    # Створюємо регулярку зі словника, сортуємо ключі за довжиною (щоб upper-intermediate шукався раніше за intermediate)
    sorted_keys = sorted(ENGLISH_DICT.keys(), key=len, reverse=True)
    # Екрануємо ключі (для безпеки) та додаємо word boundaries \b, щоб уникнути B2B
    escaped_keys = [re.escape(k) for k in sorted_keys]
    pattern = r'(?i)\b(' + '|'.join(escaped_keys) + r')\b'
    
    # Шукаємо всі згадки
    for match in re.finditer(pattern, text):
        raw_val = match.group(1).lower()
        # Додаткова перевірка: якщо це просто "C1" чи "B2", перевіряємо, чи немає поруч "B2B" або "C++"
        # \b вже частково це робить, але краще перестрахуватися
        
        normalized_val = ENGLISH_DICT.get(raw_val)
        
        results.append({
            "field_type": "ENGLISH_LEVEL",
            "value": normalized_val,
            "start_char": match.start(),
            "end_char": match.end(),
            "method": "dictionary_match"
        })
        
    return results

# --- ГОЛОВНА ФУНКЦІЯ ---
def extract_all(text: str) -> list:
    """Проганяє текст через усі правила та повертає відсортований список знайдених сутностей."""
    if not isinstance(text, str) or not text.strip():
        return []
        
    all_entities = []
    all_entities.extend(extract_salary(text))
    all_entities.extend(extract_experience(text))
    all_entities.extend(extract_english(text))
    
    # Сортуємо по позиції в тексті (зліва направо)
    all_entities.sort(key=lambda x: x['start_char'])
    return all_entities

if __name__ == "__main__":
    # Локальний тест
    sample = "Шукаємо Data Engineer з досвідом 2.5 роки. Зарплата від 3k до 4.5k USD. English: Upper-Intermediate."
    print("Тестовий текст:", sample)
    print(json.dumps(extract_all(sample), indent=2, ensure_ascii=False))