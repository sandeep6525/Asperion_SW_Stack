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
            v = v.strip().replace("'", "\\'")
            camel_k = re.sub(r'-([a-z])', lambda m: m.group(1).upper(), k)
            items.append(f"{camel_k}: '{v}'")
    return "{{ " + ", ".join(items) + " }}"

def convert_html_robust(html_str, cfg=None):
    # 1. Clean HTML comments into JSX comments
    html_str = re.sub(r'<!--(.*?)-->', r'{/*\1*/}', html_str, flags=re.DOTALL)

    # 2. Void elements self-closing: <tag ...> -> <tag ... />
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

    # 4. Convert numeric JSX attributes to numbers: colSpan={5}, rowSpan={2}, rows={3}, etc.
    num_attrs = ['colSpan', 'rowSpan', 'rows', 'cols', 'tabIndex', 'maxLength', 'minLength', 'size', 'strokeWidth']
    for na in num_attrs:
        html_str = re.sub(rf'\b{na}="(-?\d+)"', rf'{na}={{\1}}', html_str)
        html_str = re.sub(rf"\b{na}='(-?\d+)'", rf'{na}={{\1}}', html_str)

    # 5. Styles: style="..." -> style={{ ... }}
    html_str = re.sub(r'style="([^"]*)"', lambda m: f"style={parse_style(m.group(1))}", html_str)

    # 6. Events: double quotes and single quotes
    html_str = re.sub(r'onsubmit="[^"]*"', 'onSubmit={(e) => e.preventDefault()}', html_str, flags=re.IGNORECASE)
    html_str = re.sub(r"onsubmit='[^']*'", 'onSubmit={(e) => e.preventDefault()}', html_str, flags=re.IGNORECASE)

    html_str = re.sub(r'onchange="[^"]*"', 'onChange={() => {}}', html_str, flags=re.IGNORECASE)
    html_str = re.sub(r"onchange='[^']*'", 'onChange={() => {}}', html_str, flags=re.IGNORECASE)

    html_str = re.sub(r'oninput="[^"]*"', 'onInput={() => {}}', html_str, flags=re.IGNORECASE)
    html_str = re.sub(r"oninput='[^']*'", 'onInput={() => {}}', html_str, flags=re.IGNORECASE)

    # Tabs in onclick
    if cfg and 'tabs' in cfg:
        switch_fn = cfg.get('tab_switch_fn')
        if switch_fn:
            pattern1 = re.compile(rf'onclick="[^"]*{switch_fn}\(\s*\\?[\'"]([^\'"]+)\\?[\'"]\s*\)[^"]*"', re.IGNORECASE)
            html_str = pattern1.sub(r"onClick={() => setActiveTab('\1')}", html_str)
            pattern2 = re.compile(rf"onclick='[^']*{switch_fn}\(\s*\\?[\'\"]([^\'\"]+)\\?[\'\"]\s*\)[^']*'", re.IGNORECASE)
            html_str = pattern2.sub(r"onClick={() => setActiveTab('\1')}", html_str)

    # All remaining onclick
    html_str = re.sub(r'onclick="[^"]*"', 'onClick={() => {}}', html_str, flags=re.IGNORECASE)
    html_str = re.sub(r"onclick='[^']*'", 'onClick={() => {}}', html_str, flags=re.IGNORECASE)

    # 7. Inputs defaultValue
    html_str = re.sub(r'(<input\b[^>]*?)\bvalue="([^"]*)"([^>]*?)(?<!onChange)(/?>)', r'\1defaultValue="\2"\3\4', html_str)

    # 8. Unhide root
    html_str = re.sub(r'(className="[^"]*?\b)hidden(\b[^"]*")', r'\1\2', html_str, count=1)

    # 9. Wire pane visibility if tabbed
    if cfg and 'tabs' in cfg:
        pane_prefix = cfg.get('pane_prefix')
        for tab in cfg['tabs']:
            pane_id = f"{pane_prefix}{tab}"
            disp_style = "style={{ display: activeTab === '" + tab + "' ? 'block' : 'none' }}"
            html_str = re.sub(rf'(id=["\']{pane_id}["\'])', rf"\1 {disp_style}", html_str)

    # 10. Fix VendorPortal stray unclosed div if present in raw
    bad_vendor = '<div className="bg-white p-3.5 rounded-xl border border-slate-200 shadow-sm">\n                    <button onClick={() => setActiveTab(\'pos\')}'
    good_vendor = '</div>\n\n                {/* Navigation Tabs */}\n                <div className="flex flex-wrap gap-2 mb-6 border-b border-slate-200 pb-3">\n                    <button onClick={() => setActiveTab(\'pos\')}'
    html_str = html_str.replace(bad_vendor, good_vendor)

    return html_str

print("html_to_jsx_lib_v2 updated with numeric attribute parser.")
