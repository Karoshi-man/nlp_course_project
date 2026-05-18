# Knowledge Base: Read-only schema and dictionaries
TECH_VACANCY_SCHEMA = {
    "type": "object",
    "properties": {
        "technologies": {
            "type": "array",
            "items": {"type": "string"},
            "description": "List of programming languages, frameworks, or DBs."
        },
        "experience_years": {
            "type": ["integer", "null"],
            "description": "Minimum years of experience required. Null if not specified."
        }
    },
    "required": ["technologies", "experience_years"]
}

# Ключові слова для простого роутера
TECH_KEYWORDS = ["розробник", "developer", "engineer", "devops", "qa", "python", "java", "react", "c++", "data"]
NON_TECH_KEYWORDS = ["sales", "hr", "recruiter", "менеджер з продажу", "маркетолог", "seo"]