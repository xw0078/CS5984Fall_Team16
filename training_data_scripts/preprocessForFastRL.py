import json
import os
import io

data = []
for line in open('All_filtered_related_wiki_gensim_v5.json', 'r', encoding = "utf-8"):
    data.append(json.loads(line))
i = -1

import pickle as pkl
import collections
vocab_counter = collections.Counter()
    
for item in data[0:190000]:

    js_example = {}
    js_example['id'] = item["id"]
    
    para = item["textbody"]
    
    para = para.replace('"', "'")
    para = "".join(filter(lambda x: ord(x)<128, para))
    sentences = para.split(".")
    sentences = [' '.join(line.lower().strip().split()) for line in sentences]
    sentences = [x for x in sentences if x]
    
    js_example['article'] = sentences
   
    abst = item["introduction"]
    abst = abst.replace('"', "'")
    abst = "".join(filter(lambda x: ord(x)<128, abst))
    absSen = abst.split(".")
    absSen = [' '.join(line.lower().strip().split()) for line in absSen]
    absSen = [x for x in absSen if x]
    
    if(not((len(sentences) > 3 * len(absSen)) and len(para) > 999 )):
        continue
    
    js_example['abstract'] = absSen
    i = i + 1
    if(i%1000 == 0):
        print("Processed: " + str(i))
        
    with io.open("./train/" + str(i) + '.json', 'w', encoding='utf8') as json_file:
        json.dump(js_example, json_file, indent = 4)

  
    art_tokens = ' '.join(sentences).split()
    abs_tokens = ' '.join(absSen).split()
    tokens = art_tokens + abs_tokens
    tokens = [t.strip() for t in tokens] # strip
    tokens = [t for t in tokens if t != ""] # remove empty
    vocab_counter.update(tokens)
    
print("Writing vocab file...")
with open("vocab_cnt.pkl", 'wb') as vocab_file:
    pkl.dump(vocab_counter, vocab_file)
print("Finished writing vocab file")

i = -1
print("Generate val")
for item in data[190000:254000]: 
   
    js_example = {}
    js_example['id'] = item["id"]
    
    para = item["textbody"]
    
    para = para.replace('"', "'")
    para = "".join(filter(lambda x: ord(x)<128, para))
    sentences = para.split(".")
    sentences = [' '.join(line.lower().strip().split()) for line in sentences]
    sentences = [x for x in sentences if x]
    
    js_example['article'] = sentences
   
    abst = item["introduction"]
    abst = abst.replace('"', "'")
    abst = "".join(filter(lambda x: ord(x)<128, abst))
    absSen = abst.split(".")
    absSen = [' '.join(line.lower().strip().split()) for line in absSen]
    absSen = [x for x in absSen if x]
    
    js_example['abstract'] = absSen
    if(not((len(sentences) > 3 * len(absSen)) and len(para) > 999 )):
        continue
    i = i + 1
    if(i%1000 == 0):
        print("Processed: " + str(i))
        
    with io.open("./val/" + str(i) + '.json', 'w', encoding='utf8') as json_file:
        json.dump(js_example, json_file, indent = 4)


i = -1
print("Generate Test")
for item in data[254000:]:
        
    
    js_example = {}
    js_example['id'] = item["id"]
    
    para = item["textbody"]
    
    para = para.replace('"', "'")
    para = "".join(filter(lambda x: ord(x)<128, para))
    sentences = para.split(".")
    sentences = [' '.join(line.lower().strip().split()) for line in sentences]
    sentences = [x for x in sentences if x]
    
    js_example['article'] = sentences
   
    abst = item["introduction"]
    abst = abst.replace('"', "'")
    abst = "".join(filter(lambda x: ord(x)<128, abst))
    absSen = abst.split(".")
    absSen = [' '.join(line.lower().strip().split()) for line in absSen]
    absSen = [x for x in absSen if x]
    
    if(not((len(sentences) > 3 * len(absSen)) and len(para) > 999 )):
        continue
    js_example['abstract'] = absSen
    i = i + 1
    if(i%1000 == 0):
        print("Processed: " + str(i))
    with io.open("./test/" + str(i) + '.json', 'w', encoding='utf8') as json_file:
        json.dump(js_example, json_file, indent = 4)
        


    
