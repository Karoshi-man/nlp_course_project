import json
import re
from .flow_state import FlowState
from .schemas import TECH_KEYWORDS, NON_TECH_KEYWORDS, TECH_VACANCY_SCHEMA
from jsonschema import validate, ValidationError

def ingest(state: FlowState) -> FlowState:
    """Етап 1: Прийом та очищення даних."""
    if not state.raw_text or not state.raw_text.strip():
        state.status = "failed"
        state.errors.append("Input text is empty.")
        return state
        
    state.clean_text = " ".join(state.raw_text.split())
    state.status = "ingested"
    return state

def route(state: FlowState) -> FlowState:
    """Етап 2: Маршрутизація (визначаємо тип вакансії)."""
    if state.status == "failed": return state
    
    text_lower = state.clean_text.lower()
    
    if any(kw in text_lower for kw in TECH_KEYWORDS):
        state.route = "tech_extraction"
        state.routing_reason = "Found technical keywords in text."
    elif any(kw in text_lower for kw in NON_TECH_KEYWORDS):
        state.route = "non_tech_skip"
        state.routing_reason = "Found non-technical/HR keywords. Extraction not needed."
    else:
        state.route = "unknown"
        state.routing_reason = "No specific IT keywords found. Could be spam or vague."
        
    state.status = "routed"
    return state

def execute(state: FlowState, llm_caller) -> FlowState:
    """Етап 3: Виконання NLP задачі."""
    if state.status == "failed" or state.route != "tech_extraction":
        return state # Пропускаємо, якщо маршрут не вимагає екстракції
        
    prompt = f"""
    Analyze the following IT vacancy and extract the technologies and minimum years of experience.
    Output MUST strictly follow this JSON schema: {json.dumps(TECH_VACANCY_SCHEMA)}
    Vacancy text: '{state.clean_text}'
    """
    
    try:
        response = llm_caller(prompt)
        cleaned_response = response.replace("```json", "").replace("```", "").strip()
        state.extracted_data = json.loads(cleaned_response)
        state.status = "executed"
    except Exception as e:
        state.status = "execution_error"
        state.errors.append(f"LLM execution failed: {str(e)}")
        
    return state

def validate_step(state: FlowState) -> FlowState:
    """Етап 4: Перевірка результату."""
    if state.status in ["failed", "execution_error"] or state.route != "tech_extraction":
        return state
        
    try:
        validate(instance=state.extracted_data, schema=TECH_VACANCY_SCHEMA)
        state.validation_result = {"schema_ok": True}
        
        # Логічна валідація
        exp = state.extracted_data.get("experience_years")
        if exp is not None and (not isinstance(exp, int) or exp < 0 or exp > 20):
            state.warnings.append("Experience years looks suspiciously high or invalid.")
            state.status = "validated_with_warning"
        else:
            state.status = "validated"
            
    except ValidationError as e:
        state.validation_result = {"schema_ok": False, "error": e.message}
        state.status = "validation_failed"
        state.errors.append(f"Schema validation failed: {e.message}")
        
    return state

def apply_fallback(state: FlowState) -> FlowState:
    """Етап 5: Fallback у разі збою валідації або виконання."""
    if state.status in ["validation_failed", "execution_error"]:
        state.fallback_triggered = True
        state.fallback_result = "safe_failure"
        state.warnings.append("Fallback triggered. Data might be incomplete. Needs manual review.")
        
        # Rule-based fallback для досвіду, якщо LLM впала
        if state.route == "tech_extraction":
            matches = re.findall(r'(\d+)\+?\s*рок', state.clean_text)
            fallback_exp = int(matches[0]) if matches else None
            
            if not state.extracted_data:
                state.extracted_data = {"technologies": [], "experience_years": fallback_exp}
            else:
                state.extracted_data["experience_years"] = fallback_exp
                
        state.status = "recovered_via_fallback"
        
    return state

def export(state: FlowState) -> dict:
    """Етап 6: Формування фінального стабільного JSON."""
    export_payload = {
        "case_id": state.case_id,
        "route": state.route,
        "final_output": None,
        "needs_manual_review": state.fallback_triggered or bool(state.errors),
        "status": state.status,
        "warnings": state.warnings,
        "errors": state.errors
    }
    
    if state.route == "tech_extraction" and state.extracted_data:
        export_payload["final_output"] = state.extracted_data
    elif state.route == "non_tech_skip":
        export_payload["final_output"] = "Skipped extraction for non-technical vacancy."
    else:
        export_payload["final_output"] = "No data extracted."
        
    state.final_output = export_payload
    return export_payload