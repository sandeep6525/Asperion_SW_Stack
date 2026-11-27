with open('app/static/js/app.js', 'r', encoding='utf-8') as f:
    js = f.read()

idx = js.find('function renderAgenticFleet(')
if idx == -1:
    idx = js.find('function loadAgenticFleet(')
if idx != -1:
    print(js[idx:idx+1500])
else:
    print("Not found, searching 'cachedAgenticFleet'...")
    matches = [m.start() for m in re.finditer(r'cachedAgenticFleet', js)]
    for m in matches[:3]:
        print(js[m:m+500])
