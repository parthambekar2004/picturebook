from nltk.tokenize import sent_tokenize
import nltk

def extract_important_event(page_text: str) -> str:
    if not page_text or len(page_text.strip()) < 20:
        return ""

    try:
        sentences = sent_tokenize(page_text)
    except LookupError:
        nltk.download('punkt')
        nltk.download('punkt_tab')
        sentences = sent_tokenize(page_text)

    return max(sentences, key=len)