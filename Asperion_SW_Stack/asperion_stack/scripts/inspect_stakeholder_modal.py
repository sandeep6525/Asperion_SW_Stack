with open("E:/Asperion_SW_Stack/Asperion_SW_Stack/Asperion_SW_Stack/asperion_stack/app/static/index.html", "r", encoding="utf-8") as f:
    text = f.read()

pos = text.find('id="modal-stakeholder-login"')
if pos != -1:
    end = text.find('</div>\n            </div>', pos) + 22
    print("=== Stakeholder Login Modal ===")
    print(text[pos-20:pos+1500])
