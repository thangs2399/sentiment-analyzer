
############################################################ IMPORTS ############################################################

# import math
import math

# local modules
import tokenization as TK
import someFunctions as SF

############################################################ MAIN PROGRAM ############################################################

trainingSet = TK.tokenizeTrainingSet("./data/sentiment-train.txt")
testingSet = TK.tokenizeTestingSet("./data/sentiment-test.txt")


# a dictionary to keep track of probabilities of each of the files
prob = {}

# Priors
positivePrior = math.log(trainingSet["P"]["docCount"]/trainingSet["C"]["docCount"])
negativePrior = math.log(trainingSet["N"]["docCount"]/trainingSet["C"]["docCount"])

# these are used in calculating the probabilites
totalWords_P = trainingSet["P"]["wordsCount"] # count of total words in postive documents
totalWords_N = trainingSet["N"]["wordsCount"] # count of total words in negative documents
totalVocabs_C = trainingSet["C"]["vocabsCount"] # count of total vocabs in both negative and positive documents

# iterate over all the reviews one by one
for reviewName in testingSet.keys():
    
    # negative & positive probabilites variables
    posititveProbability = positivePrior
    negativeProbability = negativePrior
    
    ##### CALCULATE PROBABILITY #####
    
    # iterate over each word from current review
    for word in testingSet[reviewName]["review"]:
        
        # if the word is in the vocabs (combined)
        if word in trainingSet["C"]["vocabs"]:
            
            #################### POSITIVE  ####################
            
            # if word is in the vocabs of postitive docs
            if (word in trainingSet["P"]["vocabs"]):
            
                wordFreq = trainingSet["P"]["vocabs"][word] # wordFreq set to count of the word in negative docs
            # if not
            else:
                
                wordFreq = 0 # wordFreq is set to zero
                        
            positiveLikeliHood = math.log( (wordFreq + 1) / (totalWords_P + totalVocabs_C)) # calculate positive likelihood
            posititveProbability += positiveLikeliHood # add positive likelihood to the positiveProbability
            
            #################### NEGATIVE  ####################
            
            # if word is in the vocabs of negative docs
            if (word in trainingSet["N"]["vocabs"]):
                
                wordFreq = trainingSet["N"]["vocabs"][word] # wordFreq set to count of the word in negative docs
            else:
                
                wordFreq = 0 # wordFreq is set to zero
            
            negativeLikelihood = math.log( (wordFreq + 1) / (totalWords_N + totalVocabs_C)) # calculate negative likelihood
            negativeProbability += negativeLikelihood # add negative likelihood to the negative Probability

    # classify the sentiment based on the proabilities
    # if a review's positiveProbability is greater than its negativeProbabilites then it is assumed as positive review
    # otherwise it is negative review
    if (posititveProbability > negativeProbability):
        
        testingSet[reviewName]["sentiment"] = 1 # 1 is positive  
        
    else:
        
        testingSet[reviewName]["sentiment"] = 0 # 0 is negative
    
    
    # add to prob dictionary
    a_dict = {}
    a_dict["P"] = posititveProbability
    a_dict["N"] = negativeProbability
    
    prob[reviewName] = a_dict
        
        
############################################################ TESTING & OUTPUT ############################################################

# prompt user for output file name
outputFileName = input("Enter name of the output text file: ")

# sanitize the outputfilename
outputFileName = outputFileName.strip() + ".txt"

# open the textfile
outputFile = open(outputFileName, "w")

# a dictionary - reviewName : sentiment
correctTest = TK.toTest("./data/sentiment-gold.txt") # from gold text

errorCount = 0 # error count
count = 1 # line count for each line from the doc


# CONFUSION MATRIX
# tp = true positive, fp = false positive, fn = false nagtive and tn = true nagative
confustionMatrix = {
    "tp" : 0,
    "fp" : 0,
    "fn" : 0,
    "tn" : 0,
}


# go thru each review from testing set
for reviewName in testingSet.keys():
    
    result = str(testingSet[reviewName]['sentiment'])
    correct = str(correctTest[reviewName])
    
    outputFile.write(f"{reviewName} {result}\n") # write the ID and sentiment to the output file
    
    if ( result == correct ):
        
        # print(f"{reviewName}: {result} == {correct}") 
        
        if (result == "1") :
            
            confustionMatrix["tp"] += 1 # increment true positive
            
        else:
            
            confustionMatrix["tn"] += 1 # increment true negative
        
    else:
        
        # print(f"{reviewName}: {result} != {correct} *")
        
        if (result == "1" and correct == "0") :
            
            confustionMatrix["fp"] += 1 # increment false positive
            
        else:
            
            confustionMatrix["fn"] += 1 # increment false negative
        
        errorCount += 1 # increment errorCount
    
    count += 1

##### calculate precision & recall #####

tp = confustionMatrix["tp"] #  true positive
fp = confustionMatrix["fp"] # false positive
fn = confustionMatrix["fn"] # false negative
tn = confustionMatrix["tn"] # true negative

# precision
precision = round((tp)/(tp + fp), 3)

# recall
recall = round((tp)/(tp+fn), 3)

# F measure
f1 = round((2 * precision * recall)/(precision + recall), 3)


###### ACTUAL OUTPUTS ######

print()
print(80*"-")
print()
print("OUTPUT: ")
print()    
print(f"*  {len(correctTest)} of reviews were tested and {errorCount} reviews have different results.  *")

print()
# output for tp, fp, fn, tn

print(f"True Positive: {tp}")
print(f"False Positive: {fp}")
print(f"False Negative: {fn}")
print(f"True Negative: {tn}")

print()
# output for the precision, recall and f measure

print(f"Precision: {precision}")
print(f"Recall: {recall}")
print(f"F measure: {f1}")
print()
print(80*"-")

# close the output file
outputFile.close()
        
    
