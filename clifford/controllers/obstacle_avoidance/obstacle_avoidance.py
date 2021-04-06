"""obstacle_avoidance controller."""

# You may need to import some classes of the controller module. Ex:
#  from controller import Robot, Motor, DistanceSensor
from controller import Robot
from controller import Motor

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
MAX_SPEED = 0.25*rightMotor.getMaxVelocity() #get max speed

speed = 0.1*MAX_SPEED
#Initial Conditions?
leftMotor.setPosition(float('inf'))
rightMotor.setPosition(float('inf'))
leftMotor.setVelocity(speed)
rightMotor.setVelocity(speed)

# Main loop:
# - perform simulation steps until Webots is stopping the controller
while robot.step(timestep) != -1:
    # Read the sensors:
    leftVal = left_sensor.getValue()
    rightVal = right_sensor.getValue()
    centerVal = center_sensor.getValue()

    # Distance Sensor Values:
    # 1000: 60cm
    # 800:  48cm
    # 600:  36cm
    # 400:  24cm
    # 200:  12cm
    # 0:    0cm
    
    if centerVal > 800 and centerVal < 1000:
        speed = (0.01 * speed)
    elif centerVal > 400 and centerVal < 800:
        speed = 0

    speed += speed*0.01
    if speed > (MAX_SPEED):
        speed = (MAX_SPEED)
    
    # Enter here functions to send actuator commands, like: motor.setPosition(10.0)
    leftMotor.setVelocity(speed)
    rightMotor.setVelocity(speed)
    print("Speed: %.1f " % (speed))
    print("Left distance: %.1f " % leftVal)
    print("Right distance: %.1f " % rightVal)
    print("Center distance: %.1f " % centerVal)
    

# Enter here exit cleanup code.
