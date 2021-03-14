"""new controller."""

# You may need to import some classes of the controller module. Ex:
#  from controller import Robot, Motor, DistanceSensor
import math
from controller import Robot

# create the Robot instance.
robot = Robot()

# get the time step of the current world.
timestep = int(robot.getBasicTimeStep())

# You should insert a getDevice-like function in order to get the
# instance of a device of the robot. Something like:

#m1 = robot.getDevice('A')
#m2 = robot.getDevice('B')
w1 = robot.getDevice('pivot')

m1.setPosition(float('inf'))
m2.setPosition(float('inf'))
w1.setPosition(float('inf'))

ds = robot.getDevice('dsname')
ds.enable(timestep)

# Main loop:
# - perform simulation steps until Webots is stopping the controller
while robot.step(timestep) != -1:
    # Read the sensors:
    # Enter here functions to read sensor data, like:
    val = ds.getValue()
    #print(val)
    
    for x in range(1,9):
        time=robot.getTime()
        y= math.sin(time+x)
        w1.setPosition(y)
        print(y)
    
    
    

    # Process sensor data here.

    # Enter here functions to send actuator commands, like:
    #m1.setVelocity(15.0)
    #m2.setVelocity(15.0)
    pass

# Enter here exit cleanup code.
