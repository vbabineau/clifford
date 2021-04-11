"""clifford_controller controller."""
from controller import Robot,Motor
from vectors import Point, Vector
from path import createPath, updatePath,angle_between
import copy
from carQueue import *
import random
import struct
import numpy as np
import math
def unpack_helper(fmt, data):
    encoding = 'utf-8'
    size = struct.calcsize(fmt)
    (i,), data = struct.unpack(fmt, data[:size]), data[size:]
    s, info = data[:i], data[i:]
    s = str(s, encoding)
    return s
TIME_STEP = 64 #time in ms
WHEEL_RADIUS = 0.02625
ANGULAR_VELOCIY = 22
ANGULAR_ACCELERATION = 10 


#Create Robot
robot = Robot()

leftMotor = robot.getDevice('A') #get motor pointers
rightMotor = robot.getDevice('B')
pivot = robot.getDevice('pivot')
pivot.setPosition(0)
ANGULAR_VELOCIY = rightMotor.getMaxVelocity() #get max speed

gps = robot.getDevice('gps') # get gps
gps.enable(TIME_STEP) # Enable gps

comp = robot.getDevice('compass') #get compasss
comp.enable(TIME_STEP)

acceler = robot.getDevice('accelerometer')
acceler.enable(TIME_STEP)

receiv = robot.getDevice('receiver')
receiv.setChannel(1)
receiv.enable(TIME_STEP)

#0.27m/s^2

emitter= robot.getDevice('emitter')
#This should be changed in terms of breaking time
emitter.setRange(2)
emitter.setChannel(1)

#Start and end Points
startPoints = [Point(0.25,0.036,4.9),Point(5.4,0.036,-.75),Point(-5.4,0.036,-.75)]
endPoints = [Point(-0.25,0.036,4.9),Point(5.4,0.036,-.25),Point(-5.4,0.036,-.75)]


speed = ANGULAR_VELOCIY#*random.random() #Sets speed to a random fraction of the max
dirVect = comp.getValues() #normalized direction vector
coords = Point.from_list(gps.getValues())      #coordinates
velocity = Vector(dirVect[0]*speed,dirVect[1]*speed,dirVect[2]*speed)        #Velocity vector
destination = endPoints[random.randrange(0,2,1)]

#Initial Conditions?
leftMotor.setPosition(float('inf'))
rightMotor.setPosition(float('inf'))
leftMotor.setVelocity(1* speed)
rightMotor.setVelocity(1* speed)



transmissions = []

ctr = 0

#path = createPath(coords,destination,dirVect)
# Main loop:
# - perform simulation steps until Webots is stopping the controller
while robot.step(TIME_STEP) != -1: #infinite loop cause TIME_STEP never changing
    
    acceleration = acceler.getValues()
    dirList = np.round(comp.getValues(),2).tolist()
    dirVect = Vector.from_list(dirList)
    coords = Point.from_list(np.round(gps.getValues(),2).tolist())
    destination.y=coords.y
    velocity = Vector(dirList[0]*speed,dirList[1]*speed,dirList[2]*speed)

    if ctr == 0: # first iteration we create a path
        try:
            # print(coords,destination, dirVect)
            path = createPath(coords,destination, dirVect )
            while len(path)<1:
                destination = endPoints[random.randrange(0,2,1)]
                path = createPath(coords,destination, dirVect)    
        except ValueError:
            endPoints.remove(destination)
            destination = endPoints[random.randrange(0,1,1)]
            path = createPath(coords,destination, dirVect)   
            while len(path)<1:
                destination = endPoints[random.randrange(0,1,1)]
                path = createPath(coords,destination, dirVect)    
        print(path)
    else:
        path = updatePath(coords,destination, dirVect,path)
    
    try:
        compensatedDir=Vector(-dirVect.x,dirVect.y,dirVect.z)
        pathCarAngle =angle_between(path[0].to_2dlist(),dirVect.to_2dlist())*180/math.pi
    except ValueError:
        
        pathCarAngle = 0
        pass
    except IndexError:
        rightMotor.setVelocity(0)
        leftMotor.setVelocity(0)
        break

    if round(dirVect.cross(path[0]).y,3)!=0  :
        ratio= (abs(90-(pathCarAngle))/90)
        
        if( round(dirVect.cross(path[0]).y,3)<0):
            pivot.setPosition(-(0.40*(1-ratio**3)+.01))
            rightMotor.setVelocity(speed)
            leftMotor.setVelocity((.55+.45*ratio)* speed)
        else:
            pivot.setPosition((0.40*(1-ratio**3)+.01))
            rightMotor.setVelocity((.55+.45*ratio)* speed)
            leftMotor.setVelocity(speed)
    else:
        pivot.setPosition(0)
        rightMotor.setVelocity(speed)
        leftMotor.setVelocity(speed)
     
    if ctr==0:
        dirVect = np.round(comp.getValues(),2).tolist()
        print(f'Going from {coords}to {destination}')
        for i,v in enumerate(path):
            print('Vector',i+1,v)
        print("----------------------")

    if ctr%1 == 0:
        message = robot.getName()+':'
        message+= str(round(coords.x,4))+","+str(round(coords.y,4))+","+str(round(coords.z,4))+"_"
        message+= str(round(velocity.x,4))+","+str(round(velocity.y,4))+","+str(round(velocity.z,4))+"_"
        for v in path:
            message+=str(round(v.x,4))+','
            message+=str(round(v.y,4))+','
            message+=str(round(v.z,4))
            if v == path[-1]:
                message+='_'
            else:
                message+='|'
        if ctr ==0:
            queue = carQueue(message)
            print(message)
        elif ctr%20 ==0:
            queue.queueCar(message,update=True)

        message = bytes(message, 'utf-8')
        message =  struct.pack("I%ds" % (len(message),), len(message), message)
        emitter.send(message)

    while receiv.getQueueLength() >0:
        data = receiv.getData()
        data = unpack_helper("I",data)
        transmissions.append(data)
        receiv.nextPacket()
    
    for t in transmissions:
        queue.queueCar(t)
        transmissions.remove(t)

        


    speed = round(queue.queue[robot.getName()]['speed'],2)
    ctr+=1

    pass

# Enter here exit cleanup code.
