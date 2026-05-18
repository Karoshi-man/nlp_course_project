import re

def extract_technologies(input_data: dict) -> dict:
    """
    Витягує назви мов програмування та технологій з тексту вакансії.
    Очікуваний input: {"text": "Шукаємо Python розробника з досвідом AWS та Docker"}
    """
    try:
        text = input_data.get("text", "").lower()
        if not text:
            raise ValueError("Field 'text' is missing or empty.")
            
        # Словник популярних технологій для матчингу
        tech_stack = [
            "python", "java", "javascript", "js", "typescript", "ts", "c++", "c#", "ruby", "go",
            "react", "angular", "vue", "node.js", "django", "fastapi", "spring",
            "aws", "gcp", "azure", "docker", "kubernetes", "k8s", "sql", "postgresql", "mysql",
            "mongodb", "redis", "git", "linux", "jira"
        ]

        found_tech = []
        for tech in tech_stack:
            # Шукаємо технології як окремі слова, щоб уникнути хибних спрацьовувань
            if re.search(rf'\b{re.escape(tech)}\b', text):
                found_tech.append(tech)

        return {
            "technologies_found": list(set(found_tech)),
            "count": len(found_tech)
        }
    except Exception as e:
        raise ValueError(f"Technology extraction failed: {str(e)}")

def detect_experience_years(input_data: dict) -> dict:
    """
    Витягує необхідні роки досвіду за допомогою регулярних виразів.
    Очікуваний input: {"text": "Досвід роботи 3+ роки"}
    """
    try:
        text = input_data.get("text", "").lower()
        if not text:
            raise ValueError("Field 'text' is missing or empty.")
            
        # Шукаємо патерни типу "2 роки", "3+ years", "від 1 року"
        patterns = [
            r'(\d+)\+?\s*(?:роки|років|рік|years?|yrs)',
            r'(?:від|from)\s*(\d+)\s*(?:років|роки|years?|yrs)',
            r'досвід.*?(?:від\s*)?(\d+)\s*(?:років|роки|years?)'
        ]
        
        years_found = []
        for pattern in patterns:
            matches = re.findall(pattern, text)
            years_found.extend([int(m) for m in matches])
            
        return {
            "years_mentioned": years_found,
            "min_experience_detected": min(years_found) if years_found else None
        }
    except Exception as e:
        raise ValueError(f"Experience detection failed: {str(e)}")

# Реєстр доступних інструментів
AVAILABLE_TOOLS = {
    "extract_technologies": extract_technologies,
    "detect_experience_years": detect_experience_years
}