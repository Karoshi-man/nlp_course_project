from __future__ import annotations
from dataclasses import dataclass
from typing import List, Dict, Any, Set
import regex 
import ftfy

DOMAIN_ABBREVIATIONS: Set[str] = {
    "м.", "вул.", "р.", "рр.", "т.д.", "т. д.", "т.ін.", "т. ін.", "тобто.",
    "ім.", "п.", "с.", "смт.", "обл.", "грн.", "коп.", "№",
    
    "node.js", "vue.js", "react.js", "next.js", "nest.js", 
    "three.js", ".net", "asp.net"
}

@dataclass(frozen=True)
class PreprocessPolicy:
    """
    конфігурація для керування пайплайном
    """
    normalize_unicode: bool = True
    normalize_whitespace: bool = True
    normalize_quotes: bool = True
    normalize_dashes: bool = True
    normalize_apostrophes: bool = True
    normalize_homoglyphs: bool = False

    mask_urls: bool = True
    mask_emails: bool = True
    mask_phones: bool = True
    
    remove_dou_boilerplate: bool = True 
    sentence_split: bool = True


URL_RE = regex.compile(r"""(?xi)\b(https?://[^\s<>"']+|www\.[^\s<>"']+)\b""")
EMAIL_RE = regex.compile(r"""(?xi)\b[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}\b""")
PHONE_RE = regex.compile(r"""(?x)(?:\+?380|0)\s?(?:\(?\d{2,3}\)?)\s?\d{2,3}\s?\d{2}\s?\d{2}""")
DOU_BOILERPLATE_RE = regex.compile(r"(?i)Facebook\s+Twitter\s+LinkedIn\s+Відгукнутися\s+на\s+вакансію\s+Правила\s+відгуків")
SENT_END_RE = regex.compile(r"([.!?])")

# normalization
def normalize_text(text: str, policy: PreprocessPolicy) -> str:
    """
    зводить усі символи до 
    єдиного стандарту
    """
    if policy.normalize_unicode:
        text = ftfy.fix_text(text)
    if policy.normalize_quotes:
        text = text.replace("«", '"').replace("»", '"').replace("“", '"').replace("”", '"').replace("„", '"')
    if policy.normalize_dashes:
        text = text.replace("–", "-").replace("—", "-")
    if policy.normalize_apostrophes:
        text = text.replace("’", "'").replace("ʼ", "'").replace("`", "'")
    if policy.normalize_homoglyphs:
        homoglyphs_map = {"i": "і", "I": "І", "e": "е", "E": "Е", "o": "о", "O": "О", "a": "а", "A": "А", "p": "р", "P": "Р", "c": "с", "C": "С", "x": "х", "X": "Х"}
        text = "".join(homoglyphs_map.get(c, c) for c in text)
    return text

# mask
def mask_pii(text: str, policy: PreprocessPolicy) -> str:
    """
    маскує персональні дані тегами
    """
    if policy.mask_urls:
        text = URL_RE.sub("<URL>", text)
    if policy.mask_emails:
        text = EMAIL_RE.sub("<EMAIL>", text)
    if policy.mask_phones:
        text = PHONE_RE.sub("<PHONE>", text)
    return text


# cleaning
def clean_text(text: str, policy: PreprocessPolicy) -> str:
    """
    видаляє веб-артефакти DOU та 
    прибирає зайві пробіли/переноси
    """
    if policy.remove_dou_boilerplate:
        text = DOU_BOILERPLATE_RE.sub("", text)
        
    if policy.normalize_whitespace:
        text = text.replace("\u00A0", " ")
        text = regex.sub(r"[ \t]+", " ", text)
        text = regex.sub(r"\s*\n+\s*", "\n", text)
        text = text.strip()
    return text


# splitter
def sentence_split(text: str, abbreviations: Set[str] = DOMAIN_ABBREVIATIONS) -> List[str]:
    """
    розумне розбиття на речення 
    із захистом IT-термінів
    """
    protected = []
    
    def protect(match):
        token = match.group(0)
        placeholder = f"__PROTECTED{len(protected)}__"
        protected.append(token)
        return placeholder

    def restore(t: str) -> str:
        for idx, token in enumerate(protected):
            t = t.replace(f"__PROTECTED{idx}__", token)
        return t

    text_prot = regex.sub(r"(?i)\b[a-z]+\.js\b", protect, text)
    text_prot = regex.sub(r"(?i)(?<!\w)\.net\b", protect, text_prot)
    text_prot = regex.sub(r"\bC\+\+", protect, text_prot)
    text_prot = regex.sub(r"\bC\#", protect, text_prot)
    text_prot = regex.sub(r"\b\d+(?:\.\d+)+\b", protect, text_prot)

    parts = []
    start = 0
    for m in SENT_END_RE.finditer(text_prot):
        end = m.end()
        chunk = text_prot[start:end].strip()
        chunk_restored = restore(chunk)
        
        last_token = chunk_restored.split()[-1].lower() if chunk_restored.split() else ""
        if last_token in abbreviations:
            continue
            
        parts.append(chunk_restored)
        start = end

    tail = restore(text_prot[start:].strip())
    if tail:
        parts.append(tail)

    return [regex.sub(r"\s+", " ", s).strip() for s in parts if s.strip()]


# main pipeline
def preprocess(text: str, policy: PreprocessPolicy | None = None) -> Dict[str, Any]:
    """
    головна точка входу 
    виконує всі кроки у правильній послідовності
    """
    policy = policy or PreprocessPolicy()
    
    # unify symbols
    text = normalize_text(text, policy)
    # hide PII
    text = mask_pii(text, policy)
    # сleaning
    text = clean_text(text, policy)
    
    result: Dict[str, Any] = {"clean_text": text}
    
    # breaking it down into sentences     
    if policy.sentence_split:
        result["sentences"] = sentence_split(text)
        
    return result
