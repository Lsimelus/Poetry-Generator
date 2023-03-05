import glob2
import PyPDF3
import random
from nltk.util import ngrams
import pronouncing
import os

class Poem:


    def __init__(self):
        """
        Constructor for Poem Class
        
        @returns None
        @params None
        """
        self.body = ""
        self.last_words = []
        self.rhyming_words = []

    def add(self, add_on):
        """
        Adds a string to the body of the poem
        
        @returns None
        @params The string that is being added to the poem body
        """        
    
        self.body = self.body + add_on + " "

    def new_end(self, end):
        """
        Add The last word of each sentences or to the list
        So, it can later be called later when trying to rhyme
        
        @returns None
        @params New word at the end of sentence 
        """          
        self.last_words.append(end)

    def get_ends(self):
        """
        gets list of last words
        
        @returns List of all of the last words in the sentences
        @params None
        """          
        return self.last_words
    
    def get_matches(self):
        """
        gets words that rhyme List
        
        @returns List of all of the last words in the sentences that rhyme with another ending
        @params None
        """
        return self.rhyming_words
    
    def new_match(self, new_word):
        """
        Add the s word to the list of rhyming words
        
        @returns None
        @params New word that rhymes
        """            
        self.rhyming_words.append(new_word)
    
    def result(self):
        """
        Getter function for the poem body
        
        @returns string of body
        @params None
        """        
        return self.body

    def score(self):
        """
        Evaluation of poem
        
        @returns The number of words that rhyme
        @params None
        """           
        return len(self.rhyming_words)

    def sign(self):
        """
        Gets rid of the author signature so it can be signed
        
        @returns None
        @params None
        """        
        body_in_list = self.body.split()
        body_in_list.pop()
        self.body = ' '.join(body_in_list)

    def __repr__(self):
        """
        Print representation of the poem class
        Signs it as well
    
        @returns None
        @params None
        """        
        raw = self.body.split()
        i = 0
        for words in raw:
            if i%15 == 0:
                raw.insert(i, "\n")
            i = i + 1
        raw.append("\n Different Centuries meet System\n")
        return ' '.join(raw)

