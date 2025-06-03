import re

f = open('../markdown-backup/index.md', 'r')
mdtext = f.read()

# Spits out the file
tokenTypes = r"((?:\[.+?\]\(.*?\))|(?:\S+)|(?:\s+))"
tokens = re.findall(tokenTypes, mdtext)

def kebab_to_title(words):
    return [
        word[0].upper() + word[1:]
            for word in words
    ]

for token in tokens:
  if token.startswith('['):
    regex = r"\[(?P<link_text>.+?)\]\((?P<url>.+?)\)"
    m = re.match(regex, token)

    link_text = m.group("link_text")
    url = m.group("url")

    if url.startswith('http'):  # external link
      pass
    else:  # internal link
      last_slug = url.split('/')[-1]

      page_title_words = kebab_to_title(last_slug.split('-'))
      if page_title_words[-1] == 'Archive':
        page_title_words.pop()

      anchor_words = kebab_to_title(link_text.split())

      if anchor_words == page_title_words:
        token = f'[[{link_text}]]'
      else:
        page_title = ' '.join(page_title_words)
        token = f'[[{page_title}|{link_text}]]'

  print(token, end='')

