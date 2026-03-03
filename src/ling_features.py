import stanza
import json

stanza.download('uk', processors='tokenize,pos,lemma')
nlp = stanza.Pipeline(lang='uk', processors='tokenize,pos,lemma', use_gpu=False)

def extract_linguistic_features(text: str) -> dict:
    """
    Приймає текст і повертає 
    оригінальні токени, леми та POS-теги
    """
    doc = nlp(text)
    
    tokens = []
    lemmas = []
    pos_tags = []
    
    for sentence in doc.sentences:
        for word in sentence.words:
            tokens.append(word.text)
            lemmas.append(word.lemma if word.lemma else word.text)
            pos_tags.append(word.upos)
            
    return {
        "lemma_text": " ".join(lemmas),
        "pos_seq": " ".join(pos_tags),
        "original_tokens": " ".join(tokens)
    }

if __name__ == "__main__":
    edge_cases_path = "../tests/ling_edge_cases.jsonl"
    with open(edge_cases_path, "r", encoding="utf-8") as f:
        for line in f:
            case = json.loads(line.strip())
            result = extract_linguistic_features(case["text"])
            
            print(f"Оригінал: {case['text']}")
            print(f"Леми:    {result['lemma_text']}")
            print(f"POS:     {result['pos_seq']}")
            print(f"Очікувана проблема: {case['expected_issue']}")
            print("-" * 60)