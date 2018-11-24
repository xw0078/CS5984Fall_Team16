# -*- mode: python; -*-

"""Clean wiki text:
This script uses methods developed for the Wikipedia Extractor project, with some minor modifications
see: http://medialab.di.unipi.it/wiki/Wikipedia_Extractor
"""

import json
import re
from itertools import zip_longest

from smart_open import smart_open, codecs

selfClosingTags = ('br', 'hr', 'nobr', 'ref', 'references', 'nowiki')

placeholder_tags = {'math': 'formula', 'code': 'codice'}

# Match HTML comments
# The buggy template {{Template:T}} has a comment terminating with just "->"
comment = re.compile(r'<!--.*?-->', re.DOTALL)

# Match <nowiki>...</nowiki>
nowiki = re.compile(r'<nowiki>.*?</nowiki>')

# Match selfClosing HTML tags
selfClosing_tag_patterns = [
    re.compile(r'<\s*%s\b[^>]*/\s*>' % tag, re.DOTALL | re.IGNORECASE) for tag in selfClosingTags
]

# Match HTML placeholder tags
placeholder_tag_patterns = [
    (re.compile(r'<\s*%s(\s*| [^>]+?)>.*?<\s*/\s*%s\s*>' % (tag, tag), re.DOTALL | re.IGNORECASE),
     repl) for tag, repl in placeholder_tags.items()
]

# Match preformatted lines
preformatted = re.compile(r'^ .*?$')

# Match external links (space separates second optional parameter)
externalLink = re.compile(r'\[\w+[^ ]*? (.*?)]')
externalLinkNoAnchor = re.compile(r'\[\w+[&\]]*\]')

# Matches bold/italic
bold_italic = re.compile(r"'''''(.*?)'''''")
bold = re.compile(r"'''(.*?)'''")
italic_quote = re.compile(r"''\"([^\"]*?)\"''")
italic = re.compile(r"''(.*?)''")
quote_quote = re.compile(r'""([^"]*?)""')

# Matches space
spaces = re.compile(r' {2,}')

# Matches dots
dots = re.compile(r'\.{4,}')

# match tail after wikilink
tailRE = re.compile('\w+')

syntaxhighlight = re.compile('&lt;syntaxhighlight .*?&gt;(.*?)&lt;/syntaxhighlight&gt;', re.DOTALL)

# skip level 1, it is page name level
section = re.compile(r'(==+)\s*(.*?)\s*\1')

keep_tables = False
keepSections = True
keepLists = True


def wiki2text(text):
    # Drop tables
    # first drop residual templates, or else empty parameter |} might look like end of table.
    if not keep_tables:
        text = dropNested(text, r'{{', r'}}')
        text = dropNested(text, r'{\|', r'\|}')
        text = dropNested(text, r':{', r'   ')

    # Handle bold/italic/quote
    text = bold_italic.sub(r'\1', text)
    text = bold.sub(r'\1', text)
    text = italic_quote.sub(r'"\1"', text)
    text = italic.sub(r'"\1"', text)
    text = quote_quote.sub(r'"\1"', text)
    # residuals of unbalanced quotes
    text = text.replace("'''", '').replace("''", '"')

    return text


def clean(text):
    """
    Removes irrelevant parts from :param: text.
    """

    # Collect spans
    spans = []
    # Drop HTML comments
    for m in comment.finditer(text):
        spans.append((m.start(), m.end()))

    # Drop self-closing tags
    for pattern in selfClosing_tag_patterns:
        for m in pattern.finditer(text):
            spans.append((m.start(), m.end()))

    # Drop ignored tags
    # for left, right in options.ignored_tag_patterns:
    #     for m in left.finditer(text):
    #         spans.append((m.start(), m.end()))
    #     for m in right.finditer(text):
    #         spans.append((m.start(), m.end()))

    # Bulk remove all spans
    text = dropSpans(spans, text)

    # Drop discarded elements
    # for tag in options.discardElements:
    #     text = dropNested(text, r'<\s*%s\b[^>/]*>' % tag, r'<\s*/\s*%s>' % tag)

    # Expand placeholders
    for pattern, placeholder in placeholder_tag_patterns:
        index = 1
        for match in pattern.finditer(text):
            text = text.replace(match.group(), '%s_%d' % (placeholder, index))
            index += 1

    text = text.replace('<<', '«').replace('>>', '»')

    #############################################

    # Cleanup text
    text = text.replace('\t', ' ')
    text = spaces.sub(' ', text)
    text = dots.sub('...', text)
    text = re.sub(' (,:\.\)\]»)', r'\1', text)
    text = re.sub('\([^a-zA-Z\d]*\)', '', text)
    text = re.sub('(\[\(«) ', r'\1', text)
    text = re.sub(r'\n\W+?\n', '\n', text, flags=re.U)  # lines with only punctuations
    text = text.replace(',,', ',').replace(',.', '.')
    text = text.replace(' , ', ', ')
    if keep_tables:
        # the following regular expressions are used to remove the wikiml chartacters around table strucutures
        # yet keep the content. The order here is imporant so we remove certain markup like {| and then
        # then the future html attributes such as 'style'. Finally we drop the remaining '|-' that delimits cells.
        text = re.sub(r'!(?:\s)?style=\"[a-z]+:(?:\d+)%;\"', r'', text)
        text = re.sub(r'!(?:\s)?style="[a-z]+:(?:\d+)%;[a-z]+:(?:#)?(?:[0-9a-z]+)?"', r'', text)
        text = text.replace('|-', '')
        text = text.replace('|', '')
    text = text.replace('(; ', '(')
    text = text.strip()
    return text


