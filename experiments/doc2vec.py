import multiprocessing
import time
from pprint import pprint

import gensim.models.doc2vec
from gensim.corpora.wikicorpus import WikiCorpus
from gensim.models.doc2vec import Doc2Vec, TaggedDocument

assert gensim.models.doc2vec.FAST_VERSION > -1, "This will be painfully slow otherwise"

cores = multiprocessing.cpu_count()


class TaggedWikiDocument(object):
    def __init__(self, wiki):
        self.wiki = wiki
        self.wiki.metadata = True

    def __iter__(self):
        for content, (page_id, title) in self.wiki.get_texts():
            yield TaggedDocument([c.decode("utf-8") for c in content], [title])


print("Loading Wiki Corpus")
wiki = WikiCorpus("../enwiki-latest-pages-articles.xml.bz2")
print(type(wiki))
documents = TaggedWikiDocument(wiki)

print("Done")

model = Doc2Vec(dm=0, dbow_words=1, size=200, window=8, min_count=19, iter=10, workers=cores)

model.build_vocab(documents)
print(str(model))

start = time.time()
print("Training model")
model.train(documents, total_examples=model.corpus_count, epochs=model.iter)
model.save("wikipedia-vectors.d2v")
print(time.time() - start)

pprint(model.docvecs.most_similar(positive=["Automatic summarization"], topn=20))
