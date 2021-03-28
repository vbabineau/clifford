from vectors import Point, Vector
from collections import OrderedDict
#I3OT:4.0171,0.0662,4.0171_1.0482,0.0,-0.0__PathS1.3829,0.0,-0.0_0.0,0.0,0.0552_PathE 
class carQueue(object):
    
    def __init__(self,message):
        self.queue = OrderedDict()
        self.queueCar(message)
        

    def createCar(self,message):
        car = dict()

        spltMess = message.split(':')
        car['name'] = spltMess[0]

        pos = spltMess[1].split('_')[0].split(',')
        car['pos'] = Point(float(pos[0]),float(pos[1]),float(pos[2]))

        vel = spltMess[1].split('_')[1].split(',')
        car['vel'] = Point(float(vel[0]),float(vel[1]),float(vel[2]))

        path = []
        for v in spltMess[1].split('_')[2].split('|'):
            v=v.split(',')
            path.append(    Vector( float(v[0]), float(v[1]), float(v[2])  ))
        car['path'] = path

        #Maybe add a target velocity that is calculated when there are more than one cars in queue
        #We can then access this target velocity and force the car to slow down
        return car

    def queueOrder(self):
        return self.queue.keys()

    
    def queueCar(self,message):
        car = self.createCar(message)
        self.queue[car.pop('name')] = car
        if len(self.queue.keys())>1:
            try:
                self.reorderQueue()
            except NotImplementedError:
                print('Warning the queue Reordering is not implemented yet.')
                print('The queue order will not be optimized for its purpose')
                print(self.queueOrder())
                for car in self.queueOrder():   
                    print(self.queue[car])
                print("______________________"*5)

    def reorderQueue(self):
        raise NotImplementedError

if __name__ == '__main__':
    quque = carQueue('FiatPanda:0.2636,0.0662,0.2636_-21.9016,-0.0,0.0_-0.5136,-0.0,0.0|0.0,0.03,-5.6713_')