# DB Design

## Summary

Files -> DB -> Site -> Read Text

We left off at struggling with triggers and functions; the tables are complete.

- PostgreSQL
  - Decide on provider
  - Use full text search

## Plan

- [] Make page schema
  - Title (text)
  - Author (text)
  - Version (integer)
  - Text (text)
  - Date (timestamp)
- [] Plan relationships
  - Page to Author (one-to-many)
  - Page to Version (one-to-many)
- [] "Upload" markdown files to db

