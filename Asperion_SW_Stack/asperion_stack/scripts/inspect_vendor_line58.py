with open('frontend/src/views/VendorPortalView.tsx', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i in range(45, 75):
    if i < len(lines):
        print(f"{i+1}: {lines[i]}", end='')
