import tensorflow

from keras import layers, models, optimizers
from keras.layers import LSTM, GRU, Bidirectional
from keras.optimizers import SGD, RMSprop, Adadelta, Adam
from keras.preprocessing import text, sequence
from keras.callbacks import ReduceLROnPlateau, ModelCheckpoint, LearningRateScheduler
from keras import backend as k
import numpy as np
import pandas as pd
import io
import os
from statistics import mean, stdev, median
from sklearn import model_selection, preprocessing, linear_model, naive_bayes, metrics, svm
from sklearn.model_selection import train_test_split, StratifiedKFold
from sklearn.utils import shuffle
from collections import Counter
import math
import matplotlib.pyplot as plt
import csv
from .utilities import *

def load_patents(file):
    trainDF = pd.read_csv(file, header=None, usecols=[0, 1])
    trainDF = trainDF.rename(columns={0: 'label'})
    trainDF = trainDF.rename(columns={1: 'text'})

    print("Loaded")

    return trainDF


def encode_labels(trainDF):
    labels_val = trainDF['label'].values
    onehot_encoder = preprocessing.OneHotEncoder(sparse=False)
    onehot_encoded = onehot_encoder.fit_transform(labels_val.reshape(-1, 1))

    print("Example, label: ", labels_val[0], "\n", "One-hot encoding:", onehot_encoded[0], "\n")

    return onehot_encoded, onehot_encoder


def enumarate_codes(onehot_encoded):
    number_of_codes = np.shape(onehot_encoded)
    number_of_codes = number_of_codes[1]

    print("Number of ipc codes: ", number_of_codes, "\n")

    return number_of_codes


def split_dataset(trainDF, onehot_encoded):
    train_x, valid_x, train_y, valid_y = train_test_split(trainDF['text'], onehot_encoded, test_size=0.2,
                                                          random_state=42)  # stratify=onehot_encoded
    test_x, valid_x, test_y, valid_y = train_test_split(valid_x, valid_y, test_size=0.5, random_state=41)
    print("split_abstract_dataset-Done! \n")

    # Number of data per split
    number_of_train_data = np.shape(train_x)
    number_of_train_data = number_of_train_data[0]
    print("Number of train data:", number_of_train_data)

    number_of_valid_data = np.shape(valid_x)
    number_of_valid_data = number_of_valid_data[0]
    print("Number of validation data:", number_of_valid_data)

    number_of_test_data = np.shape(test_x)
    number_of_test_data = number_of_test_data[0]
    print("Number of test data:", number_of_test_data, "\n")

    return train_x, train_y, valid_x, valid_y, test_x, test_y, number_of_test_data


def tokenize_text(trainDF):
    token = text.Tokenizer()
    token.fit_on_texts(trainDF['text'])
    word_index = token.word_index

    print('Number of unique words:', len(word_index), "\n")

    return token, word_index


def convert_text(number_of_words, token, train_x, valid_x, test_x):
    maxlen = number_of_words

    train_seq_x = sequence.pad_sequences(token.texts_to_sequences(train_x), maxlen)
    valid_seq_x = sequence.pad_sequences(token.texts_to_sequences(valid_x), maxlen)
    test_seq_x = sequence.pad_sequences(token.texts_to_sequences(test_x), maxlen)

    print('convert text to tokens - Done! \n')

    return train_seq_x, valid_seq_x, test_seq_x


def load_fasttext(fname):
    data = {}
    fin = io.open(fname, 'r', encoding='utf-8', newline='\n', errors='ignore')
    n, d = map(int, fin.readline().split())
    for line in fin:
        tokens = line.rstrip().split(' ')
        data[tokens[0]] = np.array(list(map(float, tokens[1:])))

    print("load_patentVec-Done! \n")

    return data


def create_embedding_matrix(embeddings_index, word_index):
    num_words = len(word_index) + 1
    embedding_matrix = np.zeros((num_words, 300))

    for word, i in word_index.items():
        embedding_vector = embeddings_index.get(word)
        if embedding_vector is not None:
            embedding_matrix[i] = embedding_vector

    return embedding_matrix, num_words

def kill_model():
    try:
        K.clear_session()
        del model
    except:
        print('No model to clear \n')


