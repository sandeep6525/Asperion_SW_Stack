import re, os, glob

for filepath in sorted(glob.glob('extracted_views/view-*.html')):
    vid = os.path.basename(filepath).replace('.html', '')
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Find h2, h3, tabs (buttons with onclick="switch...Tab")
    h2 = re.findall(r'<h2[^>]*>(.*?)</h2>', content, re.DOTALL)
    tabs = re.findall(r'onclick=[\'"](switch[A-Za-z0-9_]*Tab[^\'"]*)[\'"][^>]*>(.*?)</button>', content, re.DOTALL)
    buttons = re.findall(r'<button[^>]*onclick=[\'"]([^\'"]+)[\'"][^>]*>(.*?)</button>', content, re.DOTALL)
    
    title = h2[0].strip() if h2 else vid
    clean_tabs = [re.sub(r'<[^>]+>', '', t[1]).strip() for t in tabs]
    action_btns = list(set([b[0].split('(')[0] for b in buttons]))
    
    print(f"\n[{vid}] {title[:40]}")
    if clean_tabs:
        print(f"   TABS ({len(clean_tabs)}): {clean_tabs}")
    print(f"   ACTIONS: {action_btns[:6]}")
