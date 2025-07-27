# convertLenoreWiki.py -- Converts wikitext files from the pre-2025 Lenore
#                         wiki to markdown

import re
from pathlib import Path

from VersionedFile2 import VersionedFile2
from WikiRepository import WikiRepository
from WikiText2 import ParagraphList, _parseParas
from UnsmashWords import unsmashWords

# def printAllVersions(f):
#     pageFile = repo.pageFile(pageName)
#     f = pageFile.openForReading()
#     v = VersionedFile2(f)

#     for i in range(1, v.getLatestVersionNum() + 1):
#         print('page name:', pageName)
#         info = v.getVersionInfo(i)
#         print('versionNum:', info.versionNum)
#         print('date:', info.date)
#         print('author:', info.author)
#         print('text:', )
#         for line in v.getVersion(i):
#             print(line, end='')
#         print("@@")

repo = WikiRepository('../lenore-exegesis')

def replace_token(token):
    if token[0:4] == "----":
        return "---"
    # elif word.startswith("[[") and word.endswith("]]"):
    #     return _bracketLink(word[2:-2])
    elif token == "''": # italics
        return "_"
    elif token == "'''": # bold
        return "**"
    else:
        return token

def get_page_info(title, version):
    pageFile = repo.pageFile(title)
    f = pageFile.openForReading()
    v = VersionedFile2(f)
    wikitext = v.getVersion(version)
    title = unsmashWords(title)
    author = v.getVersionInfo(version).author
    date = convert_timestamp(v.getVersionInfo(version).date)
    return [wikitext, title, author, date]

def convert_timestamp(timestamp):
    arr = timestamp.split('.')
    return "-".join([str(n) for n in arr[:3]]) + " " + ":".join([str(n) for n in arr[3:6]])

def fix_line_tokens(wikitext):
    token_types = r"((?:\$\$.+?\$\$)|(?:\[\[.+?\]\])|(?:http://\S+)|(?:ftp://\S+)|(?:https://\S+)|(?:mailto:\S+)|(?:\<)|(?:\>)|(?:\&)|(?:\w+)|(?:\s+)|(?:-{4,})|(?:''')|(?:'')|(?:[^\w\s]))"
    result = []

    for line in wikitext:
        fixed_line = []
        for token in re.findall(token_types, line.strip()):
            fixed_line.append(replace_token(token))
        result.append(''.join(fixed_line))
    return result

def fix_paras(paras):
    regex = r"^(?P<equals>={1,5})(?P<text>[^=].*?)(={1,5})$"
    d = {'=': '##', '==': '##', '===': '###', '====': '####', '=====': '#####'}
    for para in paras:
        if para.startswith("="): # Heading
            m = re.match(regex, para)
            if m:
                heading = d[m.groupdict()["equals"]]
                text = m.groupdict()['text']
                yield f'{heading} {text}'
            else:
                yield para
        elif para.startswith("* "): # Unordered List
            yield ' - ' + para[2:]
        elif para.startswith("# "): # Ordered List
            yield '1. ' + para[2:]
        else:
            yield para

def convert_to_markdown(wikitext):
    fixed_tokens = fix_line_tokens(wikitext)
    paras = _parseParas(fixed_tokens)
    fixed_paras = fix_paras(paras)

    for para in fixed_paras:
        yield para


def get_all_filenames():
    directory = Path("../lenore-exegesis")
    for file in directory.iterdir():
        yield file.name

def versions_of(title):
    pageFile = repo.pageFile(title)
    f = pageFile.openForReading()
    v = VersionedFile2(f)

    for version_num in range(1, v.getLatestVersionNum()):
        yield version_num

def new_path_for(title, version_num):
    return 'wikitext-converted/' + title + '.' + str(version_num) + '.md'

def create_markdown(filename, version_num, f):
    wikitext, title, author, date = get_page_info(filename, version_num)
    markdown = convert_to_markdown(wikitext)

    print("---", file = f)
    print(f"title: {title}", file = f)
    print(f"author: {author}", file = f)
    print(f"version: {version_num}", file = f)
    print(f"date: {date}", file = f)
    print("---", file = f)

    for para in markdown:
        print(para, file = f)

if __name__ == '__main__':
    for filename in get_all_filenames():
        for version_num in versions_of(filename):
            with open(new_path_for(filename, version_num), 'w', encoding='utf-8') as f:
                create_markdown(filename, version_num, f)
