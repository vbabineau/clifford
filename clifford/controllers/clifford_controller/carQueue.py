import pandas as pd
from vectors import Point, Vector
from matplotlib import pyplot as plt
from path import vecToSeg,intersect,plot_intersect
from collections import OrderedDict
import copy
import numpy as np


class carQueue(object):
    
    def __init__(self,message):
        self.queue = OrderedDict()
        self.queueLength= 0

        self.queueCar(message)
        self.carInterMatrix = None
        
    def createCar(self,message):
        car = dict()

        spltMess = message.split(':')
        car['name'] = spltMess[0]

        pos = spltMess[1].split('_')[0].split(',')
        car['pos'] = Point(round(float(pos[0]),2),round(float(pos[1]),2),round(float(pos[2]),2))

        vel = spltMess[1].split('_')[1].split(',')
        car['vel'] = np.array([float(vel[0]),float(vel[1]),float(vel[2])])

        car['speed'] = np.linalg.norm(car['vel'])
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

        car['targetSpeed'] = 22 #22 rad/s being the max speed of the tinkerbot
        
        car['intersectingPaths'] = []
        return car

    def queueOrder(self):
        return self.queue.keys()

    def queueCar(self,message, update=False):
        car = self.createCar(message)
        self.queue[car.pop('name')] = car
        if self.queueLength<len(self.queueOrder()) and self.queueLength!=0:
            print(message)
            self.reorderQueue()
        elif update:
            self.reorderQueue()
            
        self.queueLength = len(self.queueOrder())
        

    def reorderQueue(self):
        
        carInterMatrix=pd.DataFrame(index = self.queue.keys(), columns = self.queue.keys() )
        for carName in self.queue.keys():
            queueCopy = list(self.queue.keys())
            car = self.queue[carName]
            
            
            if len(queueCopy)>1:
                queueCopy.remove(carName)

                for carCName in queueCopy:
                   
                    carC = self.queue[carCName]
                    carInterMatrix.loc[carName,carCName] = []

                    for seg1 in car["segmentPath"][1:]:

                        v= []
                        pos1 = car["segmentPath"][car["segmentPath"].index(seg1)-1]
                        index=car["segmentPath"].index(seg1)

                        for seg2 in carC["segmentPath"][1:]:

                            pos2 = carC["segmentPath"][carC["segmentPath"].index(seg2)-1]
                            
                            v.append( intersect(pos1.round(),seg1.round(),pos2.round(),seg2.round()))
                            
                        carInterMatrix.loc[carName,carCName].append(v)
                    carInterMatrix.loc[carName,carCName] = np.array(carInterMatrix.loc[carName,carCName],dtype=object)


                self.queue[carName]['intersectingPaths'] = carInterMatrix.loc[carName]
        carInterMatrix=carInterMatrix.fillna(0)

        self.carInterMatrix = pd.DataFrame(index = self.queue.keys(), columns = self.queue.keys() )
        



        for i in carInterMatrix.index:

            for j in carInterMatrix.columns:

                if type(carInterMatrix.loc[i,j])!=int :
                    if type(carInterMatrix.loc[i,j].any())!=tuple:
                        self.carInterMatrix.loc[i,j]=carInterMatrix.loc[i,j].any()
                    else:
                        self.carInterMatrix.loc[i,j]=carInterMatrix.loc[i,j].any()
        if len( self.queueOrder())>1:
            print("Clean up")
            print(self.carInterMatrix)
        carSpeedMatrix=pd.DataFrame(index = self.queue.keys(),columns= self.queue.keys())
        breaking_d=.35
        keysCopy=list( self.queue.keys())
        for carName in self.queue.keys():
            car = self.queue[carName]

            for carCName in keysCopy:
                carC = self.queue[carCName]
                arr = []
                if not(self.carInterMatrix.loc[carName,carCName]):
                    arr.append(22)
                    
                elif type(self.carInterMatrix.loc[carName,carCName])!=float:
                    p = self.carInterMatrix.loc[carName,carCName]
                    d1 = round(np.linalg.norm(np.array(p)-np.array((car['pos'].x,car['pos'].z))),3)
                    t1 = round(d1/np.linalg.norm( car['speed']*0.02652),3)
                    d2 = round(np.linalg.norm(np.array(p)-np.array((carC['pos'].x,carC['pos'].z))),3)
                    t2 = round(d2/np.linalg.norm( carC['speed']*0.02652),3)
                    if t1<t2:
                        arr.append(round(car['speed'],2))
                        
                    elif t1>t2:
                        deltaT= t1-t2
                        carSpe=car['speed']
                        if deltaT*abs( car['speed']*0.02652)<.011+breaking_d:
                            carSpe= round((d1-.011-breaking_d-deltaT*abs( car['speed'])*0.02652)/(t1*0.02652),4)
                        arr.append(round(carSpe,2))
                    else:
                        names = [carName,  carCName]
                        names = np.sort(names)
                        if names[0]!=carName:
                            car=self.queue[names[0]]
                            carC=self.queue[names[1]]
                            d1 = round(np.linalg.norm(np.array(p)-np.array((car['pos'].x,car['pos'].z))),3)
                            t1 = round(d1/np.linalg.norm( car['speed']*0.02652),3)
                            d2 = round( np.linalg.norm(np.array(p)-np.array((carC['pos'].x,carC['pos'].z))),3)
                            t2 = round( d2/np.linalg.norm( carC['speed']*0.02652),3)
                            carCspe= round((d1-.011-breaking_d)/(t1*0.02652),4)
                            arr.append(carCspe)
                        else:
                            arr.append(round(car['speed'],2))
                else:
                    arr.append(22)

                carSpeedMatrix.loc[carName,carCName] =  arr

        if len( self.queueOrder())>1:
            print(carSpeedMatrix)
        for i in carSpeedMatrix.index:
            self.queue[i]['speed']= min(carSpeedMatrix.loc[i])[0]
        # self.plotpath(carInterMatrix)

                            


    def plotpath(self,carInterMatrix):
        keys=list( self.queue.keys())
        keysCopy=list( self.queue.keys())
        plt.figure(figsize=(10,10))
        plt.title("Full plan Vision")
        plt.twinx().set_ylabel('z')
        plt.twinx().set_xlabel('x')
        plt.xlim(-6,6)
        plt.grid()
        plt.ylim(6,-6)

        for carName in self.queue.keys():
            
            car = self.queue[carName]
            ctr=keys.index(carName)
            
            a=['b-','r-','g-']
            for seg in car["segmentPath"][1:]:
                pos = car["segmentPath"][car["segmentPath"].index(seg)-1]
                arr=np.array([pos.to_2dlist(),seg.to_2dlist()])
                plt.plot(arr[:,0],arr[:,1],a[ctr-1],label=carName)
        for carName in self.queue.keys():
            keysCopy.remove(carName)
            for  carCName in keysCopy:
                for V in carInterMatrix.loc[carName, carCName]:
                    for p in V:
                        if p:
                            if len(p)<=1:
                                plt.plot(p[0][0],p[0][1],'co')
                            else:
                                na=np.array(p)
                                plt.plot(na[:,0],na[:,1],'m-',linewidth=4)

            
        plt.legend()
        plt.pause(3)
        plt.close()


if __name__ == '__main__':
    queue = carQueue('babyPluto:0.29,0.07,4.7_0.0,0.0,-22.0_0.0,0.0,-4.95|5.11,0.0,0.0_')
    queue.queueCar('I3OT:-4.5,0.06,-0.25_22.0,-0.0,0.0_9.9,0,0.0_')
    queue.queueCar('babyPluto(1):0.29,0.07,3.85_0.0,0.0,-22.0_0.0,0.0,-4.1|5.11,0.0,0.0_')