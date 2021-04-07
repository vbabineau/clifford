from vectors import Point, Vector
import struct
import numpy as np

def createPath(startP,endP,dirVect):
    path = []
    birdsEyePath = Vector.from_points(startP,endP)

    birdsEyePath.y = 0

    if birdsEyePath.magnitude()<1:
        raise ValueError

    elif birdsEyePath.angle(dirVect)%180 == 0:
        path.append(birdsEyePath)
    else:
        path.append(dirVect.multiply(birdsEyePath.dot(dirVect)))
        vec = [birdsEyePath.x-path[-1].x,birdsEyePath.y-path[-1].y,birdsEyePath.z-path[-1].z]
        path.append(Vector.from_list(vec))
    return path

def updatePath(startP,endP,dirVect,path):
    birdsEyePath = (Vector.from_points(startP,endP))
    birdsEyePath.y = 0
    if birdsEyePath.angle(dirVect)%180 == 0:
        path.pop(-1)
        path.append(birdsEyePath)
    else:
        for v in path:
            path.remove(v)
            mag=v.magnitude()
            pathVect = v.multiply(1/mag)
            newV = pathVect.multiply(abs(birdsEyePath.dot(pathVect)))
            if abs(round(newV.magnitude(),2))>.6:
                path.insert(0,newV)
                break
    return path

def vecToSeg(startP, v):
    '''Takes a start point and vector and returns the segment it forms '''
    endP=Point(startP.x+v.x,startP.y+v.y,startP.z+v.z)

    return [startP,endP]


# Formulas taken from to check if segments intersect https://stackoverflow.com/questions/3838329/how-can-i-check-if-two-segments-intersect
def ccw(A,B,C):
    return (C.z-A.z) * (B.x-A.x) > (B.z-A.z) * (C.x-A.x)

# Return true if line segments AB and CD intersect
def intersect(A,B,C,D):
    return ccw(A,C,D) != ccw(B,C,D) and ccw(A,B,C) != ccw(A,B,D)

#https://gist.github.com/hellpanderrr/a6c30179f64bb1b13b85
def seg_intersect(A,B,C,D) :
    da = Vector(B.x-A.x,0,B.z-A.z)
    db = Vector(D.x-C.x,0,D.z-C.z)
    dp = Vector(B.x-D.x,0,B.z-D.z)
    dap = Vector(-da.z,0,da.x)
    denom = dap.dot(db)
    num = dap.dot(dp)
    ptoV= Vector(C.x,C.y,C.z)
    print(db,da)
    print(dap)

    if db.perpendicular(da):
        x3 = (db.multiply(num / denom).sum(ptoV).x)
        z3 = (db.multiply(num / denom).sum(ptoV).z)
    elif da.parallel(db):
        print("Collinear Path")
        return False

    p1 = [A.x,A.z,B.x,B.z]
    p2 = [C.x,C.z,D.x,D.z]
    if (min(p1[0],p1[2])<x3 and x3<max(p1[0],p1[2]) ) and( min(p1[1],p1[3]) < z3 and z3 <max(p1[1],p1[3])):
        if(min(p2[0],p2[2])<x3 and x3<max(p2[0],p2[2]) ) and( min(p2[1],p2[3]) < z3 and z3 <max(p2[1],p2[3])):
            return x3,z3
    else:
        return False

def unit_vector(vector):
    """ Returns the unit vector of the vector.  """
    return vector / np.linalg.norm(vector)

def angle_between(v1, v2):
    """ Returns the angle in radians between vectors 'v1' and 'v2'::

            >>> angle_between((1, 0, 0), (0, 1, 0))
            1.5707963267948966
            >>> angle_between((1, 0, 0), (1, 0, 0))
            0.0
            >>> angle_between((1, 0, 0), (-1, 0, 0))
            3.141592653589793
    """
    v1_u = unit_vector(v1)
    v2_u = unit_vector(v2)
    return np.arccos(np.clip(np.dot(v1_u, v2_u), -1.0, 1.0))
if __name__ =="__main__":
    start = Point(0.2919,0.0654,4.8651)  
    end = Point(5.4, 0.0654, -0.25)

    path=createPath(start,end,Vector.from_list([1,0,0]))
    print(path)
    up=(updatePath(start,end,Vector.from_list([1,-0.0,-0.0]),path))
    print(up)