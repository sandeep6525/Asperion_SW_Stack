with open('extracted_views/view-portal-vendor.html', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i in range(45, 66):
    if i < len(lines):
        print(f"{i+1}: {lines[i]}", end='')
