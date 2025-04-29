import re
from typing import List

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