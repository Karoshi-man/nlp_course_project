import pandas as pd
import json
import re
import os

def generate_edge_cases():
    # Прості відносні шляхи (працюють, якщо запускати з кореня)
    csv_path = "data/raw/raw.csv"
    output_path = "tests/edge_cases.jsonl"

    if not os.path.exists(csv_path):
        print(f"❌ Помилка: Не бачу файл {csv_path}")
        print(f"Поточна папка: {os.getcwd()}")
        return

    # Завантажуємо
    df = pd.read_csv(csv_path)
    # Шукаємо текстову колонку
    text_col = 'description' if 'description' in df.columns else df.columns[0]
    texts = df[text_col].astype(str).dropna().unique()

    # Що шукаємо для "жирних" прикладів
    patterns = [
        (r"Facebook Twitter LinkedIn", "Видалення сміття DOU"),
        (r"(?i)(Node\.js|Vue\.js|\.NET)", "Збереження IT-крапок"),
        (r"(?i)(м\.|вул\.|т\.д\.)", "Українські скорочення"),
        (r"https?://\S+", "Маскування URL"),
        (r"\S+@\S+\.\S+", "Маскування Email"),
        (r"[«»`’\"—–]", "Нормалізація символів")
    ]

    edge_cases = []
    
    # 1. Шукаємо цікаві кейси за паттернами
    for pattern, desc in patterns:
        regex = re.compile(pattern)
        for t in texts:
            if regex.search(t):
                # Чистимо від зайвих переносів для зручності
                snippet = " ".join(t.split())[:180] + "..."
                edge_cases.append({
                    "id": f"ec_{len(edge_cases) + 1:02d}",
                    "raw_text": snippet,
                    "expected_behavior": desc
                })
                break # Беремо по 1-2 на кожен паттерн
        if len(edge_cases) >= 15: break

    # 2. Добиваємо до 20 випадковими
    while len(edge_cases) < 20:
        import random
        t = random.choice(texts)
        snippet = " ".join(t.split())[:180] + "..."
        edge_cases.append({
            "id": f"ec_{len(edge_cases) + 1:02d}",
            "raw_text": snippet,
            "expected_behavior": "Загальний препроцесинг"
        })

    # Зберігаємо
    os.makedirs("tests", exist_ok=True)
    with open(output_path, 'w', encoding='utf-8') as f:
        for ec in edge_cases:
            f.write(json.dumps(ec, ensure_ascii=False) + '\n')

    print(f"✅ Готово! 20 реальних кейсів збережено в {output_path}")

if __name__ == "__main__":
    generate_edge_cases()