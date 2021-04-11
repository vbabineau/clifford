from vectors import Point, Vector
from matplotlib import pyplot as plt
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
    try:
        if birdsEyePath.angle(dirVect)%180 == 0:
            path.pop(-1)
            path.append(birdsEyePath)
        else:
            for v in path:
                path.remove(v)
                mag=v.magnitude()
                pathVect = v.multiply(1/mag)
                newV = pathVect.multiply(abs(birdsEyePath.dot(pathVect)))
                if abs(round(newV.magnitude(),2))>.65:
                    path.insert(0,newV)
                    break
    except ValueError:
        path.pop(-1)
        path.append(birdsEyePath)
    return path

def vecToSeg(startP, v):
    '''Takes a start point and vector and returns the segment it forms '''
    endP=Point(startP.x+v.x,startP.y+v.y,startP.z+v.z)

    return [startP,endP]

# Return true if line segments AB and CD intersect
def intersect(A,B,C,D):

    maxX = min(max(A.x,B.x),max(C.x,D.x))
    maxZ = min(max(A.z,B.z),max(C.z,D.z))
    minX = max(min(A.x,B.x),min(C.x,D.x))
    minZ = max(min(A.z,B.z),min(C.z,D.z))
    if(minX==maxX and minZ==maxZ):
        return[(round(minX,1),round(minZ,1)) ]#point touching
    Ix=[minX,maxX]
    Iz=[minZ,maxZ]

    if (B.x-A.x)!=0 and (D.x-C.x)!=0:
        slopeA = (B.z-A.z)/(B.x-A.x)
        slopeC = (D.z-C.z)/(D.x-C.x)
    elif(B.x-A.x)!=0:
        slopeA = (B.z-A.z)/(B.x-A.x)
        slopeC = None
    elif(D.x-C.x)!=0:
        slopeC = (D.z-C.z)/(D.x-C.x)
        slopeA = None
    else:
        slopeA = None
        slopeC = None

    if slopeA == slopeC:
        #parrallel  4r 
        if slopeA==None and (max(A.z,B.z)>=min(C.z,D.z) or max(C.z,D.z)>=min(A.z,B.z)) and (A.x==C.x):
            if (A.x,Iz[0])==(D.x,Iz[1]):
                return [(A.x,max(min(A.z,B.z),min(C.z,D.z))),(A.x,max(max(A.z,B.z),max(C.z,D.z)))]
            else:
                return [(round(A.x,1),round(Iz[0],1)),(round(A.x,1),round(Iz[1],1))]
        elif slopeA==0 and (A.z==C.z) and (max(A.x,B.x)>=min(C.x,D.x) or max(C.x,D.x)>=min(A.x,B.x)):
            if (Ix[0],A.z)==(Ix[1],D.z):
                return [(max(min(A.x,B.x),min(C.x,D.x)),A.x),(max(max(A.x,B.x),max(C.x,D.x)),A.z)]
            else:
                return [(round(Ix[0],1),round(A.z,1)),(round(Ix[1],1),round(A.z,1))]
        else: #parrallel non-touching
            return False
    return False#not parralel not touching



#https://gist.github.com/hellpanderrr/a6c30179f64bb1b13b85
def plot_intersect(A,B,C,D) :
    arr = np.array([A.to_2dlist(),B.to_2dlist(),C.to_2dlist(),D.to_2dlist()])
    plt.xlim(-6,6)
    plt.ylim(6,-6)

    plt.plot(arr[:2,0],arr[:2,1])
    plt.plot(arr[2:,0],arr[2:,1])
    plt.pause(1)
    plt.close()

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
    start = Point(0.25,0.036,4.9)
    end = Point(5.4,0.036,-.25)
    path=createPath(start,end,Vector.from_list([1,0,0]))
    print(path)
    up=(updatePath(start,end,Vector.from_list([1,-0.0,-0.0]),path))
    print(up)