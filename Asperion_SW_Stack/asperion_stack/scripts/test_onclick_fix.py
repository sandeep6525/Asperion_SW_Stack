import re

test_str = '<button onclick="toggleCRMModal(\'modal-crm-opp\')" class="w-full">'
res = re.sub(r'onclick="([^"]*)"', 'onClick={() => {}}', test_str)
print("Before:", test_str)
print("After: ", res)
