import numpy as np
import string
import copy

alphabet = list(string.lowercase)
f = open('/usr/share/dict/words')
dictionary = f.read().splitlines()
f.close()
lowerCut = [word.islower() for word in dictionary]
upperCut = [word.isupper() for word in dictionary]
#lowerDictionary = dictionary[lowerCut]
#upperDictionary = dictioanry[upperCut]
message = 'attack at dawn'
message = message.replace(' ','').lower()
key = 'do it now'
key = key.replace(' ','').lower()

def Encrypte(message,key):
    message = message.replace(' ','')
    cipherText = ''
    for i,letter in enumerate(message):
        isUpper = letter.isupper()
        letterIndex = alphabet.index(letter.lower())
        shift = alphabet.index(key[i%len(key)])
        cipherText += alphabet[ (letterIndex+shift)%len(alphabet) ]
    #print cipherText
    return cipherText

def Decrypte(cipherText, key):
    key = key.lower()
    message = ''
    for i,letter in enumerate(cipherText):
        isUpper = letter.isupper()
        letterIndex = alphabet.index(letter)
        shift = alphabet.index(key[i%len(key)])
        message += alphabet[ (letterIndex-shift)%len(alphabet) ]
    #print message
    return message

def CipherBreaker(cipherText,keyLength):
    #assume single word message and key
    for key in dictionary:
        if key.islower() == False: continue
        if len(key) != keyLength: continue
        message = Decrypte(cipherText,key)
        if message in dictionary:
            print key
            print message
            
def SubsetSum(target):
    # partition is a list of lists of the numbers 
    # that add up to the target number
    if target == 1:
        return [[1]]
    elif target > 1:
        partition = SubsetSum(target-1)
        nextPartition = copy.copy(partition)
        for p,part in enumerate(partition):
            for i in xrange(len(part)):
                temp = copy.copy(part)
                temp[i] += 1
                nextPartition.append(temp)
            if part == [1]*(target-1):
                nextPartition[p].append(1)

    finalPartition = copy.copy(nextPartition)
    for p,part in enumerate(nextPartition):
        if sum(part) != target:
            #print part
            finalPartition.remove(part)
    fp = set(map(tuple,finalPartition))
    finalParts = map(list,fp)
    print finalParts
    return finalParts
        
def ListOfWords(keyLength):
    # find a list of all possible keys
    # combinations is all possible lengths of words
    # that add up to the keyLength
    keyList = []
    combinations = SubsetSum(keyLength)
    wordsOfLength = {}
    for l in xrange(1,keyLength+1):
        if l == 1:
            wordsOfLength[str(1)] = ['a','i']
            continue
        elif l == 2:
            wordsOfLength[str(2)] = ['am','an','as','at','ax',
                                     'be','by','do','ex','go',
                                     'hi','id','if','in','is',
                                     'it','me','my','of','oh',
                                     'on','or','so','to','up']
            continue
        for word in dictionary:
            # only consider lower case words
            if word.islower() == False: continue
            if len(word) != l: continue
            if str(l) not in wordsOfLength.keys():
                wordsOfLength[str(l)]=[word]
            else:
                wordsOfLength[str(l)]+=[word]
    return wordsOfLength

def ListOfKeys(keyLength):
    wordsOfLength = ListOfWords(keyLength)
    combinations = SubsetCum(keyLength)
    setOfKeys = []
    for combo in combinations:
        keys = []
        for num in combo:
            print ''
        
                
ct = Encrypte(message,key)
mes = Decrypte(ct,key)
