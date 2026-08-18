import re

with open('app.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Replace common Unicode characters with ASCII
content = content.replace('\u2026', '...')   # ellipsis
content = content.replace('\u2014', '-')     # em-dash
content = content.replace('\u2550', '=')     # box drawing
content = content.replace('\u2019', "'")     # right single quotation
content = content.replace('\u2018', "'")     # left single quotation
content = content.replace('\u2013', '-')     # en-dash

with open('app.py', 'w', encoding='utf-8') as f:
    f.write(content)

print('Done - all Unicode replaced in app.py')

# Also fix src files
import os
src_dir = 'src'
for fname in os.listdir(src_dir):
    if fname.endswith('.py'):
        fpath = os.path.join(src_dir, fname)
        with open(fpath, 'r', encoding='utf-8') as f:
            c = f.read()
        changed = c
        changed = changed.replace('\u2026', '...')
        changed = changed.replace('\u2014', '-')
        changed = changed.replace('\u2550', '=')
        changed = changed.replace('\u2019', "'")
        changed = changed.replace('\u2018', "'")
        changed = changed.replace('\u2013', '-')
        if changed != c:
            with open(fpath, 'w', encoding='utf-8') as f:
                f.write(changed)
            print(f'Fixed unicode in {fpath}')

print('All done!')
