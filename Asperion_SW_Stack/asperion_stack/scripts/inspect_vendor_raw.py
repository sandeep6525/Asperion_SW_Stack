with open('extracted_views/view-portal-vendor.html', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i in range(65, 95):
    if i < len(lines):
        print(f"{i+1}: {lines[i]}", end='')
