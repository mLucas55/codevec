"""String manipulation and formatting utilities"""

def truncate_string(text, max_length, suffix="..."):
    """Shorten text to maximum length with ellipsis"""
    if len(text) <= max_length:
        return text
    return text[:max_length - len(suffix)] + suffix

def slugify(text):
    """Convert text to URL-friendly slug"""
    import re
    
    # Convert to lowercase
    text = text.lower()
    
    # Replace spaces with hyphens
    text = text.replace(' ', '-')
    
    # Remove non-alphanumeric characters except hyphens
    text = re.sub(r'[^a-z0-9-]', '', text)
    
    # Remove multiple consecutive hyphens
    text = re.sub(r'-+', '-', text)
    
    # Remove leading/trailing hyphens
    return text.strip('-')

def format_currency(amount, currency_symbol='$'):
    """Format number as currency with commas"""
    return f"{currency_symbol}{amount:,.2f}"

def capitalize_words(text):
    """Capitalize first letter of each word"""
    return ' '.join(word.capitalize() for word in text.split())

def remove_duplicates(text, delimiter=','):
    """Remove duplicate items from delimited string"""
    items = [item.strip() for item in text.split(delimiter)]
    unique_items = []
    
    for item in items:
        if item not in unique_items:
            unique_items.append(item)
    
    return delimiter.join(unique_items)

def extract_numbers(text):
    """Extract all numbers from a string"""
    import re
    return [int(num) for num in re.findall(r'\d+', text)]

def mask_sensitive_data(text, visible_chars=4):
    """Mask sensitive information like credit cards"""
    if len(text) <= visible_chars:
        return '*' * len(text)
    
    masked_length = len(text) - visible_chars
    return '*' * masked_length + text[-visible_chars:]

def convert_to_snake_case(text):
    """Convert camelCase or PascalCase to snake_case"""
    import re
    
    # Insert underscore before uppercase letters
    text = re.sub(r'([A-Z])', r'_\1', text)
    
    # Convert to lowercase and remove leading underscore
    return text.lower().lstrip('_')

def parse_key_value_pairs(text, pair_delimiter=',', kv_delimiter='='):
    """Parse string like 'key1=value1,key2=value2' into dict"""
    result = {}
    
    pairs = text.split(pair_delimiter)
    for pair in pairs:
        if kv_delimiter in pair:
            key, value = pair.split(kv_delimiter, 1)
            result[key.strip()] = value.strip()
    
    return result
