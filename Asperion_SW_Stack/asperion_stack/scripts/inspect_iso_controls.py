with open('app/static/js/app.js', 'r', encoding='utf-8') as f:
    js = f.read()

idx = js.find('function loadISOControlsTable(')
if idx != -1:
    print(js[idx:idx+600])
else:
    print("Not found exact 'function loadISOControlsTable('")
    matches = [m.start() for m in re.finditer(r'loadISOControlsTable', js)]
    for m in matches:
        print(js[m-20:m+200])
