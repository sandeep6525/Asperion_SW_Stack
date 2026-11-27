import re

with open('extracted_views/all_modals.html', 'r', encoding='utf-8') as f:
    c = f.read()

for m in ['modal-crm-opp', 'modal-crm-ticket']:
    idx = c.find(m)
    if idx != -1:
        print(f"=== {m} ===")
        print(c[idx-50:idx+800])
        print("...\n")
