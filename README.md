# Files in this folder:

1. deduplicate.py - script that preprocessed the original input
2. search_query - sample query of the dense vector
3. summarizers_testing.ipynb
4. two_embeddings_first_512.ipynb
5. prototype.ipynb - querying ES with embeddings to get semantically similar docs
6. compute_5_embeddings_test_index - compute 5 embeddings for the "test" index
7. prototype-test_index.ipynb - we used this to query "test" index to see which embeddings work better
8. prototype_with_reranking - reranking with a cross_encoder
9. prototype_combined_embeddings - linear combination of SBERT embedding and CTM
10. ctm_topic_modelling_inference - to do inference in CTM topic modelling


# bertopic

files to train and do inference with BERTOPIC, see README inside

# Compute Cloud

We had an instance set up in the LRZ compute cloud with the following parameters: 10 CPUs, 45GBs RAM, 400GBs storage, Ubuntu 20.04. 

base.yml was produced by conda env export > base.yml

requirements.txt was produced by pip freeze > requirements.txt

# ES_data

ES_data folder contains files segmentaaa, segmentaab, segmentaac, segmentaad which are to be uploaded into the Elasticsearch. It also contains mapping.json that creates the "posts" index and specifies its structure (see below how to insert mapping).

# web application (via Streamlit)

See README in the Streamlit folder

When working with prototype*.ipynb or Streamlit web application in order to query the ES instance from the local machine, one needs to set up an SSH tunnel as in: 

- ssh -i <path_to_your_private_key> <your_username>@INSTANCE_IP -L 9200:127.0.0.1:9200 -N -v

Alternatively, if one wants access to Kibana from the local machine:

- ssh -i <path_to_your_private_key> <your_username>@INSTANCE_IP -L 5601:127.0.0.1:5601 -N -v

# ElasticSearch

## Set up a running instance

Both ElasticSearch and Kibana are installed via Docker containers on the Ubuntu machine. In order to start them and access Elastic from your local computer,
run:

- docker start <elasticsearch_image> (start Elastic instance)

- docker start <kibana_image> (start Kibana instance)


Images can be created via the following commands(extracted from the official Elastic documentation):

- docker run --name es01-test --net elastic -p 9200:9200 -p 9300:9300 -e "discovery.type=single-node" docker.elastic.co/elasticsearch/elasticsearch:7.12.1

- docker run --name kib01-test --net elastic -p 5601:5601 -e "ELASTICSEARCH_HOSTS=http://es01-test:9200" docker.elastic.co/kibana/kibana:7.12.1

## Push data

In order to push the preprocessed data to Elastic, the elasticdump tool seems to provide the simplest way, due to the fact that our data is already in the format elasticdump requires. 

The data will be pushed as part of the "posts" index. Run the following for creating the index first
with the corresponding mapping:

- curl -i -X PUT 'http://localhost:9200/posts' -H "Content-Type: application/json" --data-binary "@mapping.json"

Then, run the following in order to insert the data.

- elasticdump --output=http://127.0.0.1:9200 --input=<file_name> --type=data --limit=1000

The limit argument specifies the number of documents (rows in our case, since each document is a row) which will be sent at once to Elastic via the BULK API. Due
to the size of the embeddings, the limit should be reasonably small (at 10000, for instance, elasticdump heap crashes due to lack of memory). In this example,
a limit of 1000 documents is used.

## Delete data


To delete an index(test, in this example), use:

- curl -XDELETE localhost:9200/test


To delete a field(distilbert_embedding, in this example) from an index (posts, in this example), use:

- curl -XPOST 'localhost:9200/posts/_update_by_query?wait_for_completion=true&conflicts=proceed' -H 'Content-Type:application/json' -d '{"script":"ctx._source.remove(\"distilbert_embedding\")", "query": {"exists": {"field": "distilbert_embedding"}}}'

## Update data

In order to update the data in Elasticsearch (adding an additional field, as in this example), one needs to use the UPDATE API (instead of the INDEX API, which overwrites existing documents), by first updating the mapping of the Elasticsearch index and then performing the actual updates via elasticdump.

To update the mapping, use:

- curl -X PUT "localhost:9200/posts/_mapping" -H 'Content-Type: application/json' -d'{
    "properties": {
        "topics_ctm_10": {
            "type":"dense_vector",
            "dims": 10
        },
        "topics_ctm_50": {
            "type":"dense_vector",
            "dims": 50
        }
    }
}'

This will update the mapping of the index *posts* by inserting 2 additional dense_vector fields with the properties mentioned in the inner JSON.

To perform the actual update, one needs to have the input files, and elasticdump can be used as before:

- elasticdump --output=http://127.0.0.1:9200 --input=<input_file> --type=data --limit=1000

