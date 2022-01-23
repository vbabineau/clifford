"""new controller."""

# You may need to import some classes of the controller module. Ex:
#  from controller import Robot, Motor, DistanceSensor
import math
import decimal
import time
from controller import Accelerometer
from controller import Robot
from controller import Keyboard
from controller import Lidar
from vehicle import Driver

if __name__ == "__main__":

    robot = Robot()
    keyboard=Keyboard()
    
    keyboard.enable(50);

# get the time step of the current world.
    timestep = 64
    max_speed= 100
 
    left_motor = robot.getDevice('A1')
    right_motor = robot.getDevice('B1')
    pm = robot.getDevice('pivot')
   
    ds = robot.getDevice('LT')
    ds.enable(timestep)

    left_motor.setPosition(float('inf'))
    left_motor.setVelocity(0.0)

    right_motor.setPosition(float('inf'))
    right_motor.setVelocity(0.0)

    while robot.step(timestep)!= -1:
        val=float(round(ds.getValue(),2))
        
        if 0.07 <= val <= 0.35:
            ls=5.0
            rs=5.0
            p=0

        elif val < 0.06  : #left
            ls=1.0
            rs=5.0
            p=0.07
        elif val > 0.36  : #right
             ls=5.0
             rs=1.0
             p=-0.07
        else:
            ls=5
            rs=5
            p=0
            
        left_motor.setVelocity(ls)
        right_motor.setVelocity(rs)
        pm.setPosition(p)

        print(val)