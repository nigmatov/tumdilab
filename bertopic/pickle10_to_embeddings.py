import json
import pickle
import sys

if len(sys.argv) < 3:
    sys.exit(1)

embeddings = pickle.load(open(sys.argv[1], 'rb'))
i = 0

results = []

with open(sys.argv[2] + 'bertopic10', 'w') as fout:
    with open(sys.argv[2], 'r') as fin_docs:
        for line in fin_docs:
            line_json = json.loads(line)
            line_json['_source']['topics_bertopic_10'] = embeddings[i]
            fout.write(json.dumps(line_json))
            fout.write('\n')
            i += 1