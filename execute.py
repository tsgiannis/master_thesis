# Import libraries
import os.path

import tensorflow
from tensorflow import keras
from keras import layers, models, optimizers
from keras.layers import LSTM, GRU, Bidirectional
from keras.optimizers import SGD, RMSprop, Adadelta, Adam
from keras.preprocessing import text, sequence
from keras.callbacks import ReduceLROnPlateau, ModelCheckpoint, LearningRateScheduler
import numpy as np
import pandas as pd
import io
from statistics import mean, stdev, median
from sklearn import model_selection, preprocessing, linear_model, naive_bayes, metrics, svm
from sklearn.model_selection import train_test_split, StratifiedKFold
from sklearn.utils import shuffle
from collections import Counter
import math
import matplotlib.pyplot as plt
import csv
import pickle

import pickle
import os
from apps.utilities import *


def execute(arguments):
# Load the model

    method = get_value_out_of_list_of_dicts(arguments, 'methods')
    languagemodel= get_value_out_of_list_of_dicts(arguments, 'languagemodels')
    dataset=get_value_out_of_list_of_dicts(arguments,'datasets')
    patentsection = get_value_out_of_list_of_dicts(arguments, 'sections')
    ipclevel = get_value_out_of_list_of_dicts(arguments, 'ipclevels')
    noofwords = get_value_out_of_list_of_dicts(arguments, 'noofwords')
    singlemulti = get_value_out_of_list_of_dicts(arguments, 'singlemulti')
    structure = get_value_out_of_list_of_dicts(arguments, 'structure')
    ensemble = get_value_out_of_list_of_dicts(arguments, 'ensemble')
    resultstodisplay = get_value_out_of_list_of_dicts(arguments, 'results')





    methods,languagemodels,datasets,ipclevels,noofwords,singlemulti,structures,ensemble = load_config()
    encoder_file = get_element_by_value(datasets, 'name', arguments[0]['datasets'])['object']
    word_vec_file = get_element_by_value(languagemodels, 'name', arguments[1]['language_models'])['object']
    classifier_file = get_element_by_value(methods, 'name', arguments[2]['deep_learning'])['object']
    classifier_file = os.path.join('resources',classifier_file)
    example_classifier = models.load_model(classifier_file, compile=False)

    # Load the tokenizer
    word_vec_file = os.path.join('resources',word_vec_file)
    with open(word_vec_file, 'rb') as handle:
        token = pickle.load(handle)

    # Load the encoder


    encoder_file = os.path.join('resources',encoder_file)
    with open(encoder_file, 'rb') as f:
        encoder = pickle.load(f)

    # Get the input text from the keyboard

    text_list = []
    text_keywords = get_value_out_of_list_of_dicts(arguments, 'keywords')
    #text_keywords = str(input("Please enter some keywords:\n"))
    text_list.append((text_keywords))

    # Create an input dataframe

    inputDF = pd.DataFrame()
    inputDF['text'] = text_list

    # Convert text to sequence of tokens
    # maxlen is 60 words since the classifier has been trained to get as input text of 60 words

    maxlen = 60
    input_seq_x = sequence.pad_sequences(token.texts_to_sequences(inputDF['text']), maxlen)

    # Use the classifier to make the prediction
    predictions = example_classifier.predict(input_seq_x)

    sorted_categories = np.argsort(predictions)
    sorted_categories = np.fliplr(sorted_categories)

    print("the predicted codes (sorted) in numbers",  )

    # Convert the predictions into codes
    # number_of_codes is 731 codes since the initial dataset has 731 different codes

    number_of_codes = 731
    pred_class = []

    for row in range(len(text_list)):
        list_class = []
        for i in range(number_of_codes):
            class_number = sorted_categories[row, i]
            class_number_zeros = np.zeros(number_of_codes)
            class_number_zeros[class_number] = 1
            class_number_zeros = class_number_zeros[np.newaxis, :]
            #class_label = encoder.inverse_transform(class_number_zeros)

            class_label = encoder.categories_[0][np.nonzero(class_number_zeros)[1][0]]
            list_class.append(class_label)
        pred_class.append(list_class)

    #outputDF = pd.DataFrame()

    outputDF=pd.DataFrame(pred_class).T
    outputDF.columns = text_list
    #print("the predicted codes (sorted) in labels", outputDF)
    return outputDF
