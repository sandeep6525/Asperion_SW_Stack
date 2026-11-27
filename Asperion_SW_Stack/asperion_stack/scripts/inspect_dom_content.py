with open('app/static/js/app.js', 'r', encoding='utf-8') as f:
    js = f.read()

idx = js.find('DOMContentLoaded')
print(js[idx:idx+1200])
