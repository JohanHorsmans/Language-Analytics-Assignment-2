#!/usr/bin/python

import os
import re
from collections import Counter
import pandas as pd
from pathlib import Path
import math
import sys

def collocation(filepath, keyword, window_size): #Define a function with three parameters, "filepath", "keyword" & "window_size".
    #Defining empty list for appending objects:
    u = []
    collocates = []
    collocate_word = []
    O11 = []
    O12 = []
    all_words = []
    
    for text in Path(filepath).glob("*.txt"): #Loop through all .txt-files in the filepath.
        with open(text, "r", encoding="utf-8") as text: #Opening the contents of the .txt-file.
            loaded_text = text.read() #Loading the contents of the .txt-file.
            loaded_text = loaded_text.lower() #Using the lower-method to make all letters in the text lowercase to ensure that identical words with different casing are regarded as the same word.
            regex = re.compile('[^a-zA-Z\s]') #Use regular expression to define special characters which I want to delete. \s is whitespace, a-zA-Z - matches all the letters, ^ - negates them all so it deletes everything else. This is done to ensure that, i.e., "fish." and "fish!" are recognized as identical words.
            loaded_text = regex.sub('', loaded_text) #Remove word defined in the above regular expression.
        t = -1 #Defining t as -1
        loaded_text = loaded_text.split() #Split text into individual words.
        all_words.append(loaded_text) #Append the text to a list that will be composed of all words in the texts.
        while True: #While true (i.e. as long as possible)...
            try: #... do the following
                t = loaded_text.index(keyword, t + 1) #Try to find keyword at t + 1 (where t increases by 1 iteratively).
                keyword = loaded_text[t] #Save keyword to variable called "keyword".
                lower_window = loaded_text[t-window_size:t] #Define lower window.
                upper_window = loaded_text[t+1:t+window_size+1] #Define upper window.
                u.append(loaded_text[t]) #Append the keyword to the "u"-list.
                collocates.extend(lower_window + upper_window) #Add the words from the lower- and upper window to the "collocates-list".
            except ValueError: 
                break
    
    #Flatten the "all_words"-list to a single line with no breaks:
    all_words_flat = [] 
    for sublist in all_words:
        for item in sublist:
            all_words_flat.append(item)

    #Calculate O11:
    collocates = (" ".join(collocates)) #Transform "callocates"-lists into a single string. 
    collocates = collocates.split() #Split callocates-string into individual words.
    collocate_count = Counter(collocates).most_common(len(collocates)) #Count unique words and their apperance. The reason for using the most_common specifications is that it gives a tuple as an output, which can be indexed. 
        
    for i in list(range(0,len(collocate_count))): #For each element in the collocate...
        collocate_word.append(collocate_count[i][0]) #... Append the word to the "collocate_word"-list.
        O11.append(collocate_count[i][1]) #... Append the count of the word to the "O11"-list.


    
    #Calculate O12:
    for word in collocate_word: #For each word in the callocates...
        O12.append(all_words_flat.count(word)) #... append how often the word appears in the entire corpus to the "O12"-list.
    
    for i in list(range(0, len(collocate_word))): #For the amount of words in "collocate_words"...
        O12[i] = max(0,O12[i]-O11[i]) #...iterate through the O12 list and replace the values with O11 subtracted from O12.
        
    #Calculate R1:

    R1 = list(range(0, len(collocate_word))) #Make a list called "R1" with integers ranging from zero to the number of collocates.

    for i in R1: #For each element in the "R1"-list.
        R1[i] = O12[i]+O11[i] #...Replace R1-value with O12 + O11 (iteratively).

    #Calculate O21:

    O21 = list(range(0, len(collocate_word))) #Make a list called "O21" with integers ranging from zero to the number of collocates.
        
    for i in O21: #For each element in the "O21"-list.
        O21[i] = len(u) - O11[i] #...Replace O21-value with O11 (iteratively) subtracted from the amount keywords in total.

    #Calculate C1:
    C1 = list(range(0, len(collocate_word))) #Make a list called "C1" with integers ranging from zero to the number of collocates.
    
    for i in C1: #For each element in the "C1"-list.
        C1[i] = O11[i] + O21[i] #...Replace C1-value with O11 + O21 (iteratively).

    #Calculate N:
    N = len(all_words_flat) #Calculate the total amount of words.

    
    #Calculate E11:
    
    E11 = list(range(0, len(collocate_word))) #Make a list called "C1" with integers ranging from zero to the number of collocates.
    
    for i in E11: #For each element in the "C1"-list.
        E11[i] = (R1[i]*C1[i])/N #...Replace C1-value with (R1*C1)/N (iteratively).

    #Calculate MI:
    MI = list(range(0, len(collocate_word))) #Make a list called "MI" with integers ranging from zero to the number of collocates.
    
    for i in MI: #For each element in the "C1"-list.
        MI[i] = math.log((O11[i]/E11[i])) #... Calculate the MI-score.
        

#Writing .CSV-file;
    

    dict = {'collocate': collocate_word, 'raw_frequency': R1, 'MI': MI} #Create a dictionary with the column-names and values for the .CSV-file
    df = pd.DataFrame(dict) #Creating a pandas-dataframe using the above dictionary.
    df.to_csv(f'{keyword} - window_size_{window_size}.csv') #Write the dataframe as a .csv-file called {keyword} - window_size_{window_size}.csv'.

#If the script is called from the commandline make filepath the first argument, keyword the second argument and window_size the third argument:
if __name__=="__main__":
    collocation(filepath = sys.argv[1], keyword = sys.argv[2], window_size = int(sys.argv[3]))

    