def compact(text):
    """Deal with headers, lists, empty sections, residuals of tables."""

    page = []  # list of paragraph
    headers = {}  # Headers for unfilled sections
    emptySection = False  # empty sections are discarded
    listLevel = []  # nesting of lists
    listCount = []  # count of each list (it should be always in the same length of listLevel)
    for line in text.split('\n'):
        if not line:  # collapse empty lines
            # if there is an opening list, close it if we see an empty line
            if len(listLevel):
                page.append(line)
                listLevel = []
                listCount = []
                emptySection = False
            elif page and page[-1]:
                page.append('')
            continue
        # Handle section titles
        m = section.match(line)
        if m:
            title = m.group(2)
            lev = len(m.group(1))  # header level
            if title and title[-1] not in '!?':
                title += '.'  # terminate sentence.
            headers[lev] = title
            # drop previous headers
            for i in list(headers.keys()):
                if i > lev:
                    del headers[i]
            emptySection = True
            listLevel = []
            listCount = []
            continue
        # Handle page title
        elif line.startswith('++'):
            title = line[2:-2]
            if title:
                if title[-1] not in '!?':
                    title += '.'
                page.append(title)
        # handle indents
        elif line[0] == ':':
            # page.append(line.lstrip(':*#;'))
            continue
        # handle lists
        elif line[0] in '*#;:':
            i = 0
            # c: current level char
            # n: next level char
            for c, n in zip_longest(listLevel, line, fillvalue=''):
                if not n or n not in '*#;:':  # shorter or different
                    if c:
                        listLevel = listLevel[:-1]
                        listCount = listCount[:-1]
                        continue
                    else:
                        break
                # n != ''
                if c != n and (not c or (c not in ';:' and n not in ';:')):
                    if c:
                        # close level
                        listLevel = listLevel[:-1]
                        listCount = listCount[:-1]
                    listLevel += n
                    listCount.append(0)
                i += 1
            n = line[i - 1]  # last list char
            line = line[i:].strip()
            if line:  # FIXME: n is '"'
                if keepLists:
                    if keepSections:
                        # emit open sections
                        items = sorted(headers.items())
                        for _, v in items:
                            page.append(v)
                    headers.clear()
                    # use item count for #-lines
                    listCount[i - 1] += 1
                    bullet = '%d. ' % listCount[i - 1] if n == '#' else '- '
                    page.append('{0:{1}s}'.format(bullet, len(listLevel)) + line)
        elif len(listLevel):
            listLevel = []
            listCount = []
            page.append(line)

        # Drop residuals of lists
        elif line[0] in '{|' or line[-1] == '}':
            continue
        # Drop irrelevant lines
        elif (line[0] == '(' and line[-1] == ')') or line.strip('.-') == '':
            continue
        elif len(headers):
            if keepSections:
                items = sorted(headers.items())
                for i, v in items:
                    page.append(v)
            headers.clear()
            page.append(line)  # first line
            emptySection = False
        elif not emptySection:
            # Drop preformatted
            if line[0] != ' ':  # dangerous
                page.append(line)
    return page


def dropNested(text, openDelim, closeDelim):
    """
    A matching function for nested expressions, e.g. namespaces and tables.
    """
    openRE = re.compile(openDelim, re.IGNORECASE)
    closeRE = re.compile(closeDelim, re.IGNORECASE)
    # partition text in separate blocks { } { }
    spans = []  # pairs (s, e) for each partition
    nest = 0  # nesting level
    start = openRE.search(text, 0)
    if not start:
        return text
    end = closeRE.search(text, start.end())
    next = start
    while end:
        next = openRE.search(text, next.end())
        if not next:  # termination
            while nest:  # close all pending
                nest -= 1
                end0 = closeRE.search(text, end.end())
                if end0:
                    end = end0
                else:
                    break
            spans.append((start.start(), end.end()))
            break
        while end.end() < next.start():
            # { } {
            if nest:
                nest -= 1
                # try closing more
                last = end.end()
                end = closeRE.search(text, end.end())
                if not end:  # unbalanced
                    if spans:
                        span = (spans[0][0], last)
                    else:
                        span = (start.start(), last)
                    spans = [span]
                    break
            else:
                spans.append((start.start(), end.end()))
                # advance start, find next close
                start = next
                end = closeRE.search(text, next.end())
                break  # { }
        if next != start:
            # { { }
            nest += 1
    # collect text outside partitions
    return dropSpans(spans, text)


def dropSpans(spans, text):
    """
    Drop from text the blocks identified in :param spans:, possibly nested.
    """
    spans.sort()
    res = ''
    offset = 0
    for s, e in spans:
        if offset <= s:  # handle nesting
            if offset < s:
                res += text[offset:s]
            offset = e
    res += text[offset:]
    return res


def main():
    articles = 300
    count = 1

    in_file = '../ETD_related_abstract_v3.json'
    out_file = '../ETD_related_abstract_v5.json'

    with smart_open(out_file, 'wb') as fout:
        with smart_open(in_file, 'rb') as fin:
            for line in fin:
                count += 1

                data = json.loads(line)
                data['introduction'] = ' '.join(compact(clean(wiki2text(data['introduction']))))
                data['textbody'] = ' '.join(compact(clean(wiki2text(data['textbody']))))

                if len(data['introduction']) < 50 or len(data['textbody']) < 100:
                    continue

                # print(data['introduction'])
                # print()
                # print(data['textbody'])
                # print()

                json.dump(data, codecs.getwriter('utf-8')(fout), ensure_ascii=False)
                fout.write(b'\n')
                #
                # if count > articles:
                #     break


if __name__ == "__main__":
    main()
