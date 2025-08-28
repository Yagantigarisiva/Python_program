\
"""
merge_uploaded.py
-----------------
This utility imports files placed in the uploaded_files/ directory into the Flask project.
- HTML files (*.html) are copied into templates/ (if they use full <html>... they are inserted into
  templates/original_pages/ with no changes so your content is preserved).
- CSS files are copied into static/css/ unless they already exist (a numeric suffix will be added).
- JS files are copied into static/js/ similarly.
- Images and other static assets are copied into static/assets/

Run this script from the project root:
    python merge_uploaded.py
After running, optionally run `python data/init_db.py` to reinitialize the DB and then `flask --app app run`.
"""
import os, shutil, pathlib, re, sys

ROOT = os.path.dirname(os.path.abspath(__file__))
UP = os.path.join(ROOT, "uploaded_files")
TEMPLATES = os.path.join(ROOT, "templates", "original_pages")
STATIC_CSS = os.path.join(ROOT, "static", "css")
STATIC_JS = os.path.join(ROOT, "static", "js")
STATIC_ASSETS = os.path.join(ROOT, "static", "assets")
DATA_DIR = os.path.join(ROOT, "data")

os.makedirs(UP, exist_ok=True)
os.makedirs(TEMPLATES, exist_ok=True)
os.makedirs(STATIC_CSS, exist_ok=True)
os.makedirs(STATIC_JS, exist_ok=True)
os.makedirs(STATIC_ASSETS, exist_ok=True)

def unique_copy(src, dst_dir):
    base = os.path.basename(src)
    name = base
    dst = os.path.join(dst_dir, name)
    i = 1
    while os.path.exists(dst):
        name = f"{os.path.splitext(base)[0]}-{i}{os.path.splitext(base)[1]}"
        dst = os.path.join(dst_dir, name)
        i += 1
    shutil.copy2(src, dst)
    return dst

def import_files():
    copied = []
    for root, _, files in os.walk(UP):
        for f in files:
            src = os.path.join(root, f)
            ext = f.lower().split(".")[-1]
            if ext in ("html","htm"):
                # preserve original HTML untouched in templates/original_pages/
                dst = unique_copy(src, TEMPLATES)
                copied.append(dst)
            elif ext in ("css",):
                dst = unique_copy(src, STATIC_CSS)
                copied.append(dst)
            elif ext in ("js",):
                dst = unique_copy(src, STATIC_JS)
                copied.append(dst)
            elif ext in ("png","jpg","jpeg","gif","svg","webp","ico"):
                dst = unique_copy(src, STATIC_ASSETS)
                copied.append(dst)
            elif ext in ("sql",):
                # copy to data/
                dst = unique_copy(src, DATA_DIR)
                copied.append(dst)
            else:
                # default: copy to assets
                dst = unique_copy(src, STATIC_ASSETS)
                copied.append(dst)
    return copied

if __name__ == "__main__":
    copied = import_files()
    if not copied:
        print("No files found in uploaded_files/. Drop your files there and run again.")
    else:
        print("Imported files:")
        for c in copied:
            print(" -", os.path.relpath(c, ROOT))
        print("\\nIf you imported HTML files, check templates/original_pages/ and update routes in app.py to serve them.")
