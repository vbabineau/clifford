2021-03-07  
Each autonomous car has a destination with a predifined path.    
For our purposes these will be pregenerated we are not into making the path but how they interact withe each other.  
Each path has a color and they can stack. 
A car is only allowed to to keep moving forward on their path if it coresponds their path's color.  
The car would need to be able to 'see' all paths within their breaking distance.  
The breaking distance is based on current speed and a predefind max deceleration.  
The queue order for the color stacking is order based on speed and distance from the first path intersection.
Each car "transmits" their path within breaking distance and some for computing time.  
If a car rolls in on a path stack, its path would be added last to the queue.