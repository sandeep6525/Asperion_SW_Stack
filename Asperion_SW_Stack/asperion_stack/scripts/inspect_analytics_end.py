with open('frontend/src/views/AnalyticsView.tsx', 'r', encoding='utf-8') as f:
    lines = f.readlines()

print(f"Total lines: {len(lines)}")
for i in range(max(0, len(lines)-25), len(lines)):
    print(f"{i+1}: {lines[i]}", end='')