def create_bidirectional_lstm(maxlen, num_words, number_of_codes, embedding_matrix):
    # Add an Input Layer
    input_layer = layers.Input((maxlen,))

    # Add the word embedding Layer
    embedding_layer = layers.Embedding(num_words, embedding_matrix.shape[1], weights=[embedding_matrix],
                                       trainable=False)(input_layer)
    embedding_layer = layers.SpatialDropout1D(0.1)(embedding_layer)

    # Add a bi-directional layer
    lstm_layer = layers.Bidirectional(layers.LSTM(100, recurrent_dropout=0.1, dropout=0.1))(embedding_layer)

    # Add the output Layers
    # output_layer1 = layers.Dropout(0.25)(lstm_layer)
    output_layer2 = layers.Dense(number_of_codes, activation="softmax")(lstm_layer)

    # Compile the model
    model = models.Model(inputs=input_layer, outputs=output_layer2)
    model.compile(optimizer='Adam', loss='categorical_crossentropy', metrics=['accuracy'])

    model.summary()

    return model


def make_predictions(test_seq_x, test_y, classifier):
    predictions = classifier.predict(test_seq_x)
    prediction = np.argmax(predictions, axis=-1)
    y_true = np.argmax(test_y, axis=-1)
    print('make_predictions-Done! \n')

    return predictions, prediction, y_true


def ensemble_predictions(predictions_p1, predictions_p2, predictions_p3, predictions_p4, predictions_p5, predictions_p6,
                         number_of_test_data_p1, en):
    average_predictions = []
    i = 0

    for i in range(number_of_test_data_p1):
        average_predictions.append((predictions_p1[i] + predictions_p2[i] + predictions_p3[i] + predictions_p4[i] +
                                    predictions_p5[i] + predictions_p6[i]) / en)

    average_predictions_2 = np.array(average_predictions)

    average_prediction = np.argmax(average_predictions, axis=-1)
    print(type(average_predictions_2), type(average_prediction))

    print('ensemble_predictions-Done! \n')

    return average_predictions_2, average_prediction


def calculate_metrics(predictions, prediction, y_true, number_of_test_data):
    # Accuracy
    accuracy_total = metrics.accuracy_score(prediction, y_true) * 100
    print("Accuracy:", accuracy_total)

    # MRR, P@3, P@5, P@10
    all_rr = []
    number_of_top_three = 0
    number_of_top_five = 0
    number_of_top_ten = 0

    predictions_2 = predictions.argsort()
    predictions_3 = np.fliplr(predictions_2)
    for i in range(0, number_of_test_data):
        specific_prediction = predictions_3[i, :]
        list1 = specific_prediction.tolist()
        target = y_true[i]
        prediction_rank = list1.index(target) + 1
        # MRR
        RR = 1 / prediction_rank
        all_rr.append(RR)
        # P@3
        if prediction_rank <= 3:
            number_of_top_three = number_of_top_three + 1
        # P@5
        if prediction_rank <= 5:
            number_of_top_five = number_of_top_five + 1
            # P@10
        if prediction_rank <= 10:
            number_of_top_ten = number_of_top_ten + 1
    MRR = np.mean(all_rr)
    print("MRR:", MRR)
    P3 = number_of_top_three / number_of_test_data * 100
    print("P@3:", P3)
    P5 = number_of_top_five / number_of_test_data * 100
    print("P@5:", P5)
    P10 = number_of_top_ten / number_of_test_data * 100
    print("P@10:", P10)

    return accuracy_total, MRR, P3, P5, P10




def execute_trained_model(arguments):
    words = 60
    epochs = 1
    batch_size = 128
    datasets,language_models, deep_learning = load_config()
    dataset_file = get_element_by_value(datasets, 'name', arguments[0]['datasets'])['file']
    word_vec_file = get_element_by_value(language_models, 'name', arguments[1]['language_models'])['file']
    classifier_file = get_element_by_value(deep_learning, 'name', arguments[2]['deep_learning'])['file']
    DF = load_patents(os.path.join('resources',dataset_file))
    onehot_encoded, onehot_encoder=encode_labels(DF.head(25000))
    number_of_codes=enumarate_codes(onehot_encoded)
    train_x, train_y, valid_x, valid_y, test_x, test_y, number_of_test_data=split_dataset(DF.head(25000), onehot_encoded)
    token, word_index=tokenize_text(DF)
    train_seq_x, valid_seq_x, test_seq_x =convert_text(words, token, train_x, valid_x, test_x)
    embeddings_index = load_fasttext(os.path.join('resources',word_vec_file))
    embedding_matrix, num_words =create_embedding_matrix(embeddings_index, word_index)

    kill_model()
    classifier = create_bidirectional_lstm(words, num_words, number_of_codes, embedding_matrix)
    history=classifier.fit(train_seq_x, train_y, epochs=epochs, batch_size=batch_size, verbose=1)

    predictions, prediction, y_true=make_predictions(test_seq_x, test_y, classifier)
    accuracy_total, MRR, P3, P5, P10 = calculate_metrics(predictions, prediction, y_true, number_of_test_data)