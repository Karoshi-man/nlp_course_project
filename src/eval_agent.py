def run_evaluation(test_cases, agent, baseline_llm_caller=None):
    """
    Запускає список текстів вакансій через агента і через baseline LLM для порівняння.
    """
    results = []
    
    for case in test_cases:
        task_id = case["id"]
        input_text = case["text"]
        
        print(f"\n--- Running Task: {task_id} ---")
        
        # Запуск агента з інструментами
        agent_result = agent.run(task_id=task_id, user_input=input_text)
        
        # Запуск базової моделі (без інструментів)
        baseline_answer = None
        if baseline_llm_caller:
            baseline_prompt = f"Analyze this IT vacancy from DOU. Tell me the required tech stack and minimum years of experience. Vacancy: '{input_text}'"
            baseline_answer = baseline_llm_caller(baseline_prompt)
            
        results.append({
            "task_id": task_id,
            "input": input_text,
            "expected_behavior": case["expected_behavior"],
            "tool_calls": agent_result["tool_calls"],
            "agent_final_answer": agent_result["final_answer"],
            "baseline_answer": baseline_answer
        })
        
    return results