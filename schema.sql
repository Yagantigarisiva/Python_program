PRAGMA foreign_keys = ON;

-- Pages table (editable content repository)
DROP TABLE IF EXISTS pages;
CREATE VIRTUAL TABLE pages USING fts5(
  title UNINDEXED,
  slug UNINDEXED,
  content,
  tokenize='porter'
);

-- A small ranking helper for FTS5
DROP VIEW IF EXISTS pages_ranked;
CREATE VIEW pages_ranked AS
SELECT rowid, title, slug, content,
       bm25(pages, 1.0, 0.5, 2.0) AS rank
FROM pages;
