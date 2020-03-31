"""This script contains the data cleaning procedure of fake news dataset"""
import dataset
import text

import pandas as pd
import sys
import time
import tqdm

__author__ = "Akshay Kale"
__copyright__ = "GPL"
__credits__ = "Dilanga Abeyrathna"
__email__ = "akale@unomaha.edu"

def process_english_bs(PATH, SAVEPATH):
    print('Importing..', PATH)
    df = dataset.Dataset(PATH)
    
    # data preprocess and clean
    print('Extracting english records..')
    df.select_english()
    
    print('Extracting text classified as BS..')
    df.select_bs()
     
    print('Reducing dataframe to essential columns...')
    df.clean_columns()

    print('Filtering and adding new columns for Day, Date, and Year..')
    df.add_daydateyear()
    
    print("Processing style attributes..")    
    df.treat_text()

    print("Exporting BS dataset", SAVEPATH)
    df.dataframe.to_csv(SAVEPATH)

def process_english(PATH, SAVEPATH):
    print('Importing..', PATH)
    df = dataset.Dataset(PATH)
    
    # data preprocess and clean
    print('Extracting english records..')
    df.select_english()
    
    print('Reducing dataframe to essential columns...')
    columns = ['published', 'thread_title', 'author', 'text', 'type']
    df.clean_columns(columns)

    print('Filtering and adding new columns for Day, Date, and Year..')
    df.add_daydateyear()

    print("Processing style attributes..") 
    df.treat_text()

    print("Exporting all english dataset", SAVEPATH)
    df.dataframe.to_csv(SAVEPATH)


if __name__=='__main__':
    PATH = '../data/fake.csv'
    SAVEPATH  = '../data/new_csv'
    process_english(PATH, SAVEPATH)

