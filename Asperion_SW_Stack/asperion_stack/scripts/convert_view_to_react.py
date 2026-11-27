import os
import re

def parse_style(style_str):
    # e.g. "width: 80%; display: none;" -> "{ width: '80%', display: 'none' }"
    items = []
    for part in style_str.split(';'):
        part = part.strip()
        if not part:
            continue
        if ':' in part:
            k, v = part.split(':', 1)
            k = k.strip()
            v = v.strip()
            # camelCase key
            camel_k = re.sub(r'-([a-z])', lambda m: m.group(1).upper(), k)
            items.append(f"{camel_k}: '{v}'")
    return "{{ " + ", ".join(items) + " }}"

def html_to_jsx(html):
    # Convert comments
    html = re.sub(r'<!--(.*?)-->', r'{/*\1*/}', html, flags=re.DOTALL)
    
    # Void elements to self-closing: input, img, hr, br, col, meta, link
    void_tags = ['input', 'img', 'hr', 'br', 'col', 'meta', 'link', 'source']
    for tag in void_tags:
        # replace <tag (attrs)> (if not ending in />) with <tag (attrs) />
        html = re.sub(rf'<({tag}\b[^>]*?)(?<!/)>', r'<\1 />', html, flags=re.IGNORECASE)
    
    # Attributes
    attr_replacements = [
        (r'\bclass=', 'className='),
        (r'\bfor=', 'htmlFor='),
        (r'\btabindex=', 'tabIndex='),
        (r'\bcolspan=', 'colSpan='),
        (r'\browspan=', 'rowSpan='),
        (r'\bautocomplete=', 'autoComplete='),
        (r'\bautofocus\b', 'autoFocus'),
        (r'\breadonly\b', 'readOnly'),
        (r'\bclip-rule=', 'clipRule='),
        (r'\bfill-rule=', 'fillRule='),
        (r'\bstroke-width=', 'strokeWidth='),
        (r'\bstroke-linecap=', 'strokeLinecap='),
        (r'\bstroke-linejoin=', 'strokeLinejoin='),
        (r'\bstop-color=', 'stopColor='),
        (r'\bstop-opacity=', 'stopOpacity='),
    ]
    for pattern, repl in attr_replacements:
        html = re.sub(pattern, repl, html, flags=re.IGNORECASE)
    
    # Styles style="..." -> style={{ ... }}
    def style_sub(m):
        raw_val = m.group(1)
        return f"style={parse_style(raw_val)}"
    html = re.sub(r'style="([^"]*)"', style_sub, html)
    
    # Handle inputs without onChange having value="..." -> defaultValue="..."
    html = re.sub(r'<input\b([^>]*?)\bvalue="([^"]*)"([^>]*?)(?<!onChange)(/?>)', r'<input\1defaultValue="\2"\3\4', html)
    
    # Remove outer hidden class on root module-view if present
    html = re.sub(r'(<div[^>]*class(?:Name)?="[^"]*?\b)hidden(\b[^"]*")', r'\1\2', html, count=1)
    
    return html

print("Converter helper ready.")
