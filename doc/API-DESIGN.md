md -> react (parser) -> react (jsx)

Use cases:

1. User views a page.

   GET /PageName

   Retrieve the latest version of the markdown for PageName.
   Do this in React back-end.

2. User edits a page.

   Front-end form.

   POST /PageName

3. User views a diff.

   GET /PageName?q=diff

Database?

- Page table + Version table? (Staying atomic)
- Each row is one version of a page

