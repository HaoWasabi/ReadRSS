import re

def fix_surrogates(text):
    # Convert surrogate pairs to characters
    return re.sub(r'\\u(d[89ab][0-9a-f]{2})\\u(d[cdef][0-9a-f]{2})', 
                  lambda m: chr((int(m.group(1), 16) - 0xD800) * 0x400 + (int(m.group(2), 16) - 0xDC00) + 0x10000), text)

def decode_unicode_escapes(text):
    # Decode regular unicode escape sequences
    return re.sub(r'\\u[0-9a-fA-F]{4}', 
                  lambda m: chr(int(m.group(0)[2:], 16)), text)

def finally_change_formatting(text):
    # Replace \n and \/ for proper formatting
    return text.replace(r'\n', '\n').replace(r'\/', '/')

class read_fb_by_api:
    def __init__(self):
        pass
    