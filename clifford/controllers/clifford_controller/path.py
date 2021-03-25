from vectors import Point, Vector

def createPath(startP,endP,dirVect):
    path = []
    birdsEyePath = Vector.from_points(startP,endP)
    path.append(dirVect.multiply(birdsEyePath.dot(dirVect)))
    path.append(birdsEyePath.substract(path[-1]))
    return path

def updatePath(startP,endP,dirVect,path):
    birdsEyePath = Vector.from_points(startP,endP)
    for v in path:
        if(len(path)==1):
            print()
        path.remove(v)
        mag=v.magnitude()
        pathVect = v.multiply(1/mag)
        newV = pathVect.multiply(birdsEyePath.dot(pathVect))
        if round(newV.magnitude(),2)>1:
            path.insert(0,newV)
            break
    return path

if __name__ =="__main__":
    start = Point(0.25,0.036,4.9)
    end = Point(5.4,0.036,-.25)

    path=createPath(start,end,Vector.from_list([0,0,1]))
    for i in range(0,49):
        print(updatePath(start.substract(Vector(0,0,i*.1)),end,Vector.from_list([0,0,1]),path))