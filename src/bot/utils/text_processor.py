import re
from bs4 import BeautifulSoup

class TextProcessor:
    def fix_surrogates(self, text):
        # Convert surrogate pairs to characters
        return re.sub(r'\\u(d[89ab][0-9a-f]{2})\\u(d[cdef][0-9a-f]{2})', 
                      lambda m: chr((int(m.group(1), 16) - 0xD800) * 0x400 + (int(m.group(2), 16) - 0xDC00) + 0x10000), text)
        
    def decode_unicode_escapes(self, text):
        # Decode regular unicode escape sequences
        return re.sub(r'\\u[0-9a-fA-F]{4}', 
                      lambda m: chr(int(m.group(0)[2:], 16)), text)
        
    def finally_change_formatting(self, text):
        # Replace \n and \/ for proper formatting
        return text.replace(r'\n', '\n').replace(r'\/', '/')
    
    def proccess_unicode_text(self, text):
        text = self.fix_surrogates(text)
        text = self.decode_unicode_escapes(text)
        text = self.finally_change_formatting(text)
        return text
    
    def parse_html(self, content):
        if content is None:
            return None
        
        # Use BeautifulSoup to parse the HTML content
        soup = BeautifulSoup(content, 'html.parser')
        
        # Strip away HTML tags and keep only the text
        text = soup.get_text()
        return text
