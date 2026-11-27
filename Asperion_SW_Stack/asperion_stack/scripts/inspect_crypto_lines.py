with open('frontend/src/views/CryptoToolsView.tsx', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i in [79, 106, 136]:
    print(f"{i+1}: {lines[i]}", end='')
