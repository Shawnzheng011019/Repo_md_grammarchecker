import os
import re

def extract_text_from_md(md_path, txt_path):
    """Extract text from MD file and save to TXT file, removing code blocks and HTML tags"""
    with open(md_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Remove fenced code blocks (```code```)
    content = re.sub(r'```.*?```', '', content, flags=re.DOTALL)
    
    # Remove indented code blocks (4 spaces or 1 tab)
    content = re.sub(r'(?:^|\n)[ \t]{4,}.*', '', content, flags=re.MULTILINE)
    
    # Remove HTML tags
    content = re.sub(r'<[^>]*>', '', content)
    
    # Remove MD markup
    text = re.sub(r'#+\s|`|!\[.*?\]\(.*?\)|\[.*?\]\(.*?\)|<.*?>|</.*?>', '', content)
    text = re.sub(r'---+', '', text)
    
    with open(txt_path, 'w', encoding='utf-8') as f:
        f.write(text)    