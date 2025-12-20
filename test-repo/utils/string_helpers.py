import re
from typing import List

def sanitize_html(text: str) -> str:
    """Remove HTML tags from a string"""
    clean = re.compile('<.*?>')
    return re.sub(clean, '', text)

def truncate_string(text: str, max_length: int, suffix: str = "...") -> str:
    """Truncate a string to a maximum length and add suffix if truncated"""
    if len(text) <= max_length:
        return text
    return text[:max_length - len(suffix)] + suffix

def capitalize_words(sentence: str) -> str:
    """Capitalize the first letter of each word in a sentence"""
    return ' '.join(word.capitalize() for word in sentence.split())

def extract_email_addresses(text: str) -> List[str]:
    """Extract all email addresses from a text string using regex"""
    email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    return re.findall(email_pattern, text)

def reverse_words_in_string(text: str) -> str:
    """Reverse the order of words in a string"""
    words = text.split()
    return ' '.join(reversed(words))

def count_word_frequency(text: str) -> dict:
    """Count the frequency of each word in a text"""
    words = text.lower().split()
    frequency = {}
    for word in words:
        frequency[word] = frequency.get(word, 0) + 1
    return frequency
