"""clifford_controller controller."""
# You may need to import some classes of the controller module. Ex:
#  from controller import Robot, Motor, DistanceSensor
from controller import Robot,Motor
from vectors import Point, Vector
from path import createPath, updatePath
import random
import struct
import numpy as np
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
endPoints = [Point(-0.25,0.036,4.9),Point(5.4,0.036,-.25),Point(-5.4,0.036,-.25)]


speed = ANGULAR_VELOCIY*random.random() #Sets speed to a random fraction of the max
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
    coords = Point.from_list(gps.getValues())
    destination.y=coords.y
    velocity = Vector(dirList[0]*speed,dirList[1]*speed,dirList[2]*speed)

    if ctr == 0: # first iteration we create a path
        try:
            path = createPath(coords,destination, dirVect )
        except ValueError:
            endPoints.remove(destination)
            destination = endPoints[random.randrange(0,1,1)]
            path = createPath(coords,destination, dirVect)            
        print(f"Going from {coords} cm to {destination}")
        print(dirVect)
        print('Original Path:')
        for i,v in enumerate(path):
            print('Vector',i+1,v)
        print("----------------------")
        print(path[0])
    else:
        path = updatePath(coords,destination, dirVect,path)
    
    try:
        pathCarAngle = path[0].angle(dirVect)  % 180
    except ValueError:
        pathCarAngle = 0
        pass

    if pathCarAngle!=0:
        #print(round( path[0].cross(dirVect).y,2))
        ratio= (1-pathCarAngle/90) 
        if( round(path[0].cross(dirVect).y,3)>0):
            pivot.setPosition(0.25*(1-ratio)+.01)
            rightMotor.setVelocity(ANGULAR_VELOCIY)
            leftMotor.setVelocity((.75+.25*ratio)* ANGULAR_VELOCIY)
        else:
            pivot.setPosition(-(0.25*(1-ratio)+.01))
            rightMotor.setVelocity((.75+.25*ratio)* ANGULAR_VELOCIY)
            leftMotor.setVelocity(ANGULAR_VELOCIY)
    else:
        pivot.setPosition(0)
        rightMotor.setVelocity(ANGULAR_VELOCIY)
        leftMotor.setVelocity(ANGULAR_VELOCIY)
     
    if ctr==-1:
        dirVect = np.round(comp.getValues(),2).tolist()
        print(f'Current dir: {round(pathCarAngle,2)} degrees, Updated Path:')
        for i,v in enumerate(path):
            print('Vector',i+1,v)
        print("----------------------")
    
    message = robot.getName()+':'
    message+= str(round(coords.x,4))+","+str(round(coords.y,4))+","+str(round(coords.x,4))+"_"
    message+= str(round(velocity.x,4))+","+str(round(velocity.y,4))+","+str(round(velocity.z,4))+"_"
    message+= "_PathS"
    for v in path:
        message+=str(round(v.x,4))+','
        message+=str(round(v.y,4))+','
        message+=str(round(v.z,4))+'_'
    message+="PathE"
    message = bytes(message, 'utf-8')
    #print((list(message)))
    message =  struct.pack("I%ds" % (len(message),), len(message), message)
    emitter.send(message)

    while  receiv.getQueueLength() >0:
        data = receiv.getData()
        data = unpack_helper("I",data)
        transmissions.append(data)
        receiv.nextPacket()
        # (i,), data = struct.unpack("I", data[:4]), data[4:]
        # s, data = data[:i], data[i:]
        # transmissions.append(s)
    
    print(robot.getName()+f" received  at ctr {ctr}: ")
    for t in transmissions:
        print(t)
        transmissions.remove(t)
    print("______________________"*5)
        



    ctr+=1

    pass

# Enter here exit cleanup code.
