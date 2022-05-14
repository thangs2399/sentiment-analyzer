
import re
import someFunctions as SF

def tokenizeTrainingSet(someFile):
    """
    
    This function will tokenize the training set. It will takes someFile that includes reviewID, sentiment, and review as argument.
    Data in someFile is assumed well-formatted : reviewID sentiment review 
    And returns a dictionary that includes data needed for to calculate sentiment analysis

    Args:
        someFile (_string_): fileName if file is in same directory, else absolute directory path

    Returns:
        final_dict (_dict_) : 
                    - inside the dict there is three nested dicts : Positive, Negative, Combined
                    - Postive includes data from Positive reviews (or docs)
                    - Negative includes data from Negative reviews (or docs)
                    - Combined includes data from both Negative and Positive reveiws (or docs)
    """
    #################### VARIABLES ####################
    
    final_dict = {} # dict that is returned by the function

    positiveText = "" # words (or text) from positive reviews
    negativeText = "" # words (or text) from negative reviews
    combinedText = "" # words (or text) from both negative/postive reviews
    
    # these empty dictionaries will be used later to store tokenized datas accordingly
    positive = {}
    negative = {}
    combined = {}
    
    # count of negative & positive reviews
    positiveCount = 0
    negativeCount = 0

    #################### HANDLE FILE ####################

    myFile = open(someFile, "r")
    lines_list = myFile.readlines() # a list of reviews
    myFile.close()

    # go over each review
    for line in lines_list:

        # classify the text data using regex
        fileName = re.sub(r"(cv[0-9]{3}_tok-[0-9]{5}\.txt) ([0-1]) (.*)", r"\1", line).strip() # reviewID or name
        sentiment = re.sub(r"(cv[0-9]{3}_tok-[0-9]{5}\.txt) ([0-1]) (.*)", r"\2", line).strip() # sentiment
        review = SF.normalizeText(re.sub(r"(cv[0-9]{3}_tok-[0-9]{5}\.txt) ([0-1]) (.*)", r"\3", line)).strip() # actual review. And it is also normalize the text using normalize() from someFunctions.py

        # remove redundant spaces
        review = review.split()
        review = " ".join(review)

        # concatenate all the reviews accordingly
        # all positive reviews are concatenated together, the same goes for negative reviews
        if (sentiment == "0"):
            
            negativeText += " " + review
            negativeCount += 1 # increment count
        
        elif (sentiment == "1"):

            positiveText += " " + review
            positiveCount += 1 # increment count
    
    # get combine text by concatenating positiveText and negativeText        
    combinedText = positiveText + negativeText
    
    # store tokenized datas
    positive = SF.tokenizeText(positiveText)
    negative = SF.tokenizeText(negativeText)
    combined = SF.tokenizeText(combinedText)

    # store it in final_dict accordingly
    for i in range(3):
        
        a_dict = {}
        
        # handle the data from positive reviews
        if (i == 0):
            
            # add to a_dict
            a_dict["vocabs"] = positive[0] # vocab_dict
            a_dict["vocabsCount"] = positive[1] # vocabsCount
            a_dict["wordsCount"] = positive[2] # wordsCount
            a_dict["docCount"] = positiveCount # count of positive reviews
            
            # add the a_dict using key "P" (positive)
            final_dict["P"] = a_dict
        
        # handle the data from negative reviews
        elif ( i == 1 ):
            
            # add to a_dict
            a_dict["vocabs"] = negative[0] # vocab_dict
            a_dict["vocabsCount"] = negative[1] # vocabsCount
            a_dict["wordsCount"] = negative[2] # wordsCount
            a_dict["docCount"] = negativeCount # count of negative reviews
            
            # add the a_dict using key "N" (negative)
            final_dict["N"] = a_dict
        
        # handle the data from both negative & positive reviews
        elif ( i == 2 ):
            
            # add to a_dict
            a_dict["vocabs"] = combined[0] # vocab_dict
            a_dict["vocabsCount"] = combined[1] # vocabsCount
            a_dict["wordsCount"] = combined[2] # wordsCount
            a_dict["docCount"] = negativeCount + positiveCount # count of total reviews
            
            # add the a_dict using key "C" (combined)
            final_dict["C"] = a_dict
        
            
    return final_dict # type : dict


def tokenizeTestingSet(someFile):
    """
    This function is used to tokenize the testing set. It takes someFile as arg. someFile includes reviewID, sentiment, and review as argument.
    Data in someFile is assumed well-formatted : reviewID sentiment review. ( the same as in training sets )
    Returns a dictionary with data of reviews from this someFile.
    
    Args:
        someFile (type : string): fileName if file is in same directory, else absolute directory path

    Returns:
        final_dict ( type: dict ): 
                        - this dict includes nested dicts with reviewIDs as keys
                        - in these nested dicts includes sentiment (which are blanks because this is testing set)  and review (a list of words)
    """
    
    #################### VARIABLES ####################
    final_dict = {} 

    #################### HANDLE FILE ####################

    myFile = open(someFile, "r")
    lines_list = myFile.readlines() # list of reviews
    myFile.close()


    # go over each review
    for line in lines_list:
    
        # classify the text data using regex
        fileName = re.sub(r"(cv[0-9]{3}_tok-[0-9]{4,5}\.txt) (..) (.*)", r"\1", line).strip() # reviewID or name
        sentiment = re.sub(r"(cv[0-9]{3}_tok-[0-9]{4,5}\.txt) (..) (.*)", r"\2", line).strip() # sentiment of review
        review = SF.normalizeText(re.sub(r"(cv[0-9]{3}_tok-[0-9]{4,5}\.txt) (..) (.*)", r"\3", line)).strip() # actual review and it is also normalize the text using normalize() from someFunctions.py

        # remove redundant spaces
        review = review.split()
        review = " ".join(review)
        
        # a simple dict created to used to store in final_dict
        # this simple dict includes sentiment and review(list of words) 
        a_dict = {}
        a_dict["sentiment"] = sentiment
        a_dict["review"] = review.split() # list of words

        final_dict[fileName] = a_dict # simple dict was stored in final_dict with key "fileName"
    
    return final_dict # dict


def toTest(someFile):
    """
    
    This function is used to test the results of sentiment analysis program (main.py). This function will returns a dictionary with reviewIDs as keys and 
    sentiments as values. someFile is taken as argument. In this someFile, each line has a reviewID and related sentiment. And these data are
    tested and correct. So, the correctness of results from sentiment analysis program (main.py) could be tested by comparing them to data from this
    file.

    Args:
        someFile (type : string): fileName if file is in same directory, else absolute directory path

    Returns:
        final_dict (type: dict) : dictionary with reviewIDs keys and sentiments as values
    """
    #################### VARIABLES ####################
    
    final_dict = {} 

    #################### HANDLE FILE ####################

    myFile = open(someFile, "r")
    lines_list = myFile.readlines()
    myFile.close()
    
    for line in lines_list:
        
        # classify the text data using regex
        fileName = re.sub(r"(cv[0-9]{3}_tok-[0-9]{4,5}\.txt) (.)", r"\1", line).strip()
        sentiment = re.sub(r"(cv[0-9]{3}_tok-[0-9]{4,5}\.txt) (.)", r"\2", line).strip()

        # add data to final_dict
        final_dict[fileName] = sentiment
        
    return final_dict #dict