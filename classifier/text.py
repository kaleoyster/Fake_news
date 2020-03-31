"""
The  script will contain mainly Contains functions that extract style-based features from text
    1. Hedging 
    2. Elongation 
    3. Named entities 
    4. Contextuality (LDA)
    5. Abstract words 
"""
from collections import defaultdict
from nltk import ne_chunk, word_tokenize
from nltk.corpus import stopwords 
import nltk
import re
import numpy as np
import pandas as pd
import tqdm
from tqdm import tqdm

import maps

import gensim
import gensim.corpora as corpora
from gensim.utils import simple_preprocess
from gensim.models import CoherenceModel

import spacy
from spacy.lemmatizer import Lemmatizer
from spacy.lang.en.stop_words import STOP_WORDS
from spacy.lang.en import English

import en_core_web_lg


__author__ = "Akshay Kale"
__copyright__ = "GPL"
__credit__ = "Dilanga Abeyrathna"
__email__ = "akale@unomaha.edu"


class Text:
    def __init__(self, text):
        self.text = text
        self.hedgewords = {}
        self.topics = []
        self.elongations = [] 
        self.entities = []
        self.abstract_words = []
        self.processed_text = []
        self.words =  []
        self.corpus = []
        self.nlp = spacy.load("en")
        self.sentences = []
        
    def __repr__(self):
        return text[0]

    def __str__(self):
        pass

    def create_sentences(self):
        nlp = English()
        nlp.add_pipe(nlp.create_pipe('sentencizer'))
        doc = nlp(self.text)
        self.sentences = [sent.string.strip() for sent in doc.sents]
        
    def get_hedge_words(self):
        hedgewords = maps.hedge_weasel_words
        hedge_locator = defaultdict() 
        
        for word in self.text:
            if word in hedgewords:
                location = self.text.index(word)
                hedge_locator[word].append(location)
        
        self.hedge_words = hedge_locator
        return self.hedge_words
   
    def get_elongated_words(self):
        elongated_word_regex = re.compile(r"(.)\1{2}")
        words = self.text.split() 
        list_elongated_words = []
        for word in words:
            if elongated_word_regex.search(word):
                list_elongated_words.append(word)

        self.elongations = list_elongated_words
        return list_elongated_words

    def get_entities(self):
        token = word_tokenize(self.text)
        tags = nltk.pos_tag(token)
        list_entities = ne_chunk(tags)

        return list_entities

     
    def lemmatizer(self, doc):
        doc = [token.lemma_ for token in doc if token.lemma_ != '-PRON-']
        doc = u' '.join(doc)
        return self.nlp.make_doc(doc)
        
    def remove_stopwords(self, doc):
        doc = [token.text for token in doc if token.is_stop != True and token.is_punct != True ]
        return doc


    def remove_stopwords_and_lemmatize(self):
        stop_list = maps.stop_words
        self.nlp.Defaults.stop_words.update(stop_list)

        for word in STOP_WORDS:
            lexeme = self.nlp.vocab[word]
            lexeme.is_stop = True
 
        self.nlp.add_pipe(self.lemmatizer, name='lemmatizer', after='ner')
        self.nlp.add_pipe(self.remove_stopwords, name="stopwords", last=True)
        
        list_of_processed_text = []
        for sentence in self.sentences:
            processed_text = self.nlp(sentence)
            list_of_processed_text.append(processed_text)
        
        
        self.words = corpora.Dictionary(list_of_processed_text)
        self.corpus = [self.words.doc2bow(sentence) for sentence in list_of_processed_text]
       
        return list_of_processed_text, self.words, self.corpus 
    
    def get_topics(self):
        lda_model = gensim.models.ldamodel.LdaModel(corpus=self.corpus,
                                                    num_topics=10,
                                                    id2word=self.words,
                                                    random_state=2,
                                                    update_every=1,
                                                    passes=10,
                                                    alpha='auto',
                                                    per_word_topics=True
                                                    )

        return lda_model.print_topics(num_words=10)
