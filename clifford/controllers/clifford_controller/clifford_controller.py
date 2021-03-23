"""clifford_controller controller."""

# You may need to import some classes of the controller module. Ex:
#  from controller import Robot, Motor, DistanceSensor
from controller import Robot,Motor
# create the Robot instance.
robot = Robot()
# You should insert a getDevice-like function in order to get the
# instance of a device of the robot. Something like:
#  motor = robot.getMotor('motorname')
#  ds = robot.getDistanceSensor('dsname')
#  ds.enable(timestep)
leftMotor = robot.getDevice('A')  #assigning left wheel motor A
rightMotor = robot.getDevice('B') #assigning right wheel motor B 

TIME_STEP = int(robot.getBasicTimeStep())
MAX_SPEED = leftMotor.getMaxVelocity() #The robot will cap out at its max velocity:(

leftMotor.setPosition(float('inf'))#sets the servo? to infinity so it never stops
rightMotor.setPosition(float('inf'))
# Main loop:
# - perform simulation steps until Webots is stopping the controller
while robot.step(TIME_STEP) != -1: #infinite loop cause TIME_STEP never changing
    # Read the sensors:
    # Enter here functions to read sensor data, like:
    #  val = ds.getValue()

    # Process sensor data here.
    leftMotor.setVelocity(0.25*MAX_SPEED)
    rightMotor.setVelocity(MAX_SPEED)

    # Enter here functions to send actuator commands, like:
    #  motor.setPosition(10.0)
    pass

# Enter here exit cleanup code.
