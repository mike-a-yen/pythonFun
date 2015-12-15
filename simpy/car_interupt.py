import simpy
import numpy as np

class Car(object):
    def __init__(self,env):
        self.env = env
        # start the run process everytime an
        # instance is created.
        self.action = env.process(self.run())
        self.battery_life = 0

    def run(self):
        while True:
            print 'Start parking and charging at %d' %self.env.now
            charge_duration = 5
            try:
                yield self.env.process(self.charge(charge_duration))
                self.battery_life += charge_duration
                print 'Battery Life: '+'#'*self.battery_life

            except simpy.Interrupt:
                print 'Charing Interupted......%d'%self.env.now
                self.battery_life += 3
                print 'Battery Life: '+'#'*self.battery_life
                
            print 'Start driving at %d' %self.env.now
            trip_duration = 2
            self.battery_life -= trip_duration*2
            print 'Battery Life: '+'#'*self.battery_life
            yield self.env.timeout(trip_duration)

    def charge(self,duration):
        yield self.env.timeout(duration)

def driver(env,car):
    yield env.timeout(3)
    car.action.interrupt()
    
env = simpy.Environment()
car = Car(env)
t = 0
while True:
    if np.random.uniform() < 0.5:
        env.process(driver(env,car))
    t += 10
    env.run(until=t)
    if len(raw_input('continue: ')) >= 1:
        env.exit()
        break
    
    
