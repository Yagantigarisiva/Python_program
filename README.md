# Accessible Web Accessibility Project (HTML + CSS + Python + SQL)

This bundle gives you a **complete project** using Flask (Python) with accessible HTML/CSS templates and a searchable content database (SQLite FTS5).

## What you can do
- Keep all your existing HTML content **without content loss** by pasting it into the provided templates.
- Serve pages with proper landmarks and a visible **"Skip to main content"** link at the **top-right**, and navigation on the **top-left** slightly below the skip link.
- Use a keyboard-accessible, ARIA-friendly navigation.
- Search your page content with SQLite **Full‑Text Search (FTS5)**.
- SQL scripts included for schema and seed data.

---

## Quick Start (Windows + Chrome + Screen Reader)

1. **Install Python 3.10+** if not already installed.
2. Open **Command Prompt** in this project folder.
3. Create a virtual environment:
   ```
   python -m venv .venv
   ```
4. Activate it:
   ```
   .venv\Scripts\activate
   ```
5. Install dependencies:
   ```
   pip install -r requirements.txt
   ```
6. Initialize the database:
   ```
   python data/init_db.py
   ```
7. Run the site:
   ```
   flask --app app run --debug
   ```
8. Open your browser at **http://127.0.0.1:5000/**

### Paste your existing HTML
- Open the files in `templates/` (for example `index.html`).
- Replace the content inside the `<main id="main"> … </main>` area with your existing HTML chunks.
- If you have many standalone static pages, you can also drop them in `templates/` and add routes in `app.py` (see comments).

### Searching
- Use the search landmark (`Ctrl+L` to focus the address bar, then Tab into the page, or use `;` quick nav keys depending on your screen reader).
- Results page shows matches with context snippets.
- To index more pages, either:
  - Add content via `data/seed.sql` and re-run `python data/init_db.py`, or
  - Use the `/admin/reindex` route while running (simple dev‑only route).

---

## Project Structure
```
app.py
requirements.txt
README.md
templates/
  base.html
  index.html
  about.html
  contact.html
  search.html
static/
  css/styles.css
  js/main.js
data/
  schema.sql
  seed.sql
  init_db.py
tests/
  test_routes.py
```


## Importing your existing files
Place your HTML/CSS/JS/assets into the `uploaded_files/` folder. Then run `python merge_uploaded.py` to import them into the project structure.
