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

def convert_html(html_str, cfg=None):
    # 1. Comments
    html_str = re.sub(r'<!--(.*?)-->', r'{/*\1*/}', html_str, flags=re.DOTALL)
    
    # 2. Self close void elements: input, img, hr, br, col, meta, link, source
    void_tags = ['input', 'img', 'hr', 'br', 'col', 'meta', 'link', 'source']
    for tag in void_tags:
        html_str = re.sub(rf'<({tag}\b[^>]*?)(?<!/)>', r'<\1 />', html_str, flags=re.IGNORECASE)
        
    # 3. Attributes
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
        html_str = re.sub(pattern, repl, html_str, flags=re.IGNORECASE)
        
    # 4. Styles
    html_str = re.sub(r'style="([^"]*)"', lambda m: f"style={parse_style(m.group(1))}", html_str)
    
    # 5. Fix inputs without onChange having value="..." -> defaultValue="..."
    html_str = re.sub(r'(<input\b[^>]*?)\bvalue="([^"]*)"([^>]*?)(?<!onChange)(/?>)', r'\1defaultValue="\2"\3\4', html_str)

    # 6. Remove root 'hidden' class
    html_str = re.sub(r'(className="[^"]*?\b)hidden(\b[^"]*")', r'\1\2', html_str, count=1)

    # 7. Wire up tabs if config provided
    if cfg and 'tabs' in cfg:
        switch_fn = cfg.get('tab_switch_fn')
        pane_prefix = cfg.get('pane_prefix')
        
        # Replace onclick="switchXTab('tabKey')" with onClick={() => setActiveTab('tabKey')}
        if switch_fn:
            pattern = re.compile(rf'onclick=["\'][^"\']*{switch_fn}\([\'"]([^\'"]+)[\'"]\)[^"\']*["\']', re.IGNORECASE)
            html_str = pattern.sub(r"onClick={() => setActiveTab('\1')}", html_str)
            
        # Replace remaining onclick="..." with safe onClick={() => {}}
        html_str = re.sub(r'onclick=["\']([^"\']+)["\']', "onClick={() => {}}", html_str)

        # Wire up pane visibility: for each pane, add style={{ display: activeTab === 'tab' ? 'block' : 'none' }}
        for tab in cfg['tabs']:
            pane_id = f"{pane_prefix}{tab}"
            # In string formatting, {{ display: ... }}
            disp_style = "style={{ display: activeTab === '" + tab + "' ? 'block' : 'none' }}"
            html_str = re.sub(rf'(id=["\']{pane_id}["\'])', rf"\1 {disp_style}", html_str)
    else:
        # Just clean remaining onclick
        html_str = re.sub(r'onclick=["\']([^"\']+)["\']', "onClick={() => {}}", html_str)

    return html_str

print("html_to_jsx_lib ready.")
