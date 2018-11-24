import nltk
from lxml.etree import strip_tags, strip_elements, parse

nltk.download('punkt')


def extract_ch_json(doc_path, doc_type, doc_id):
    """Return JSON from Grobid TEI

    This function tries to group sections of Grobid-generated TEI as chapters.
    """
    try:
        doc = parse(doc_path)
    except Exception as e:
        print('%s: %s' % (type(e).__name__, e))
        return 0

    # initial dict for information storage
    out_dict = {'id': doc_id, 'type': doc_type, 'title': '', 'chapters': []}

    # get document title
    titles = doc.xpath('/tei:TEI/tei:teiHeader/tei:fileDesc/tei:titleStmt/tei:title',
                       namespaces={'tei': 'http://www.tei-c.org/ns/1.0'})
    out_dict['title'] = '' if titles[0] is None else titles[0].text

    # get all tei:div elements that have headings
    divs = doc.xpath('/tei:TEI/tei:text/tei:body/tei:div[tei:head]',
                     namespaces={'tei': 'http://www.tei-c.org/ns/1.0'})

    iterator = iter(divs)
    div = next(iterator, None)
    while div is not None:
        head = div.find('tei:head', namespaces={'tei': 'http://www.tei-c.org/ns/1.0'})
        n = head.get('n')
        if n is None:  # assume this is a chapter heading
            chapter = {'title': f'{head.text}', 'paragraphs': []}
            paragraphs = []
            ps = div.findall('tei:p', namespaces={'tei': 'http://www.tei-c.org/ns/1.0'})
            for p in ps:
                # get rid of the <ref> elements
                strip_elements(p, '{http://www.tei-c.org/ns/1.0}ref', with_tail=False)
                # remove all other tags, but keep their content (e.g., <b>, etc)
                strip_tags(p, '{http://www.tei-c.org/ns/1.0}*')
                paragraphs.append(p.text)

            div = next(iterator, None)
            while True:
                if div is None:
                    chapter['paragraphs'] = paragraphs
                    out_dict['chapters'].append(chapter)
                    break
                head = div.find('tei:head', namespaces={'tei': 'http://www.tei-c.org/ns/1.0'})
                n = head.get('n')
                if n is not None:  # assume this is a subsection heading
                    paragraphs.append(f'{n} {head.text}')
                    ps = div.findall('tei:p', namespaces={'tei': 'http://www.tei-c.org/ns/1.0'})
                    for p in ps:
                        # get rid of the <ref> elements
                        strip_elements(p, '{http://www.tei-c.org/ns/1.0}ref', with_tail=False)
                        # remove all other tags, but keep their content (e.g., <b>, etc)
                        strip_tags(p, '{http://www.tei-c.org/ns/1.0}*')
                        paragraphs.append(p.text)
                else:
                    if paragraphs:
                        chapter['paragraphs'] = paragraphs
                        out_dict['chapters'].append(chapter)
                    break  # break out of this loop

                div = next(iterator, None)
        else:
            chapter = {'title': '', 'paragraphs': []}
            paragraphs = []
            while True:
                if div is None:
                    chapter['paragraphs'] = paragraphs
                    out_dict['chapters'].append(chapter)
                    break
                head = div.find('tei:head', namespaces={'tei': 'http://www.tei-c.org/ns/1.0'})
                n = head.get('n')
                if n is not None:  # assume this is a subsection heading
                    paragraphs.append(f'{n} {head.text}')
                    ps = div.findall('tei:p', namespaces={'tei': 'http://www.tei-c.org/ns/1.0'})
                    for p in ps:
                        # get rid of the <ref> elements
                        strip_elements(p, '{http://www.tei-c.org/ns/1.0}ref', with_tail=False)
                        # remove all other tags, but keep their content (e.g., <b>, etc)
                        strip_tags(p, '{http://www.tei-c.org/ns/1.0}*')
                        paragraphs.append(p.text)
                else:
                    if paragraphs:
                        chapter['paragraphs'] = paragraphs
                        out_dict['chapters'].append(chapter)
                    break  # break out of this loop

                div = next(iterator, None)

    return out_dict


if __name__ == '__main__':
    """Extract sentences from Grobid TEI XML
    
    For each chapter, print the chapter title. Then print each sentence on a new line. 
    """

    docPath = '/Users/waingram/Desktop/gorbid_fulltext/theses/17274/Granstedt_JL_T_2017.tei.xml'
    ch_json = extract_ch_json(docPath, 'thesis', 17292)

    for chapter in ch_json['chapters']:
        print()
        print(chapter['title'])
        print('--')
        for paragraph in chapter['paragraphs']:
            sentences = nltk.sent_tokenize(paragraph)
            for sentence in sentences:
                print(sentence)
