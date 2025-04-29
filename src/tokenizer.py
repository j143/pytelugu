import re
from typing import List, Tuple

def normalize_text(text: str) -> str:
    """
    Normalization for Telugu text.
    - Remove extra spaces between words

    Args:
        text (str): The input Telugu text.

    Returns:
        str: The normalized Telugu text.
    """
    # Remove extra spaces
    text = re.sub(r'\s+', ' ', text).strip()

    return text

def word_tokenize(text: str) -> List[str]:
    """
    Tokenize the given Telugu text into words.

    Args:
        text (str): The input Telugu text.

    Returns:
        List[str]: A list of words extracted from the text.
    """
    # Define a regex pattern to match Telugu words and punctuation
    # reference: https://en.wikipedia.org/wiki/Telugu_(Unicode_block)
    # https://www.unicode.org/charts/PDF/U0C00.pdf
    pattern = r'[\u0C00-\u0C7F]+|[\.,!?;]'

    # Use re.findall to extract words and punctuation
    tokens = re.findall(pattern, text)

    return tokens

def pos_tag(text: str) -> List[Tuple[str, str]]:
    """
    Apply Part-of-Speech (POS) tags on Telugu text

    Args:
        text (str): Input text.

    Returns:
        List[Tuple[str, str]]: Each word and its POS tag.
    """
    # In telugu the following Parts of Speech are used
    # నామవాచకం 
    # సర్వనామం 
    # క్రియ 
    # క్రియా విశేషణం 
    # విశేషణం 
    # విభక్త్యర్థ పదం 
    # సముచ్ఛయము 
    # భావోద్రేక ప్రకటనార్ధము 

    # Basic suffice rules as a starting point
    suffix_rules = {
        'లు': 'NOUN',  # Plural suffix for nouns (పుస్తకాలు, పిల్లలు)
        'ము': 'NOUN',  # Singular suffix for nouns (మేము, తాము)
        'గా': 'ADV',   # Adverbial suffix (వేగంగా, నెమ్మదిగా)
        'కు': 'ADP',   # Postposition (నాకు, నీకు, మీకు )
        'ం': 'NOUN',   # Common noun suffix (పుస్తకం, క్షణం)
        'తున్నాను': 'VERB',  # Present continuous verb suffix (చదువుతున్నాను)
    }

    # Tokenize the text into words
    words = word_tokenize(text)

    # Tag each word based on suffix rules
    tagged_words = []
    for word in words:
        tag = 'X'  # Default tag for unknown words
        for suffix, pos in suffix_rules.items():
            if word.endswith(suffix):
                tag = pos
                break
        if word in [',', '.', '!', '?']:
            tag = 'PUNCT'
        tagged_words.append((word, tag))

    return tagged_words