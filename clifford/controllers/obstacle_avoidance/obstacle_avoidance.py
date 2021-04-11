"""obstacle_avoidance controller."""

# You may need to import some classes of the controller module. Ex:
#  from controller import Robot, Motor, DistanceSensor
from controller import Robot
from controller import Motor
import math

def getBearingAngle(north):
    rad = math.atan2(north[0],north[2])
    if rad<0:
        rad += 2*math.pi
    return rad

def avoidObstacle(pivotAngle,velocity):
    ratio = (1-abs(pivotAngle)/1.57)
    if (pivotAngle>0):
        pivot.setPosition(pivotAngle)
        rightMotor.setVelocity(velocity)
        leftMotor.setVelocity((ratio)* velocity)
    else:
        pivot.setPosition(pivotAngle)
        leftMotor.setVelocity(velocity)
        rightMotor.setVelocity((ratio)* velocity)

# create the Robot instance.
robot = Robot()

# get the time step of the current world.
timestep = int(robot.getBasicTimeStep())
sensor_timestep = 4*timestep
sensorMax = 1000
laneSensorMax = 0.9
safeDistance = 50
xAngle = 1

# You should insert a getDevice-like function in order to get the instance of a device of the robot. Something like:
left_sensor = robot.getDevice('left_sensor')
right_sensor = robot.getDevice('right_sensor')
center_sensor = robot.getDevice('center_sensor')
lane_sensor = robot.getDevice('lane_sensor')
compass = robot.getDevice ('compass')

left_sensor.enable(sensor_timestep)
right_sensor.enable(sensor_timestep)
center_sensor.enable(sensor_timestep)
lane_sensor.enable(sensor_timestep)
compass.enable(sensor_timestep)

leftMotor = robot.getDevice('A') #get motor pointers
rightMotor = robot.getDevice('B')
pivot = robot.getDevice('pivot')
pivot.setPosition(0)
MAX_SPEED = 0.5*rightMotor.getMaxVelocity() #get max speed

speed = 0.1*MAX_SPEED
#Initial Conditions?
leftMotor.setPosition(float('inf'))
rightMotor.setPosition(float('inf'))
leftMotor.setVelocity(speed)
rightMotor.setVelocity(speed)
angle = 0
ctr = 0

# Main loop:
while robot.step(timestep) != -1:
    # Read the sensors:
    leftVal = left_sensor.getValue()
    rightVal = right_sensor.getValue()
    centerVal = center_sensor.getValue()
    laneVal = float(round(lane_sensor.getValue(),2))
    direction = compass.getValues()
    bearing = getBearingAngle(direction)
    # Distance Sensor Values:
        # 1000: 0cm
        # 800:  12cm
        # 600:  24cm
        # 400:  36cm
        # 200:  48cm
        # 0:    60cm
    
    if centerVal > 200 and centerVal < 400:
        speed -= (0.01 * speed)
    elif centerVal > 600 and centerVal < 800:
        speed /= 1.01

    if rightVal > safeDistance and leftVal > safeDistance:
        #print("STOOOOOOOOOOOOOOOOOOOP")
        speed /= 1.1
        xAngle = 2 + (max(rightVal,leftVal))/(25*sensorMax)
    else:
        xAngle = 1

    if leftVal > rightVal:
        angle -= xAngle*(leftVal - rightVal) / (25 * sensorMax)
        #print("turning right")
    elif rightVal > leftVal:
        angle += xAngle*(rightVal - leftVal) / (25 * sensorMax)
        #print("turning left")
    else:
        # if ctr>5 and 3.13<bearing<3.17:
        #     angle = 0
        if ctr>5 and bearing < 3.15:
            angle = -0.14*(abs(3.15-bearing))
        elif ctr>5 and bearing > 3.15:
            angle = 0.14*(abs(3.15-bearing))
        # elif ctr>5 and 3.13<bearing<3.17:
        #     angle = 0
        #     #angle /= 1.5

    if (ctr>5 and round(rightVal) == 0 and round(leftVal) == 0):
        if 0.07 <= laneVal <= 0.35:
            angle = angle
            #print("correct distance")
        elif laneVal < 0.06: #left
            angle = 0.08*(1.75+abs(0.05-laneVal))
            #angle += (laneVal)/(1 * laneSensorMax)
            #print("adjusting left")
        elif laneVal > 0.36: #right
            angle = -0.08*(1.75+abs(0.37-laneVal))
            #angle -= (laneVal)/(1 * laneSensorMax)
            #print("adjusting right")

    speed += speed*0.1
    if speed > (MAX_SPEED):
        speed = (MAX_SPEED)
    if angle > (0.25*xAngle):
        angle = 0.25*xAngle
    elif angle < -(0.25*xAngle):
        angle = -0.25*xAngle
    
    # Enter here functions to send actuator commands, like: motor.setPosition(10.0)
    leftMotor.setVelocity(speed)
    rightMotor.setVelocity(speed)
    avoidObstacle(angle,speed)

    print("Bearing in rad: %.2f" % bearing)
    print("Speed: %.2f " % (speed))
    print("Angle: %.2f " % (angle))
    print("Left distance: %.2f " % leftVal)
    print("Right distance: %.2f " % rightVal)
    print("Center distance: %.2f " % centerVal)
    print("Lane distance: %.2f " % laneVal)
    
    ctr+=1
# Enter here exit cleanup code.
