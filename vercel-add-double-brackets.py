#!python3
# or
#!python
import re
import sys
from pathlib import Path
import traceback

def convert(input_filename, output_filename):
    md_text = open(input_filename, 'r').read()
    token_types = r"((?:\[.+?\]\(.*?\))|(?:\S+)|(?:\s+))"
    tokens = re.findall(token_types, md_text)

    output_filepath = Path(output_filename)
    output_filepath.parent.mkdir(parents=True, exist_ok=True)
    output_file = open(output_filename, 'w')

    for token in tokens:
        if token.startswith('['):
            regex = r"\[(?P<link_text>.+?)\]\((?P<url>.+?)\)"
            m = re.match(regex, token)
            if m:
                try:
                    link_text = m.group("link_text")
                except Exception as e:
                    print("Error in m.group:", token, m)
                url = m.group("url")

                if url.startswith('http'):  # external link
                    pass
                else:  # internal link
                    last_slug = url.split('/')[-1]
                    page_title_words = kebab_to_title(last_slug.split('-'))

                    if page_title_words and page_title_words[-1] == 'Archive':
                        page_title_words.pop()

                    anchor_words = kebab_to_title(link_text.split())

                    if anchor_words == page_title_words:
                        token = f'[[{link_text}]]'
                    else:
                        page_title = ' '.join(page_title_words)
                        token = f'[[{page_title}|{link_text}]]'

        print(token, end='', file=output_file)

def kebab_to_title(words):
    return [
        word[0].upper() + word[1:]
            for word in words
    ]

try:
    convert(sys.argv[1], sys.argv[2])
    print("Finished converting", sys.argv[1])
except Exception as e:
    print("Failed in", sys.argv[1])
    traceback.print_exc()
