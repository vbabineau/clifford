"""clifford_controller controller."""

# You may need to import some classes of the controller module. Ex:
#  from controller import Robot, Motor, DistanceSensor
from controller import Robot,Motor
from vectors import Point, Vector

from path import createPath, updatePath
import random
import struct
import numpy as np

TIME_STEP = 64 #time in ms


#Create Robot
robot = Robot()

leftMotor = robot.getDevice('A') #get motor pointers


rightMotor = robot.getDevice('B')

MAX_SPEED = rightMotor.getMaxVelocity() #get max speed

gps = robot.getDevice('gps') # get gps
gps.enable(TIME_STEP) # Enable gps

comp = robot.getDevice('compass') #get compasss
comp.enable(TIME_STEP)

emitter= robot.getDevice('emitter')
#This should be changed in terms of breaking time
emitter.setRange(MAX_SPEED*1000*TIME_STEP)
emitter.setChannel(1)

#Start and end Points
startPoints = [Point(0.25,0.036,4.9),Point(5.4,0.036,-.75),Point(-5.4,0.036,-.25)]
endPoints = [Point(-0.25,0.036,4.9),Point(5.4,0.036,-.25),Point(-5.4,0.036,-.75)]

#Initial Conditions?
leftMotor.setPosition(float('inf'))#sets the servo? to infinity so it never stops
rightMotor.setPosition(float('inf'))
leftMotor.setVelocity(1* MAX_SPEED)
rightMotor.setVelocity(1* MAX_SPEED)


speed = MAX_SPEED*random.random() #Sets speed to a random fraction of the max
dirVect = comp.getValues() #normalized direction vector
coords = Point.from_list(gps.getValues())      #coordinates
velocity = Vector(dirVect[0]*speed,dirVect[1]*speed,dirVect[2]*speed)        #Velocity vector
destination = endPoints[2] #random.randrange(0,2,1)

ctr = 0

#path = createPath(coords,destination,dirVect)
# Main loop:
# - perform simulation steps until Webots is stopping the controller
while robot.step(TIME_STEP) != -1: #infinite loop cause TIME_STEP never changing
    
    dirVect = np.round(comp.getValues(),2).tolist()
    coords = Point.from_list(gps.getValues())
    velocity = Vector(dirVect[0]*speed,dirVect[1]*speed,dirVect[2]*speed)

    if ctr == 0: # first iteration we create a path
        path = createPath(coords,destination, Vector.from_list(dirVect) )
    else:
        path = updatePath(coords,destination, Vector.from_list(dirVect),path)

    if ctr%16==0:
        dirVect = np.round(comp.getValues(),2).tolist()
        print(dirVect)
        for i,v in enumerate(path):
            print('Vector',i+1,v)
        print("----------------------")
    # Read the sensors:
    #print(f"X:{round(x*100,1)} cm\nY:{round(y*100,1)} cm\nZ:{round(z*100,1)} cm")
    #message = struct.pack([coords,velocity])
    #emitter.send(message)
    #for right now we only send in the position and velocity
    

    #eventually we'd add the path
    # Process sensor data here.

    # Enter here functions to send actuator commands, like:

    ctr+=1

    pass

# Enter here exit cleanup code.
