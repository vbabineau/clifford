"""obstacle_avoidance controller."""

# You may need to import some classes of the controller module. Ex:
#  from controller import Robot, Motor, DistanceSensor
from controller import Robot
from controller import Motor

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

# You should insert a getDevice-like function in order to get the instance of a device of the robot. Something like:
left_sensor = robot.getDevice('left_sensor')
right_sensor = robot.getDevice('right_sensor')
center_sensor = robot.getDevice('center_sensor')

left_sensor.enable(sensor_timestep)
right_sensor.enable(sensor_timestep)
center_sensor.enable(sensor_timestep)

leftMotor = robot.getDevice('A') #get motor pointers
rightMotor = robot.getDevice('B')
pivot = robot.getDevice('pivot')
pivot.setPosition(0)
MAX_SPEED = 1*rightMotor.getMaxVelocity() #get max speed

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

    if leftVal > rightVal:
        angle -= (leftVal - rightVal) / (50 * sensorMax)
        print("turning right")
    elif rightVal > leftVal:
        angle += (rightVal - leftVal) / (50 * sensorMax)
        print("turning left")
    else:
        angle /= 1.5

    speed += speed*0.1
    if speed > (MAX_SPEED):
        speed = (MAX_SPEED)
    if angle > 0.25:
        angle = 0.25
    elif angle < -0.25:
        angle = -0.25
    
    # Enter here functions to send actuator commands, like: motor.setPosition(10.0)
    leftMotor.setVelocity(speed)
    rightMotor.setVelocity(speed)
    avoidObstacle(angle,speed)

    print("Speed: %.2f " % (speed))
    print("Angle: %.2f " % (angle))
    print("Left distance: %.2f " % leftVal)
    print("Right distance: %.2f " % rightVal)
    print("Center distance: %.2f " % centerVal)
    
    ctr+=1
# Enter here exit cleanup code.
