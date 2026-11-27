import os, glob

total_bytes = 0
files = glob.glob('extracted_views/view-*.html')
for f in files:
    total_bytes += os.path.getsize(f)

modals_size = os.path.getsize('extracted_views/all_modals.html')
print(f"Total size of 27 views: {total_bytes / 1024:.1f} KB")
print(f"Total size of modals: {modals_size / 1024:.1f} KB")
