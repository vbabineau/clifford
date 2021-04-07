from vectors import Point, Vector
from matplotlib import pyplot as plt
from path import vecToSeg,intersect,seg_intersect
from collections import OrderedDict
import copy
import numpy as np

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

        segPath = [car['pos']]

        for v in path:
            points = vecToSeg(segPath[-1],v)
            segPath.append(points[-1])
        car['segmentPath'] = segPath   

        car['targetVel'] = 22 #22 rad/s being the max speed of the tinkerbot
        
        car['intersectingPaths'] = []
        return car

    def queueOrder(self):
        return self.queue.keys()

    
    def queueCar(self,message):
        car = self.createCar(message)
        self.queue[car.pop('name')] = car
        if len(self.queue.keys())>1:
            self.reorderQueue()

    def reorderQueue(self):
        queueCopy = copy.copy(self.queue)

        for carName in self.queue.keys():
            car = self.queue[carName]
            queueCopy.pop(carName)
            
            if len(queueCopy.keys())>1:
                for carCName in queueCopy.keys():
                   
                    carC = queueCopy[carCName]
                    for seg1 in car["segmentPath"][1:]:
                        pos1 = car["segmentPath"][car["segmentPath"].index(seg1)-1]
                        index=car["segmentPath"].index(seg1)
                        for seg2 in carC["segmentPath"][1:]:
                            pos2 = carC["segmentPath"][carC["segmentPath"].index(seg2)-1]
                           
                            if intersect(pos1,seg1,pos2,seg2):
                                
                                #print(f"{index}.{carName}:{pos1}->{seg1} and {carCName}:{pos2}->{seg2} intersect")
                                car["intersectingPaths"].append(True)
                                
                            else:
                                car["intersectingPaths"].append(False)
                    if False:
                        print(carName,car["segmentPath"])
                        print(carCName,carC["segmentPath"])
                        self.plotpath(carName,carCName,car["segmentPath"],carC["segmentPath"])
    
    def plotpath(self,car1,car2,seglist1,seglist2):
        plt.figure(figsize=(30,30))
        plt.title(car1+" Vision")
        plt.xlim(-8,8)
        plt.ylim(8,-8)

        v= seglist1[0]
        a=['-','--']
        for ctr,v1 in enumerate(seglist1[1:]):
            arr=np.array([v.to_2dlist(),v1.to_2dlist()])
            plt.plot(arr[:,0],arr[:,1],'b'+a[ctr-1], label=car1+str(ctr))
            v=v1
        v= seglist2[0]
        for ctr,v2 in enumerate(seglist2[1:]):
            arr=np.array([v.to_2dlist(),v2.to_2dlist()])
            plt.plot(arr[:,0],arr[:,1],'r'+a[ctr-1], label=car2+str(ctr))
            v=v2
        plt.legend()
        plt.pause(.0)
plt.close()

if __name__ == '__main__':
    queue = carQueue('babyPluto:0.2919,0.0654,4.8651_-0.0,-0.0,-22.0_-0.0,-0.0,-5.1151|-5.1081,0.0294,0.0_')
    queue.queueCar('FiatPanda:5.2547,0.066,-0.7713_-22.0,-0.0,0.0_-5.5047,-0.0,0.0|0.0,0.03,-5.6713_')
    queue.queueCar('I3OT:-5.2245,0.0649,-0.1948_22.0,0.0,-0.0_4.9745,0.0,-0.0|0.0,0.0,-5.0948_')