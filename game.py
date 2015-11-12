import numpy as np
import sys

class Game:
    def __init__ (self, gameNumber):
        self.gameNumber = gameNumber
        self.gameBoard = Board(self)
        self.nSpaces = self.gameBoard.nSpaces 
        self.nPeople = 200
        self.nCouples = 0
        self.population = Population(self.nPeople, self)
    
    def AdvanceTurn (self):
        for person in self.population.people:
            person.Move()
        for x in xrange(self.gameBoard.boardSize[0]):
            for y in xrange(self.gameBoard.boardSize[1]):
                space = self.gameBoard.GetSpace(x,y)
                self.MatchMaker(space)
        print self.CoupleCounter()
        print self.CoupleTracker()

    def CheckForOccupants(self, Space):
        if len(Space.GetOccupants()) <= 1:
            return False
        elif len(Space.GetOccupants()) >= 2:
            return True

    def CoupleCounter (self):
        counter = 0

        for person in self.population.people:
            if person.relationship == None: continue
            else:
                counter += 1
        return counter/2

    def CoupleTracker (self):
        couples = []
        for person in self.population.people:
            if person.taken == False: continue
            couple = [person.ID,person.relationship.ID]
            couples.append(couple)
        return couples

    def MatchMaker (self, Space):
        if self.CheckForOccupants(Space) == False:
            return None
        occupants = Space.GetOccupants()
        males = Space.GetMales()
        females = Space.GetFemales()
        if males == 0: return None
        if females == 0: return None
        for person1 in occupants:
            for person2 in occupants:
                if person1.ID == person2.ID: continue
                if person1.sexuality != person2.sexuality: continue
                if (person1.sexuality == 0 and person1.gender == person2.gender): continue
                if (person1.sexuality == 1 and person1.gender != person2.gender): continue
                # how much person1 wants person2
                person1Want = person2.score*(1.-person1.faithfullness)*(1.-person1.pickiness)
                person1Ask = int(round(np.random.normal(person1Want, 0.5-abs(person1Want-0.5))))
                if person1Ask < 0: person1Ask = 0
                # how much person2 wants person1
                person2Want = person1.score*(1.-person2.faithfullness)*(1.-person2.pickiness)
                person2Ask = int(round(np.random.normal(person2Want, 0.5-abs(person1Want-0.5))))
                if person2Ask < 0: person2Ask = 0
                if person1Ask == 1 and person2Ask == 1:
                    # make the relationship
                    person1.SetRelationship(person2)
                    person2.SetRelationship(person1)
                    print 'Made Couple 1'
                elif person1Ask == 1 and person2Ask == 0:
                    accept = int(round(np.random.normal(person2Want, 0.5-abs(person2Want-0.5))))
                    if accept == 1: # make relationship
                        person1.SetRelationship(person2)
                        person2.SetRelationship(person1)
                        print 'Made Couple 2'
                elif person2Ask == 1 and person1Ask == 0:
                    accept = int(round(np.random.normal(person1Want, 0.5-abs(person1Want-0.5))))
                    if accept == 1: # make relationship
                        person1.SetRelationship(person2)
                        person2.SetRelationship(person1)
                        print 'Made Couple 3'
                elif person1Ask == 0 and person2Ask == 0:
                    continue

class Board:
    def __init__ (self,Game):
        self.boardSize = (10,10)
        self.nSpaces = self.boardSize[0]*self.boardSize[1]
        self.spaces = np.empty((self.boardSize[0], self.boardSize[1]), dtype=object)
        for x in xrange(self.boardSize[0]):
            for y in xrange(self.boardSize[1]):
                self.spaces[x,y] = Space(x,y)
    def GetBoardSize (self):
        return self.boardSize
    def GetSpace (self, x, y):
        return self.spaces[x,y]
   
    def DrawBoard(self):
        for x in xrange(self.boardSize[0]):
            sys.stdout.write("| ")
            for y in xrange(self.boardSize[1]):
                for person in self.GetSpace(x,y).GetOccupants():
                    sys.stdout.write("%d " %person.ID)
                sys.stdout.write("|")
            sys.stdout.write("\n")

