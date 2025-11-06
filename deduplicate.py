import json
import os
import html
import unicodedata
import ndjson
import sys

from nltk.metrics.distance import jaccard_distance
from nltk.util import ngrams

filename = sys.argv[1]


documents = []

with open(filename,  encoding="utf8") as f:
    for line in f:
        documents.append(json.loads(line))

print(len(documents))

documents = [x for x in documents if "twitter" not in x['_source']['top_domain']]
documents = [x for x in documents if x['_source']['content_t'].count(" ") in range(200, 2000)]
documents = [x for x in documents if x['_source']['language'] == 'en']

def compute_similarity(a, b, n=1):
    tokens1 = a.split()
    tokens2 = b.split()
    try:
        jd = jaccard_distance(set(ngrams(tokens1, n)), set(ngrams(tokens2, n)))
    except ZeroDivisionError:
        jd = 0
    return 1 - jd

mask = {}
i=0
for line1 in documents:
    if (i % 100) == 0:
        print(i)
    if i in mask:
        i = i + 1
        continue
    text1 = line1['_source']['content_t'][0:511]
    j = i + 1
    if j >= len(documents):
        break
    for line2 in documents[j:j+1000] :
        if j in mask:
            j = j + 1
            continue
        text2 = line2['_source']['content_t'][0:511]
        #print(len(text1), ' ', len(text2))
        if compute_similarity(text1, text2) > 0.8 :
            mask[j] = 1
        j = j + 1
    i = i + 1

print(len(mask))

with  open(filename + "-output", 'w') as f:
    for k in range(0, len(documents)):
        if k in mask:
            continue
        else:
            f.write(json.dumps(documents[k]) + '\n')







