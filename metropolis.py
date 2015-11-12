import numpy as np
from matplotlib import pyplot as plt

def Metropolis():
    nThrows = 10000
    x, y = 0,0
    delta = 0.1
    inCircle = 0
    inSquare = 1

    for i in xrange(nThrows):
        deltaX = np.random.uniform(-delta,delta)
        deltaY = np.random.uniform(-delta,delta)
        newX , newY = x+deltaX, y+deltaY
        r = np.sqrt(newX**2+newY**2)
        if r <= 1.:
            inCircle += 1
            inSquare += 1
            x , y = newX, newY
        elif (abs(newX) <= 1. and abs(newY) <= 1.) and (r > 1.):
            inSquare += 1
            x, y = newX, newY
        elif (abs(newX) > 1.) or (abs(newY) > 1.) and (r > 1.):
            inSquare += 1
            x , y = x, y
    return (4.*inCircle)/inSquare

def NotMetropolis():
    nThrows = 10000
    x, y = 0,0
    delta = 0.1
    inCircle = 0
    inSquare = 1
    
    for i in xrange(nThrows):
        deltaX = np.random.uniform(-delta,delta)
        deltaY = np.random.uniform(-delta,delta)
        newX , newY = x+deltaX, y+deltaY
        r = np.sqrt(newX**2+newY**2)
        if r <= 1.:
            inCircle += 1
            inSquare += 1
            x , y = newX, newY
        elif (abs(newX) <= 1. and abs(newY) <= 1.) and (r > 1.):
            inSquare += 1
            x, y = newX, newY
        elif (abs(newX) > 1.) or (abs(newY) > 1.) and (r > 1.):
            x, y = newX, newY
    return (4.*inCircle)/inSquare

nTrials = 1000
NonMet = []
Met = []
for i in xrange(nTrials):
    m = Metropolis()
    n = NotMetropolis()
    Met.append(m)
    NonMet.append(n)

print sum(Met)/nTrials
print sum(NonMet)/nTrials

Met = np.array(Met)
NonMet = np.array(NonMet)

fig = plt.figure(1)
ax1 = fig.add_subplot(121)
ax2 = fig.add_subplot(122)
histMet,_,_ = ax1.hist(Met,25)
histNonMet,_,_ = ax2.hist(NonMet,25)
plt.show()
