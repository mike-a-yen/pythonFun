import numpy as np
import random
import sys

class Deck (object):
    def __init__(self):
        self.newDeck = self.makeNewDeck()
        self.shuffledDeck = self.shuffleDeck(self.newDeck)

    def makeNewDeck(self):
        self.newDeck = []
        for ii in xrange(1,14):
            for jj in xrange(4):
                self.newDeck.append(ii)
        return self.newDeck

    def rearrangeDeck(self,deck):
        for ii in xrange(len(deck)):
            place = np.random.randint(1,52)
            card = deck.pop(ii)
            deck.insert(place,card)
        return deck
    
    def shuffleDeck(self,deck):
        nRearrange = np.random.randint(100,1000)
        print nRearrange
        for ii in xrange (0,nRearrange):
            deck = self.rearrangeDeck(deck)
        return deck
        
class War (object):
    def __init__(self):
        newGame = Deck()
        self.deck = newGame.shuffledDeck
        self.deck1, self.deck2 = self.splitDeck(self.deck)
        self.deck1 = Deck.shuffleDeck(newGame,self.deck1)
        self.deck2 = Deck.shuffleDeck(newGame,self.deck2)
        self.inPlay1 = []
        self.inPlay2 = []
        self.score1 = 0
        self.score2 = 0
        self.battleCounter = 0

    def splitDeck(self,deck):
        deck1 = []
        deck2 = []
        for ii in xrange(0,len(deck),2):
            deck1.append(deck[ii])
        for jj in xrange(1,len(deck),2):
            deck2.append(deck[jj])
        return deck1, deck2
    
    def beginGame(self):
        print self.deck1
        print self.deck2
        while (len(self.deck1) != 0 and len(self.deck2) != 0):
            self.inPlay1 = []
            self.inPlay2 = []
            self.battleCounter += 1
            #print "--------------------------------"
            self.play()
            #print "--------------------------------"
        self.declareWinner()

    def drawCards(self):
        if len(self.deck1) == 0 or len(self.deck2) == 0:
            self.declareWinner()
            return None
        self.inPlay1.append(self.deck1.pop(0))
        self.inPlay2.append(self.deck2.pop(0))


    def returnCardsToHand(self,player):
        allInPlay = self.inPlay1+self.inPlay2
        random.shuffle(allInPlay)
        for card in allInPlay:
            if player == 1:
                self.deck1.append(card)
            elif player == 2:
                self.deck2.append(card)
            
    def declareWinner(self):
        print "Player 1: %d" %self.score1
        print "Player 2: %d" %self.score2
        print "N Battles: %d" %self.battleCounter
        if self.score1 > self.score2:
            print "Player 1 WINS!"
        elif self.score2 > self.score1:
            print "Player 2 WINS!"

    def play(self):
        self.drawCards()
        if self.inPlay1[-1] == self.inPlay2[-1]: # tie, draw again if there are more cards
            self.play()
        elif self.inPlay1[-1] > self.inPlay2[-1]: # player 1 wins
            self.returnCardsToHand(1)
            self.score1 += len(self.inPlay1)
        elif self.inPlay2[-1] > self.inPlay1[-1]: # player 2 wins
            self.returnCardsToHand(2)
            self.score2 += len(self.inPlay1)
            
