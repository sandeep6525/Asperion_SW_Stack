from html_to_jsx_lib_v2 import convert_html_robust

with open('extracted_views/view-analytics.html', 'r', encoding='utf-8') as f:
    raw = f.read()

cfg = {
    'tab_switch_fn': 'switchAnalyticsTab',
    'default_tab': 'fin',
    'tabs': ['fin', 'pmo', 'talent', 'secops', 'strategy', 'sim', 'datascience', 'decision', 'montecarlo', 'infographics'],
    'pane_prefix': 'analytics-pane-'
}

jsx = convert_html_robust(raw, cfg)
code = f"""import React, {{ useState, useEffect }} from 'react';
import axios from 'axios';

export const AnalyticsView: React.FC = () => {{
  const [activeTab, setActiveTab] = useState<string>('fin');

  useEffect(() => {{
    // Optional data hydration
  }}, []);

  return (
    <div className="w-full">
      {jsx}
    </div>
  );
}};

export default AnalyticsView;
"""

with open('frontend/src/views/AnalyticsView.tsx', 'w', encoding='utf-8') as f:
    f.write(code)

print("AnalyticsView written.")
