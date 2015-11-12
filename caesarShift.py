import numpy as np

alphabet = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']

def Encode(message,shift):
    cipherText = ''
    for l in xrange(len(message)):
        letter = message[l]
        upper = letter.isupper()
        for abc in xrange(len(alphabet)):
            if letter not in alphabet:
                cipherText += letter
                break
            if letter != alphabet[abc]: continue
            if upper == True:
                cipherText += alphabet[abc+shift].upper()
            else:
                cipherText += alphabet[abc+shift].lower()
            break
    print cipherText

def Decode(cipherText,shift):
    message = ''
    for l in xrange(len(cipherText)):
        letter = cipherText[l]
        upper = letter.isupper()
        for abc in xrange(len(alphabet)):
            if letter.lower() not in alphabet:
                message += letter
                break
            if letter.lower() != alphabet[abc]: continue
            if upper == True:
                message += alphabet[abc-shift].upper()
            else:
                message += alphabet[abc-shift].lower()
            break
    print message
