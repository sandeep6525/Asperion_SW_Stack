import os
import re

def parse_style(style_str):
    items = []
    for part in style_str.split(';'):
        part = part.strip()
        if not part:
            continue
        if ':' in part:
            k, v = part.split(':', 1)
            k = k.strip()
            v = v.strip()
            camel_k = re.sub(r'-([a-z])', lambda m: m.group(1).upper(), k)
            items.append(f"{camel_k}: '{v}'")
    return "{{ " + ", ".join(items) + " }}"

def convert_html_to_jsx_body(html):
    # 1. HTML comments to JSX comments
    html = re.sub(r'<!--(.*?)-->', r'{/*\1*/}', html, flags=re.DOTALL)
    
    # 2. Self-close void tags: input, img, hr, br, col, meta, link, source
    void_tags = ['input', 'img', 'hr', 'br', 'col', 'meta', 'link', 'source']
    for tag in void_tags:
        # replace <tag (attrs) > with <tag (attrs) /> if not already self-closing
        # We handle tags spanning multiple lines
        pattern = re.compile(rf'<({tag}\b[^>]*?)(?<!/)>', re.IGNORECASE)
        html = pattern.sub(r'<\1 />', html)
    
    # 3. Standard attribute renames
    attrs = [
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
        (r'\bxmlns:xlink=', 'xmlnsXlink='),
        (r'\bxlink:href=', 'xlinkHref='),
    ]
    for pattern, repl in attrs:
        html = re.sub(pattern, repl, html, flags=re.IGNORECASE)
    
    # 4. Convert style="display: none; width: 80%" to style={{ display: 'none', width: '80%' }}
    html = re.sub(r'style="([^"]*)"', lambda m: f"style={parse_style(m.group(1))}", html)
    
    # 5. Fix uncontrolled inputs: value="..." without onChange -> defaultValue="..."
    html = re.sub(r'(<input\b[^>]*?)\bvalue="([^"]*)"([^>]*?)(?<!onChange)(/?>)', r'\1defaultValue="\2"\3\4', html)
    
    # 6. Escape lone curly braces or ampersands in text if any
    # (Usually not an issue unless in raw script/text, handled by React)
    
    # 7. Convert generic onclick="..." to harmless or stateful callbacks
    # Remove onclick attributes from non-tab elements or convert to onClick={() => {}}
    return html

print("Converter base ready.")
