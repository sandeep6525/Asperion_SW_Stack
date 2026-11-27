import re

with open('app/static/index.html', 'r', encoding='utf-8') as f:
    text = f.read()

for term in ['guardrail', 'iso-standards', 'ai-cloud']:
    matches = re.findall(rf'.{{0,50}}{term}.{{0,50}}', text)
    print(f"\nMatches for {term}: {len(matches)}")
    for m in matches[:5]:
        print("  ", repr(m.strip()))
