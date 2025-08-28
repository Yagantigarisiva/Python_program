from flask import Flask, render_template, request, redirect, url_for, abort, g
import sqlite3
import os
from html import escape

APP_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(APP_DIR, "data", "site.db")

def get_db():
    if "db" not in g:
        g.db = sqlite3.connect(DB_PATH)
        g.db.row_factory = sqlite3.Row
    return g.db

def close_db(e=None):
    db = g.pop("db", None)
    if db is not None:
        db.close()

def init_app(app: Flask):
    app.teardown_appcontext(close_db)

def create_app():
    app = Flask(__name__)
    init_app(app)

    @app.route("/")
    def home():
        # Render index, content goes in <main> of index.html
        return render_template("index.html", title="Home")

    @app.route("/about")
    def about():
        return render_template("about.html", title="About")

    @app.route("/contact")
    def contact():
        return render_template("contact.html", title="Contact")

    @app.route("/search")
    def search():
        q = request.args.get("q", "").strip()
        rows = []
        if q:
            db = get_db()
            # Use FTS5 table for ranking
            sql = """
            SELECT p.rowid, p.slug, p.title,
                   snippet(p, 2, '<mark>', '</mark>', ' … ', 15) AS snippet
            FROM pages p
            WHERE pages MATCH ?
            ORDER BY rank;
            """
            # Simple query; wrap user query in quotes for phrase search fallbacks.
            try:
                rows = db.execute(sql, (q,)).fetchall()
            except sqlite3.OperationalError:
                # fallback to LIKE if FTS phrase causes error
                rows = db.execute(
                    "SELECT slug, title, substr(content,1,200) as snippet FROM pages WHERE content LIKE ?",
                    (f"%{q}%",)
                ).fetchall()
        return render_template("search.html", title="Search", q=q, rows=rows)

    @app.route("/pages/<slug>")
    def page(slug):
        db = get_db()
        row = db.execute("SELECT title, content FROM pages WHERE slug = ?", (slug,)).fetchone()
        if not row:
            abort(404)
        # Render content inside the base layout main region
        return render_template("index.html", dynamic_content=row["content"], title=row["title"])

    # Simple dev-only reindex endpoint
    @app.route("/admin/reindex")
    def reindex():
        db = get_db()
        with open(os.path.join(APP_DIR, "data", "schema.sql"), "r", encoding="utf-8") as f:
            schema_sql = f.read()
        db.executescript(schema_sql)
        with open(os.path.join(APP_DIR, "data", "seed.sql"), "r", encoding="utf-8") as f:
            seed_sql = f.read()
        db.executescript(seed_sql)
        db.commit()
        return "Reindexed."

    return app

app = create_app()

if __name__ == "__main__":
    app.run(debug=True)
