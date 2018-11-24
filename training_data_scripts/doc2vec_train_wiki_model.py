import multiprocessing
from pprint import pprint

from gensim.corpora.wikicorpus import WikiCorpus
from gensim.models.doc2vec import Doc2Vec, TaggedDocument, FAST_VERSION

assert FAST_VERSION > -1, "This will be painfully slow otherwise"

wiki = WikiCorpus("../enwiki-latest-pages-articles.xml.bz2")


class TaggedWikiDocument(object):
    def __init__(self, wiki):
        self.wiki = wiki
        self.wiki.metadata = True

    def __iter__(self):
        for content, (page_id, title) in self.wiki.get_texts():
            yield TaggedDocument(content, [title])


documents = TaggedWikiDocument(wiki)

cores = multiprocessing.cpu_count()
model = Doc2Vec(dm=1, dm_mean=1, size=200, window=8, min_count=10, iter=10, workers=cores)

model.build_vocab(documents)
model.train(documents, total_examples=model.corpus_count, epochs=model.iter)

pprint(model.docvecs.most_similar(positive=["Automatic summarization"], topn=20))

model.save("wikipedia-vectors.d2v")
