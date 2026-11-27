with open('frontend/src/utils/dataLoaders.js', 'r', encoding='utf-8') as f:
    c = f.read()

c = c.replace('declare const Chart: any;', '// Chart placeholder')
c = c.replace("./formatters.ts", "./formatters")

with open('frontend/src/utils/dataLoaders.js', 'w', encoding='utf-8') as f:
    f.write(c)

print('Updated dataLoaders.js successfully.')
