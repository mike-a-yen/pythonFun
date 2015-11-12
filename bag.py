import numpy as np
import random

class Bag:
    '''
    A bag of contents, that allows you to reach in and
    randomly grab one of its contents at a time.
    '''
    def __init__(self,contents=[]):
        self.__originalContents = list(contents)
        self.contents = list(contents)
        self.itemsDrawn = []
    def Add(self,newContents):
        ''' Add new content to the bag '''
        self.contents += [newContents]
    def Remove(self,item):
        ''' Remove a specific item '''
        if item in self.contents:
            self.contents.remove(item)
        else:
            raise ValueError('Item %s not in bag'%str(item))
    def Shuffle(self):
        ''' Shake up the bag to randomize the order of its contents'''
        random.shuffle(self.contents)
        print 'Bag has been shuffled!'
    def Draw(self):
        ''' Take an item out of the bag '''
        num = np.random.randint(0,len(self.contents))
        item = self.contents.pop(num)
        self.itemsDrawn.append(item)
        return item
    def __repr__(self):
        return '<Bag: %s >'%sorted(self.contents)
