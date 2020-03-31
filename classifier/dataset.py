"""This script contains the functions to manipulate fake news dataframes"""
import numpy as np
import pandas as pd
import sys
import time

import tqdm
from tqdm import  tqdm

import text


__author__ = "Akshay Kale"
__copyright__ = "GPL"
__credits__ = "Dilanga Abeyrathna"
__email__ = "akale@unomaha.edu"


class Dataset:
    def __init__(self, PATH):
        self.path = PATH
        self.dataframe = pd.read_csv(PATH, low_memory=False)

    def select_english(self):
        self.dataframe = self.dataframe[self.dataframe['language'] == 'english']
        
    def select_fake(self):    
        self.dataframe = self.dataframe[self.dataframe['type'] == 'fake']

    def select_bs(self):
        self.dataframe = self.dataframe[self.dataframe['type'] == 'bs']

    def clean_columns(self, columns):
        columns = ['published',
                    'thread_title',
                    'author',
                    'participants_count',
                    'comments',
                    'shares',
                    'text'
                ]
        self.dataframe = self.dataframe[columns]
        self.dataframe.dropna(subset=['published','thread_title', 'text'], inplace=True)


    def add_daydateyear(self):
        date =  self.dataframe['published']
        series_date = [timestamp[:10] for timestamp in tqdm(date, desc='adding date')]
        series_year = [timestamp[:4] for timestamp in tqdm(date, desc='adding year' )]
        series_month = [timestamp[5:7] for timestamp in tqdm(date, desc= 'adding month')]
        series_day = [timestamp[8:10] for timestamp in tqdm(date, desc='adding day')]
       
        self.dataframe['year'] = pd.Series(series_year)
        self.dataframe['month'] = pd.Series(series_month)
        self.dataframe['date'] = pd.Series(series_date)
        self.dataframe['day'] = pd.Series(series_day)

    def treat_text(self):
        entities = []
        elongations = []
        hedge_words = []
        processed_words = []
        text_topics = []
        for each_text in tqdm(self.dataframe['text'], desc='Processing text'):
            txt = text.Text(each_text)
            entities.append(txt.get_entities())
            elongations.append(txt.get_elongated_words())
            hedge_words.append(txt.get_hedge_words())
            txt.create_sentences()
            list_of_words, words, corpus  = txt.remove_stopwords_and_lemmatize()
            try:
                text_topics.append(txt.get_topics())
            except:
                #TODO: set up a logging system
                continue

        self.dataframe['entities'] = entities 
        self.dataframe['hedge words'] = hedge_words
        self.dataframe['lemmatized words'] = list_of_words 
        self.dataframe['Topics'] = text_topics

