# 2021-03-07  
* Each autonomous car has a destination with a predifined path.    
* For our purposes these will be pregenerated we are not into making the path but how they interact withe each other.  
* Each path has a color and they can stack. 
* A car is only allowed to to keep moving forward on their path if it coresponds their path's color.  
* The car would need to be able to 'see' all paths within their breaking distance.  
* The breaking distance is based on current speed and a predefind max deceleration.  
* The queue order for the color stacking is order based on speed and di stance from the first path intersection.
* Each car "transmits" their path within breaking distance and some for computing time.  
* If a car rolls in on a path stack, its path would be added last to the queue.

# 2021-03-13  
* Use vectors to map out the paths as they're lightweight and easily comunnicable
* For coordination use some kind of high bandwidth wifi network between cars, that has reach beyond the maximum speed breaking distance.
* Maybe add some kind of indication on robots when they're in a stack (light)
* Work on turn handling

# 2021-03-24  
* Protocol for communicating information as strings, support for multiple cars may be tricky
* Turn radius support
*   
