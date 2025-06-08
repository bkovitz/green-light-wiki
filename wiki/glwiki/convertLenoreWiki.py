# convertLenoreWiki.py -- Converts wikitext files from the pre-2025 Lenore
#                         wiki to markdown

import re
from VersionedFile2 import VersionedFile2
from WikiRepository import WikiRepository
from WikiText2 import ParagraphList, _parseParas

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

def get_page_version(title, version):
    pageFile = repo.pageFile(title)
    f = pageFile.openForReading()
    v = VersionedFile2(f)
    wikitext = v.getVersion(version)
    return wikitext

def fix_line_tokens(wikitext):
    token_types = "((?:\$\$.+?\$\$)|(?:\[\[.+?\]\])|(?:http://\S+)|(?:ftp://\S+)|(?:https://\S+)|(?:mailto:\S+)|(?:\<)|(?:\>)|(?:\&)|(?:\w+)|(?:\s+)|(?:-{4,})|(?:''')|(?:'')|(?:[^\w\s]))"
    result = []

    for line in wikitext:
        fixed_line = []
        for token in re.findall(token_types, line.strip()):
            fixed_line.append(replace_token(token))
        result.append(''.join(fixed_line))
    return result

def fix_paras(paras):
    regex = "^(?P<equals>={1,5})(?P<text>[^=].*?)(={1,5})$"
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

wikitext = get_page_version("Politicians-and-Saints_Exegesis", 7)
markdown = convert_to_markdown(wikitext)

for para in markdown:
    print(para)
