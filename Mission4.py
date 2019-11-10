import glob2
import PyPDF2
import random
from nltk.util import ngrams
import pronouncing
import os

"""
Different Centuries meet
By Lyndbergh Simelus
November 5th, 2019
"""

class Poem:
    
    def __init__(self):
        """
        Constructor for Poem Class
        
        @returns None
        @params None
        """
        self.body = ""
        self.Lastwords = []
    
        """
        Adds a string to the body of the poem
        
        @returns None
        @params The string that is being added to the poem body
        """        
    def add(self, add_on):
        self.body = self.body + add_on + " "
        
        """
        Add The last word of each sentences or to the list
        So, it can later be called later when trying to rhyme
        
        @returns None
        @params New word at the end of sentence 
        """        
    def new_end(self, end):
        self.Lastwords.append(end)
        
        """
        gets list of last words
        
        @returns List of all of the last words in the sentences
        @params None
        """        
    def get_ends(self):
        return self.Lastwords
    
        """
        Getter function for the poem body
        
        @returns string of body
        @params None
        """
    def result(self):
        return self.body
    
        """
        Evaluation of poem
        
        @returns The number of words that rhyme
        @params None
        """        
    def score(self):
        return len(self.Lastwords)
    
        """
        Gets rid of the author signature so it can be signed
        
        @returns None
        @params None
        """
    def sign(self):
        bodyinlist = self.body.split()
        bodyinlist.pop()
        self.body = ' '.join(bodyinlist)
    
        """
        Print representation of the poem class
        Signs it as well
    
        @returns None
        @params None
        """    
    def __repr__(self):
        raw = self.body.split()
        i = 0
        for words in raw:
            if i%15 == 0:
                raw.insert(i, "\n")
            i = i + 1
        raw.append("\n Different Centuries meet System\n")
        return ' '.join(raw)
    
class Database:
    
    def __init__(self):
        """
        Constructor for database class
        
        @returns None
        @params None
        """
        self.Frequency = {}
        self.authorFirst = []
    
    
    def readFileAsString(self, author_name = None):
        """
        Reads all of the files in Poems and adds the poems to the self.Frequency
        The writing style of poets is very different so it is suggested that an author is picked
        
        @returns None
        @params None
        """      
        if author_name != None:
            author_name = author_name.lower()
            
        for file in glob2.glob("Poems/*"):
            print(file)
            pdfFileObj = open(file, 'rb') 
            pdfReader = PyPDF2.PdfFileReader(pdfFileObj)
            PAGE_STARTS = 2 
            i = PAGE_STARTS
            
            author_poems = []
            name = file.split("_")
            first = (name[0])[6:]
            title = first + name[1]
            title = title #gets the last author that writes the last letter in the poem
            
            self.authorFirst.append(title)
            
            if author_name == None or author_name == title: #if we want a specific author it gets a specific author
                while( i < pdfReader.numPages):
                    pageObj = pdfReader.getPage(i) 
                    one_poem = pageObj.extractText()
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
                        self.Add(' '.join(gr))
                        
                    i += 1

        if author_name in self.authorFirst or author_name == None:
            next
        else:
            print(self.authorFirst)   
            raise( Exception(author_name + " is not a valid author. Choose one of the following and type it how you see it"))
                        

    def Add(self, words):
        """
        Adds an n-gram to the list of Frequency
        
        @returns None
        @params n-gram which is a word
        """        
        curr = 1
        if words in self.Frequency.keys():
            curr = self.Frequency[words]
            self.Frequency[words] = curr + 1
        else:
            self.Frequency[words] = curr 

    def rhyme(self, prevend, gram):
        last = gram.split()[2]
        punct = last[-1]
        last = last[:-1]
        
        #This runs for the first ending of a sentence
        if len(prevend.get_ends()) == 0:
            prevend.new_end(last)
            return last + punct
        
        #set of all possible combinations that rhyme with with the list of las words
        matches = []
        for words in prevend.get_ends():
            matches = matches + pronouncing.rhymes(words)
        allpos = set(matches)
        
        #Get a set of all possible words that match with every possible end that comes could come next in the n gram
        #so selecting a random item from the selector would make the poem act like normal
        selectpos = set(self.generate_selector(gram.split()[0], gram.split()[1]))
        selectposendingsList = []
        for items in selectpos:
            selectposendingsList.append(items.split()[-1])
        selectposending = set(selectposendingsList)
        
        #Get a set of words that rhyme with the end of sentences and comes next in the n-gram
        matches = selectposending.intersection(allpos)
        
        # if true then there is no matches and we print the original word next in the n-gram
        if len(matches) == 0 :
            prevend.new_end(last)
            return last + punct
        else:#else we exchange words
            replacement = random.choice(list(matches))
            prevend.new_end(replacement)
            return replacement + punct
        
        """
        Uses the Frequency table to write a poem
        
        @returns String of poem created
        @params An optional parameter of the authors name
        """        
    def write(self):
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
                print("There were no more possibilities the poem ended early");
                return body
            
            adding = new_word.split()[2]
            
            if adding[-1] in endings: # if it is an end then ..
                adding = self.rhyme(body, new_word)
                
            first = second
            second = adding
            body.add(adding)
            
            if (new_word.split()[-1] in self.authorFirst): #if an author name is seen then it is the end of the poem
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
            for word in self.Frequency:
                occur = self.Frequency[word]
                i = 0
                while (i < occur):
                    
                    selector.append(word)
                    i = i + 1
        elif second == None:
            #frequency withthe first word in n-gram determined
            #ran once
            for word in self.Frequency:
                
                if first == word.split()[0]:
                    occur = self.Frequency[word]
                    i = 0
                    
                    while (i < occur):
                        selector.append(word)
                        i = i + 1   
        else:#n-gram with the first two words set
            for word in self.Frequency:
                if first == word.split()[0] and second == word.split()[1]:
                    occur = self.Frequency[word]
                    i = 0
                    while (i < occur):
                        selector.append(word)
                        i = i + 1
        return selector
    

        
def main():
    test = Database()
    #test.readFileAsString("oscarwilde")
    #above will only read poems from the oscarwilder
    test.readFileAsString() 
    
    List_of_poems = []
    number_of_poems = 2
    
    i = 0
    while(i < number_of_poems ):
        List_of_poems.append(test.write())
        i += 1
        
    #Finding the method with the highest score is my method for evaluation 
    best_poem = List_of_poems[0]
    for items in List_of_poems:
        if items.score() > best_poem.score():
            best_poem = items
            
    print(best_poem)
    os.system('say ' + best_poem.result())

main()