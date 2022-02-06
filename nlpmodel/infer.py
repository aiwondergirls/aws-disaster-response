import numpy
import tflearn
import tensorflow
import random
import json

import nltk
nltk.download('punkt')
from nltk.stem.lancaster import LancasterStemmer
stemmer = LancasterStemmer()

def predict(input, type):
    if type == "earthquake":
        with open("./nlpmodel/data/earthquake_intents.json") as file:
            data = json.load(file)
    else:
        with open("./nlpmodel/data/firstaid_intents.json") as file:
            data = json.load(file)
    
    words = []
    labels = []
    docs_x = []
    docs_y = []

    for intent in data["intents"]:
        for pattern in intent["patterns"]:
            wrds = nltk.word_tokenize(pattern)
            words.extend(wrds)
            docs_x.append(wrds)
            docs_y.append(intent["tag"])

        if intent["tag"] not in labels:
            labels.append(intent["tag"])

    words = [stemmer.stem(w.lower()) for w in words if w != "?"]
    words = sorted(list(set(words)))

    labels = sorted(labels)

    training = []
    output = []

    out_empty = [0 for _ in range(len(labels))]

    for x, doc in enumerate(docs_x):
        bag = []

        wrds = [stemmer.stem(w) for w in doc]

        for w in words:
            if w in wrds:
                bag.append(1)
            else:
                bag.append(0)
        output_row = out_empty[:]
        output_row[labels.index(docs_y[x])] = 1

        training.append(bag)
        output.append(output_row)
    
    training = numpy.array(training)
    output = numpy.array(output)

    tensorflow.compat.v1.reset_default_graph()

    net = tflearn.input_data(shape=[None, len(training[0])])
    net = tflearn.fully_connected(net, 8)
    net = tflearn.fully_connected(net, 8)
    net = tflearn.fully_connected(net, len(output[0]), activation="softmax")
    net = tflearn.regression(net)

    model = tflearn.DNN(net)

    if type == "earthquake":
        model.load("./nlpmodel/models/model_earthquake.tflearn")
    else:
        model.load("./nlpmodel/models/model_firstaid.tflearn")

    results = model.predict([bag_of_words(input, words)])[0]
    results_index = numpy.argmax(results)
    tag = labels[results_index]
    
    if results[results_index] > 0.55:
        for tg in data["intents"]:
            if tg['tag'] == tag:
                responses = tg['responses']
        return(random.choice(responses))
    
    else:
        return("I didnt get that, try again")



def bag_of_words(s,words):
	bag = [0 for _ in range(len(words))]


	s_words = nltk.word_tokenize(s)
	s_words = [stemmer.stem(word.lower()) for word in s_words]

	for se in s_words:
		for i, w in enumerate(words):
			if w == se:
				bag[i] = 1

	return numpy.array(bag)