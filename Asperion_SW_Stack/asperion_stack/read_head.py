with open('app/static/index.html', 'r', encoding='utf-8') as f:
    text = f.read(4000)

print(text[:3000])
