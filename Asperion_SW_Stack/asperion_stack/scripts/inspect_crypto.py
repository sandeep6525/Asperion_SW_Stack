with open('app/static/index.html', 'r', encoding='utf-8') as f:
    text = f.read()
import re
m = re.search(r'<section[^>]*id=["\']view-crypto-tools["\'].*?</section>', text, re.DOTALL)
if m:
    with open('orig_crypto.html', 'w', encoding='utf-8') as out:
        out.write(m.group(0))
    print("Found and saved orig_crypto.html, length:", len(m.group(0)))
else:
    print("Not found")
