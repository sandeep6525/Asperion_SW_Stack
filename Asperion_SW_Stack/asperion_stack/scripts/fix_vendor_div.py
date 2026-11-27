with open('frontend/src/views/VendorPortalView.tsx', 'r', encoding='utf-8') as f:
    c = f.read()

# Replace the stray unclosed div
bad = '<div className="bg-white p-3.5 rounded-xl border border-slate-200 shadow-sm">\n                    <button onClick={() => setActiveTab(\'pos\')}'
good = '</div>\n\n                {/* Navigation Tabs */}\n                <div className="flex flex-wrap gap-2 mb-6 border-b border-slate-200 pb-3">\n                    <button onClick={() => setActiveTab(\'pos\')}'

if bad in c:
    c = c.replace(bad, good)
    with open('frontend/src/views/VendorPortalView.tsx', 'w', encoding='utf-8') as f:
        f.write(c)
    print("Replaced stray div in VendorPortalView.tsx")
else:
    print("Pattern not found!")
