import numpy as np
from matplotlib import pyplot as plt

class Disk(object):
    def __init__(self, ID, radius, x, y, vx, vy, mass=5, color='blue'):
        self.ID = ID
        self.radius = radius
        self.mass = mass
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        self.color = color
        #self.circle = plt.Circle((self.x,self.y),self.radius,color=self.color)
    def SetPosition(self, x, y):
        self.x = x
        self.y = y
        #self.circle = plt.Circle((self.x,self.y),self.radius,color=self.color)
    def SetVelocity(self, vx, vy):
        self.vx = vx
        self.vy = vy
    def SetColor(self, color):
        self.color = color

def EventFinder(disks, boardSize):
    # find time to disk collisions with walls
    # find time to disk collisions with disks
    eventTimes = []
    wallTimes = []
    pairTimes = []
    # walls first
    for disk in disks:
        r = disk.radius
        x,y = disk.x, disk.y
        vx,vy = disk.vx, disk.vy
        tx = max([(0.-(x-r))/vx, (boardSize[0]-(x+r))/vx])
        ty = max([(0.-(y-r))/vy, (boardSize[1]-(y+r))/vy])
        #print tx, ty
        t = min([tx,ty])
        wall = np.argmin([tx,ty])
        eventTimes.append((t,disk,wall))
        wallTimes.append((t,disk,wall))

    for disk1 in disks:
        for disk2 in disks:
            if disk1 == disk2: continue
            r1,r2 = disk1.radius,disk2.radius
            x1,y1,x2,y2 = disk1.x, disk1.y,disk2.x,disk2.y
            vx1,vy1,vx2,vy2 = disk1.vx,disk1.vy,disk2.vx,disk2.vy
            delx = x1-x2
            dely = y1-y2
            delvx = vx1-vx2
            delvy = vy1-vy2
            a = (delvx**2+delvy**2)
            b = 2.*(delx*delvx+dely*delvy)
            c = -(r1+r2)**2+delx**2+dely**2
            if (b**2-4*a*c) >= 0.:
                t1 = (-b + np.sqrt(b**2-4.*a*c))/(2.*a)
                t2 = (-b - np.sqrt(b**2-4.*a*c))/(2.*a)
                t = max([t1,t2])
                if t >= 0.:
                    pairTimes.append((t, disk1, disk2))
                    eventTimes.append((t, disk1, disk2))
                else:
                    pairTimes.append((float('inf'),disk1,disk2))
                    eventTimes.append((float('inf'),disk1,disk2))
            else:
                pairTimes.append((float('inf'),disk1,disk2))
                eventTimes.append((float('inf'),disk1,disk2))
        return np.array(wallTimes), np.array(pairTimes)

def WallCollision(disk,wall):
    # wall == 0 for sides
    # wall == 1 for top and bottom
    vx,vy = disk.vx, disk.vy
    if wall == 0:
        disk.SetVelocity(-vx,vy)
    elif wall == 1:
        disk.SetVelocity(vx,-vy)

def ElasticCollision(disk1, disk2):
    v1x,v1y = disk1.vx, disk1.vy
    v2x,v2y = disk2.vx, disk2.vy
    m1,m2 = disk1.mass, disk2.mass
    # energy and momentum conservation
    v1xf = (v1x*(m1-m2)+2.*m2*v2x)/(m1+m2)
    v1yf = (v1y*(m1-m2)+2.*m2*v2y)/(m1+m2)
    v2xf = (v2x*(m2-m1)+2.*m2*v1x)/(m1+m2)
    v2yf = (v2y*(m2-m1)+2.*m2*v1y)/(m1+m2)
    disk1.SetVelocity(v1xf,v1yf)
    disk2.SetVelocity(v2xf,v2yf)

def UpdateDiskPositions(disks,delt):
    for disk in disks:        
        disk.SetPosition(disk.x+disk.vx*delt, disk.y+disk.vy*delt)

def PlotDisks(disks):
    fig, ax = plt.subplots(figsize=(6,6))
    ax.set_xlim(0,boardSize[0])
    ax.set_ylim(0,boardSize[1])
    for i, disk in enumerate(disks):
        circle = plt.Circle((disk.x,disk.y),disk.radius,color=disk.color)
        ax.add_patch(circle)
    plt.show()

boardSize = (100.,100.)
colors = ['red','blue','green','yellow','orange','purple']
nDisks = 10
disks = []
for i in xrange(nDisks):
    r = np.random.randint(1,6)
    x , y = np.random.uniform(r,boardSize[0]-r), np.random.uniform(r,boardSize[1]-r)
    vx , vy = np.random.uniform(-5,5,2)
    m = np.random.uniform(1,10)
    d = Disk(i, r, x, y, vx, vy, mass=m, color=colors[i%len(colors)])
    disks.append(d)

time = 0
nEvents = 15
PlotDisks(disks)
for i in xrange(nEvents):
    wallEvents, pairEvents = EventFinder(disks, boardSize)
    wallTimes = wallEvents[:,0]
    pairTimes = pairEvents[:,0]
    delt = min([min(wallTimes),min(pairTimes)])
    if min(wallTimes) < min(pairTimes): # wall collision
        print 'Wall'
        disk = wallEvents[np.argmin(wallTimes),1]
        wall = wallEvents[np.argmin(wallTimes),2]
        UpdateDiskPositions(disks,delt)
        WallCollision(disk,wall)
        time += delt
    elif min(pairTimes) < min(wallTimes): # pair collision
        disk1, disk2 = pairEvents[np.argmin(pairTimes),1:]
        UpdateDiskPositions(disks,delt)
        ElasticCollision(disk1,disk2)
        time += delt
    print 'Time',time
    print 'delT', delt
    PlotDisks(disks)
