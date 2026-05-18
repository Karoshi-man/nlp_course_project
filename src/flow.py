from .flow_state import FlowState
from .steps import ingest, route, execute, validate_step, apply_fallback, export
from .flow_logger import log_flow_state

def run_extraction_flow(raw_text: str, llm_caller, case_id: str = None, log_file: str = "docs/flow_logs_lab14.jsonl") -> dict:
    """
    Запускає повний цикл обробки вакансії: Ingest -> Route -> Execute -> Validate -> Fallback -> Export.
    """
    # Ініціалізація стану
    state = FlowState(raw_text=raw_text, case_id=case_id)
    
    # Конвеєр
    state = ingest(state)
    state = route(state)
    
    # Виконуємо запит до LLM лише якщо це технічна вакансія
    if state.route == "tech_extraction":
        state = execute(state, llm_caller)
        state = validate_step(state)
    
    # Безпечне відновлення у разі збою
    state = apply_fallback(state)
    
    # Експорт результатів
    final_result = export(state)
    
    # Логування всього процесу
    log_flow_state(state, log_file)
    
    return final_result