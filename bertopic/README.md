## BERTopic

Structure of the files:

- In BERTopic_training.ipynb, the code for training the model is present. All the final parameters that we've used are set, as well as the name of the input file (containing 100k documents, part of one of the segments of the elasticsearch data) and the name of the output file. One might want to change the names of these files for potential reprocessing.

- In BERTopic_reduction.ipynb, the code for reduction is present. The reduction is being made for 50 topics in this particular case. Same observation as before, one might want to change the names of the input and output files (from the specified ones in the file), as in the training case.

- In BERTopic_10topics_vs_50topics.ipynb, the code is responsible for comparing 2 models (one for 10 topics, one for 50 topics) based on a number of 10 arbitrary documents, which had been previously selected and then loaded in the file (names are customizable, as before).

- In BERTopic_inference.ipynb, the code that has been used to generate the topics for all the documents is present. The file has been run for each segment individually (the name of the first segment is provided) and the topics (described as a probability distribution) have been saved, in order, for each document in a .pickle file.

- pickle10_to_embeddings.py, the code for attaching the 10 topics to all the documents within each segment. The script must be run individually for each segment in the following way: python3 pickle10_to_embeddings. py <segment_pickle_file> <segment>

- pickle50_to_embeddings.py, the code for attaching the 50 topics to all the documents within each segment. The script must be run individually for each segment in the following way: python3 pickle50_to_embeddings. py <segment_pickle_file> <segment>

The last 2 scripts must be run sequentially on each segment, by providing the name of the resulting file from the first run as the second command line argument to the second script. Each of the 2 scripts outputs a file with the following name: <segment>_bertopic[10|50], dependening on the script. An example of running for one segment could be:

python3 pickle10_to_embeddings. py segment1_10_topics.pkl segment1
python3 pickle50_to_embeddings. py segment1_50_topics.pkl segment1bertopic10
