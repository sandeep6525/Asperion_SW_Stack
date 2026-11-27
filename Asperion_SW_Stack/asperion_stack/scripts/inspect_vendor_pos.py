with open('extracted_views/view-portal-vendor.html', 'r', encoding='utf-8') as f:
    c = f.read()

# Let's inspect around that line
idx = c.find('switchVendorPortalTab(\'pos\')')
print(c[idx-300:idx+200])
