import glob2
import PyPDF2
import random
from nltk.util import ngrams
import pronouncing
import os
from DB import Database


"""
Different Centuries meet
By Lyndbergh Simelus
November 5th, 2019
"""



def main():
    test = Database()
    #above will only read poems from the oscarwilder
    test.read_file_as_string() 

    list_of_poems = []
    number_of_poems = 2
    
    i = 0
    while(i < number_of_poems ):
        list_of_poems.append(test.write())
        i += 1
    #Finding the method with the highest score is my method for evaluation 
    best_poem = list_of_poems[0]
    for items in list_of_poems:
        if items.score() > best_poem.score():
            best_poem = items
            
    print(best_poem)
    os.system('say ' + best_poem.result())
main()
