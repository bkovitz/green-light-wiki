# Wikitext Conversion Plan

So we are going to run `dumpLenoreWiki.py()` to:

1. Reconstruct the versions of the pages
2. Convert the pages from wikitext to markdown
3. Store the converted pages in a db (Postgres?)

Today's plan:

1. ~~Stare at markdown files (the files manually updated by April) to understand what needs to be changed.~~
2. ~~Choose which set of files to update first.~~
3. ~~Stare at old wikitext files to understand what needs to be changed.~~
4. ~~Write Python code to convert the first set of files. (mdlinkToWikilink.py)~~
5. ~~Convert Vercel markdown files to the new format~~ resulting files are in `vercel-double-brackets/`
6. For the old textfiles: stare at old Python code to see what existing code we can exploit.
7. Write Python code to convert the other set of files.
8. Manually merge updated markdown files and updated wikitext files to make the final set of files for the new wiki.

## Vercel markdown files

[Lenore Thomson](/wiki/main/typologists/lenore-thomson) -> [[Lenore Thomson]]
[Lenore](/wiki/main/typologists/lenore-thomson) -> [[Lenore Thomson|Lenore]]

### With internal links

* The part in brackets is the alias.
* The last slug determines the page name. Convert to title case.
* Replace all with [[Page Name]] or [[Page Name|Alias]] depending on whether the alias is different from the page name.
* [The Unknown Citizen](https://poets.org/poem/unknown-citizen) -> [The Unknown Citizen](https://poets.org/poem/unknown-citizen)
* That is, don't change external links.

### Frontmatter

* date: 2025-05-27 20:00:00
* author: Unknown
* version: 1 In step 7, manually change this to latest version + 1.

## Old wikitext files

page name: Change to "title:". Change the underscores to spaces.
Change names in camel case to have a space between words. ASimpleExegesis -> A Simple Exegesis
versionNum: Change to "version:".
[[Personality Type: An Owner's Manual http://www.amazon.com/exec/obidos/ASIN/0877739870/ref=ase_greenlightwik-20]] - [Personality Type: An Owner's Manual](http://www.amazon.com/exec/obidos/ASIN/0877739870/ref=ase_greenlightwik-20)
Only change double brackets if there is a URL inside. Then change to single brackets followed by URL in parentheses.
= Abraham in the Desert = -> ## Abraham in the Desert
== What this wiki is about == -> ## What this wiki is about
---- -> ---
''Si'' -> _Si_
'''How I got into this''' -> **How I got into this**
 \* Some text -> - Some text (with a space before the hyphen)
 # Some text -> 1. Some text (maybe just do this by hand, since it only occurs in one file)