class Space:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.occupants = []
    def GetCoords (self):
        return (self.x, self.y)
    def GetOccupants (self):
        return self.occupants
    def GetMales(self):
        males = []
        for person in self.GetOccupants():
            if person.GetGender() == 0:
                males.append(person)
        return males
    def GetFemales (self):
        females = []
        for person in self.GetOccupants():
            if person.GetGender() == 1:
                females.append(person)
        return females
    def AddOccupant (self, Person):
        self.occupants.append(Person)
        print 'Added person to space %d,%d' %(self.x, self.y)
    def RemoveOccupant (self, Person):
        for p in self.GetOccupants():
            if p.ID == Person.ID:
                self.occupants.remove(Person)
                return 'Removed #%d from Space (%d,%d)' %(Person.ID, self.x, self.y)
        return 'That person is not in this space'

class Population:
    def __init__(self,size, Game):
        self.size = size
        self.people = []
        for i in xrange(self.size):
            self.people.append( Person(i, Game) )
        
    def GetLocations (self):
        locations = []
        for person in people:
            locations.append(person.GetLocation)

class Person:
    def __init__ (self, ID, Game):
        self.gameBoard = Game.gameBoard
        self.boardSize = self.gameBoard.GetBoardSize()
        self.ID = ID
        # gender: 0 = male; 1 = female
        self.gender = np.random.randint(0,2)
        self.age = np.random.uniform(20,40)
        self.looks = np.random.uniform(0,1)
        self.personality = np.random.uniform(0,1)
        self.pickiness = np.random.normal(0.5,0.25)
        if self.pickiness < 0: self.pickiness = 0.
        elif self.pickiness > 1: self.pickiness = 0.9999
        self.faithfullness = 0.
        #self.faithfullness = np.random.normal( (6.5 - ((self.age-30)/15.)**2), 0.3) * \
        #    (10 - np.random.normal(self.looks/2., self.looks/4.))/10. * \
        #    (np.random.normal(self.personality, (-(self.personality)**2+ 10*self.personality)/10. ))/10.
        self.score = (self.looks + self.personality)/2.
        self.sexuality = int(round(np.random.normal(0.75,0.34)))
        # relationship: None = single; person object = involved
        self.relationship = None
        self.taken = False
        # place person in random place on the board
        self.x = np.random.randint(0, self.boardSize[0])
        self.y = np.random.randint(0, self.boardSize[1])
        self.location = self.gameBoard.GetSpace(self.x, self.y)
        self.location.AddOccupant(self)
        
    def GetAge (self):
        return self.age
    def GetGender (self):
        return self.gender
    def GetLooks (self):
        return self.looks
    def GetPersonality (self):
        return self.personality
    def GetPickiness (self):
        return self.pickiness
    def GetRelationship (self):
        return self.relationship
    def GetPartner (self):
        if self.taken == True:
            return self.relationship.ID
        elif self.taken == False:
            return None
    def GetTaken (self):
        return self.taken
    def GetLocation (self):
        return self.location
    
    def SetAge (self, age):
        self.age = age
    def SetRelationship (self, person):
        self.relationship = person
        if person != None and person.ID != self.ID:
            self.taken = True
            self.faithfullness = np.random.normal( (6.5 - ((self.age-30)/15.)**2), 2.)/10. * \
            (1. - np.random.normal(self.looks/2., self.looks/4.)) * \
            (np.random.normal(self.personality, 5*(-(self.personality)**2 + self.personality) ))
            if self.faithfullness < 0.: self.faithfullness = 0.
            elif self.faithfullness > 1.: self.faithfullness = 0.9999
        elif person == None:
            self.taken = False
            self.faithfullness = 0.
    def SetLocation (self, newx , newy):
        self.gameBoard.GetSpace(self.x, self.y).RemoveOccupant(self)
        self.x, self.y = newx, newy
        self.location = self.gameBoard.GetSpace(self.x, self.y)            
        self.location.AddOccupant(self)

    def Move(self):
        # all people can move either +1, 0, -1
        xshift = np.random.randint(-1,2)
        yshift = np.random.randint(-1,2)

        if (self.x == (self.boardSize[0]-1) and xshift == 1):
            newx = 0
        elif (self.x == 0 and xshift ==  -1):
            newx = self.boardSize[0]-1
        else:
            newx = self.x + xshift

        if (self.y == (self.boardSize[1]-1) and yshift == 1):
            newy = 0
        elif (self.y == 0 and yshift == -1):
            newy = self.boardSize[1]-1
        else:
            newy = self.y + yshift

        self.SetLocation(newx, newy)
