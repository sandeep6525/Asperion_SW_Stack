from html_to_jsx_lib_v2 import convert_html_robust

with open('extracted_views/view-crm.html', 'r', encoding='utf-8') as f:
    raw = f.read()

jsx = convert_html_robust(raw)
code = f"""import React, {{ useState, useEffect }} from 'react';
import axios from 'axios';

export const CRMView: React.FC = () => {{
  return (
    <div className="w-full">
      {jsx}
    </div>
  );
}};

export default CRMView;
"""

with open('frontend/src/views/CRMView.tsx', 'w', encoding='utf-8') as f:
    f.write(code)

print("CRMView written.")
