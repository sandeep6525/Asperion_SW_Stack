import re

with open("E:/Asperion_SW_Stack/Asperion_SW_Stack/Asperion_SW_Stack/asperion_stack/app/static/index.html", "r", encoding="utf-8") as f:
    text = f.read()

modals = re.findall(r'id=["\'](modal-[^"\']+)["\']', text)
print("Modals found:", modals)

# Also check for command palette
cp = re.findall(r'id=["\']([^"\']*command[^"\']*)["\']', text)
print("Command palette IDs:", cp)

# Check notification dropdown
notif = re.findall(r'id=["\']([^"\']*notif[^"\']*)["\']', text)
print("Notification IDs:", notif)
