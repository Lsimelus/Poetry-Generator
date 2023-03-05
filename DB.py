import glob2
import PyPDF3
import random
from nltk.util import ngrams
import pronouncing
import os
from Poems import Poem


class Database:
    
    
    def __init__(self):
        """
        Constructor for database class
        
        @returns None
        @params None
        """
        self.frequency = {}
        self.author_first = []

    def read_file_as_string(self, author_name = None):
        """
        Reads all of the files in Poems and adds the poems to the self.Frequency
        The writing style of poets is very different so it is suggested that an author is picked
        
        @returns None
        @params None
        """      
        if author_name != None:
            author_name = author_name.lower()
            
        for file in glob2.glob("Poems/*"):
            pdf_file_obj = open(file, 'rb') 
            pdf_reader = PyPDF3.PdfFileReader(pdf_file_obj)
            page_starts = 2 
            i = page_starts 
            
            author_poems = []
            name = file.split("_")
            first = (name[0])[6:]
            title = first + name[1]
            title = title #gets the last author that writes the last letter in the poem
            
            self.author_first.append(title)
            
            if author_name == None or author_name == title: #if we want a specific author it gets a specific author
                while( i < pdf_reader.numPages):
                    page_obj = pdf_reader.getPage(i) 
                    one_poem = page_obj.extractText()
                    s = one_poem.lower()
                    #Some of the punctuation combines words
                    #We fix the pdfreadersmistakes
                    s = s.replace(".", ". ")
                    s = s.replace(",", "")
                    s = s.replace(";", "; ")
                    s = s.replace("?", "? ")
                    s = s.replace("!", "! ")
                    s = s.replace('"', " ")
                    s = s.replace("&", " and ")
                    s = s.replace(":", ": ")
                    s = s.replace(")", "")
                    s = s.replace("(", "")
                    poem_list = s.split()
                    
                    j = len(poem_list)
                    while(j > -1):
                        j = j - 1
                        if first == poem_list[j]:
                            break
                        if 1 == j:
                            #If it gets to this point then there is no author name
                            #That is because it is not a poem
                            #or the poem is more than one page long
                            break
                        poem_list.pop()
                            
                    #if we get here then it is a valid poem
                    poem_list.pop()
                    # we get rid of the authors name and sign it with title
                    poem_list.append(title)
                    
                    gram = ngrams(poem_list, 3)
                    for gr in gram:
                        self.add(' '.join(gr))
                        
                    i += 1

        if author_name in self.author_first or author_name == None:
            next
        else:
            print(self.author_first)   
            raise( Exception(author_name + " is not a valid author. Choose one of the following and type it how you see it"))
                        
    def add(self, words):
        """
        Adds an n-gram to the list of Frequency
        
        @returns None
        @params n-gram which is a word
        """        
        curr = 1
        if words in self.frequency.keys():
            curr = self.frequency[words]
            self.frequency[words] = curr + 1
        else:
            self.frequency[words] = curr 

    def rhyme(self, poem, gram):
        """
        Recieves the most recent n-gram and the poem class. 
        Checks to see if the ending could rhyme with a previous ending
        While only using words that are in the n -gram 
        
        @returns String, The value that is (not) replacing the last sentence of the word, the value should also rhyme with previous sentences
        @params Instance of an unfinished poem class, The n- gram that includes the end of the sentence
        """
        last = gram.split()[2]
        punct = last[-1]
        last = last[:-1]
        
        #This runs for the first ending of a sentence
        if len(poem.get_ends()) == 0:
            poem.new_end(last)
            return last + punct
        
        #set of all possible combinations that rhyme with with the list of las words
        matches = []
        for words in poem.get_ends():
            matches = matches + pronouncing.rhymes(words)
        all_pos = set(matches)
        
        #Get a set of all possible words that match with every possible end that comes could come next in the n gram
        #so selecting a random item from the selector would make the poem act like normal
        select_pos = set(self.generate_selector(gram.split()[0], gram.split()[1]))
        select_pos_endings_list = []
        for items in select_pos:
            select_pos_endings_list.append(items.split()[-1])
        select_pos_ending = set(select_pos_endings_list)
        
        #Get a set of words that rhyme with the end of sentences and comes next in the n-gram
        matches = select_pos_ending.intersection(all_pos)
        # if true then there is no matches and we print the original word next in the n-gram
        if len(matches) == 0 :
            poem.new_end(last)
            return last + punct
        else:#else we exchange words
            replacement = random.choice(list(matches))
            poem.new_end(replacement)
            poem.new_match(replacement)
            return replacement + punct
              
    def write(self):
        """
        Uses the Frequency table to write a poem
        
        @returns String of poem created
        @params An optional parameter of the authors name
        """          
        selector = []
        new_word = ""
        body = Poem()
        
        selector = self.generate_selector()# gets frequency of all words
        first = random.choice(selector).split()[0] #gets frequency of tri-grams with the first word
        selector = self.generate_selector(first)
        second = random.choice(selector).split()[1] #gets frequency of tri-grams with first and seond word
        endings = [ ".", "?" , "!" , ";", ":"]
        
        while(True):
            try:
                new_word = random.choice(self.generate_selector(first, second))#new word picked
            except:
                #print("There were no more possibilities the poem ended early");
                return body
            
            adding = new_word.split()[2]
            
            if adding[-1] in endings: # if it is an end then ..
                adding = self.rhyme(body, new_word)
                
            first = second
            second = adding
            body.add(adding)
            
            if (new_word.split()[-1] in self.author_first): #if an author name is seen then it is the end of the poem
                body.sign()
                return body


    def generate_selector(self, first = None, second = None):
        """
        Creates a list of all of the possible n-grams that match the words pasesed in
        
        @returns List of of possible combinations with the frequency of them taken into consideration
        @params The first and Second words is optional, If there is no word then the range of possible n- grams will be greater, making the selector list greater
        """   
        
        selector = [] 
        if (first == None and second == None):#if we are looking for the fequency of words
            #ran once for each poem
            for word in self.frequency:
                occur = self.frequency[word]
                i = 0
                while (i < occur):
                    
                    selector.append(word)
                    i = i + 1
        elif second == None:
            #frequency withthe first word in n-gram determined
            #ran once
            for word in self.frequency:
                
                if first == word.split()[0]:
                    occur = self.frequency[word]
                    i = 0
                    
                    while (i < occur):
                        selector.append(word)
                        i = i + 1   
        else:#n-gram with the first two words set
            for word in self.frequency:
                if first == word.split()[0] and second == word.split()[1]:
                    occur = self.frequency[word]
                    i = 0
                    while (i < occur):
                        selector.append(word)
                        i = i + 1
        return selector
    

        