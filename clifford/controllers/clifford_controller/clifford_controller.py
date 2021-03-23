"""clifford_controller controller."""

# You may need to import some classes of the controller module. Ex:
#  from controller import Robot, Motor, DistanceSensor
from controller import Robot,Motor
from vectors import Point, Vector
import random


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



#important variables
speed = MAX_SPEED*random.random() #Sets speed to a random fraction of the max
dirVect = comp.getValues() #normalized direction vector
coords = Point.from_list(gps.getValues())      #coordinates
velocity = Vector(dirVect[0]*speed,dirVect[1]*speed,dirVect[2]*speed)        #Velocity vector
destination =   
#Initial Conditions?
leftMotor.setPosition(float('inf'))#sets the servo? to infinity so it never stops
rightMotor.setPosition(float('inf'))
leftMotor.setVelocity(1* MAX_SPEED)
rightMotor.setVelocity(1* MAX_SPEED)

print(robot.getCustomData)


# Main loop:
# - perform simulation steps until Webots is stopping the controller
while robot.step(TIME_STEP) != -1: #infinite loop cause TIME_STEP never changing
    # Read the sensors:
    coords = Point.from_list(gps.getValues())  
    #print(f"X:{round(x*100,1)} cm\nY:{round(y*100,1)} cm\nZ:{round(z*100,1)} cm")
   
    #for right now we only send in the position and velocity
    emitter.send(coords,velocity)
    #eventually we'd add the path
    # Process sensor data here.

    # Enter here functions to send actuator commands, like:
    pass

# Enter here exit cleanup code.
