import re

# remove non-word characters from the text (example: like a punctuation)
def normalizeText(someText):
    """
        This function will normalize the text by removing non-word char from the text.

        Args: someText (type: string)

        Returns: normalizedText (type: string) 
    """
    normalizedText = ""

    words_list = someText.split() # make a list of words by splitting the text

    for word in words_list:

        word = normalizeWord(word) # uses nomalizeWord() to remove nonword char of the word

        if (not normalizedText): # if it is empty

            normalizedText += word
        else:

            normalizedText += " " + word
    
    return normalizedText # ( type : string )


# remove non-word from a word like punctuations
def normalizeWord(someWord):
    """
        This function will remove non-word characters from a word.
        
        Args: someWord ( type: string )
        
        Returns: removedText ( type : string ) : the word without any non-word char
    """
    normalizedWord = ""
    modifiedList = ["_"] # non-word chars
    
    nonWordRE = re.compile(r"\W") # remove non-word using regex object
    nonSpaceRE = re.compile(r"[^ ]") # remove non-word using regex object
    
    nonWordsWspaces = nonWordRE.findall(someWord) # extract all non-word characters
    nonWordsWOspaces = nonSpaceRE.findall(" ".join(nonWordsWspaces)) # remove spaces
    
    # filter duplicates
    for i in nonWordsWOspaces:
        
        if i not in modifiedList:
            
            modifiedList.append(i)


    for char in someWord:

        # if char is not a non-word
        if char not in modifiedList:

            # if the char is uppercase, convert it to lowercase
            if (char.isupper()):
                
                char = char.lower()
            
            # concatenate the char
            normalizedWord += char
    
    return normalizedWord # return the string


def tokenizeText(someText):
    """
        This function will tokenize words given a text. And returns three values : a dictionary of vocabs words, vocabsCount and allWordsCount . 
        
        Args: someText ( type: string )
        
        Returns: vocabs_dict ( type: dict ) : a dict with unique words as keys and counts as values,
                 vocabsCount ( type: int ) : count of all unique words
                 allWordsCount ( type: int ) : count of all words (including duplicates)
    """
    
    #################### VARIABLES ####################
    
    vocabs_dict = {} # dict with vocabs as keys and counts as values
    vocabsCount = 0 # count of all unique words
    allWords_list = someText.split() # list of all words including duplicates
    allWordsCount = len(allWords_list) # count of all words including duplicates

    # go over all the words
    for word in allWords_list:
        
        # if the word is not in vocabs_dict
        # add it to the vocabs_dict
        # increment vocabsCount by 1
        if ( word not in vocabs_dict.keys() ):
            
            vocabs_dict[word] = 1
            vocabsCount +=1 # increment vocab count
        
        # if the word is already in vocabs_dict
        # just increment the value of associated key
        elif ( word in vocabs_dict.keys() ):
            
            vocabs_dict[word] += 1
            
    return vocabs_dict, vocabsCount, allWordsCount # tuple
