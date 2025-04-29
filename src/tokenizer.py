import re
import csv
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

def load_ner_patterns(file_path: str) -> dict:
    """
    Use NER patterns we added in ner_patterns.txt file

    Args:
        file_path (str): Path to the NER patterns file.

    Returns:
        dict: A dictionary with keys as entity types and values as lists of words.
    """
    patterns = {}
    with open(file_path, 'r', encoding='utf-8') as file:
        reader = csv.reader(file)
        next(reader)  # First line is a header
        for row in reader:
            entity_type, word = row
            if entity_type not in patterns:
                patterns[entity_type] = []
            patterns[entity_type].append(word)

    # Create a pattern dictionary
    for entity_type in patterns:
        patterns[entity_type] = '|'.join(patterns[entity_type])

    return patterns

def named_entity_recognition(text: str, patterns_file: str = "ner_patterns.txt") -> List[Tuple[str, str]]:
    """
    Named Entity Recognition (NER) over Telugu text.

    Args:
        text (str): Telugu text.
        patterns_file (str): Path to the NER patterns file.

    Returns:
        List[Tuple[str, str]]: Each word and its type.
    """
    # Load patterns from the file
    patterns = load_ner_patterns(patterns_file)

    # Tokenize text into words
    words = word_tokenize(text)
    print("Debug: Tokenized words:", words)

    # Loop over all the words and identify the type
    entities = []
    for word in words:
        for entity_type, pattern in patterns.items():
            if re.fullmatch(pattern, word):
                print(f"Debug: Matched {word} as {entity_type}")
                entities.append((word, entity_type))
                break

    return entities

def stem_word(word: str) -> str:
    """
    Perform stemming on a single Telugu word using rule-based suffix removal.

    Args:
        word (str): The input Telugu word.

    Returns:
        str: The stemmed word.
    """
    suffixes = ['లు', 'ము', 'తో', 'కు', 'ని', 'లో', 'గా', 'లు', 'కి', 'న్న']  # Added 3 more common Telugu suffixes
    for suffix in suffixes:
        if word.endswith(suffix):
            return word[:-len(suffix)] # remove matched suffix and return remaining word
    return word

def lemmatize_word(word: str) -> str:
    """
    Do lemmatization with the help of dictionary words in Telugu

    Args:
        word (str): Telugu word

    Returns:
        str: result
    """
    # basic lemma example
    lemmas = {
        'పుస్తకాలు': 'పుస్తకం',
        'కాలేజీలు': 'కాలేజీ',
    }
    return lemmas.get(word, word)

def morphological_analysis(word: str) -> dict:
    """
    Do morphological analysis on a single telugu word

    Args:
        word (str): Telugu word

    Returns:
        dict: root word, prefix and suffix.
    """
    suffixes = ['ాలు', 'లు', 'ము', 'తో', 'కు', 'ని', 'లో', 'గా', 'కి', 'న్న']  # common & compound suffixes like 'ాలు'
    prefixes = ['ప్ర', 'అ', 'సు', 'వ']

    # Extract suffix, the same 
    suffix = next((s for s in suffixes if word.endswith(s)), None)
    root = word[:-len(suffix)] if suffix else word

    # Extract prefix
    prefix = next((p for p in prefixes if root.startswith(p)), None)
    root = root[len(prefix):] if prefix else root

    return {
        'root': root,
        'prefix': prefix,
        'suffix': suffix
    }
