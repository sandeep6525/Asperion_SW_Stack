with open('app/static/js/app.js', 'r', encoding='utf-8') as f:
    js = f.read()

idx = js.find('function loadFinance(')
end = js.find('function loadHRMS(', idx)
print(js[idx:end])
