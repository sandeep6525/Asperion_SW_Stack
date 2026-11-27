import sys
import os
sys.path.insert(0, os.path.abspath("."))
import app.main

routes = []
for r in app.main.app.routes:
    if hasattr(r, 'path'):
        methods = ",".join(getattr(r, 'methods', []))
        routes.append((r.path, methods))

routes.sort(key=lambda x: x[0])
for path, methods in routes:
    print(f"{path:<55} {methods}")
