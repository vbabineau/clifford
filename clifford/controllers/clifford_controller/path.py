from vectors import Point, Vector

def createPath(startP,endP,dirVect):
    path = []
    birdsEyePath = Vector.from_points(startP,endP)
    birdsEyePath.y = 0
    if birdsEyePath.angle(dirVect)%180 == 0:
        path.append(birdsEyePath)
    else:
        path.append(dirVect.multiply(birdsEyePath.dot(dirVect)))
        path.append(birdsEyePath.substract(path[-1]))
    return path

def updatePath(startP,endP,dirVect,path):
    birdsEyePath = (Vector.from_points(startP,endP))
    birdsEyePath.y = 0
    if birdsEyePath.angle(dirVect)%180 == 0:
        path.pop(-1)
        path.append(birdsEyePath)
    else:
        for v in path:
            if(len(path)==1):
                print()
            path.remove(v)
            mag=v.magnitude()
            pathVect = v.multiply(1/mag)
            newV = pathVect.multiply(abs(birdsEyePath.dot(pathVect)))
            if round(newV.magnitude(),2)>1:
                path.insert(0,newV)
                break
    return path

if __name__ =="__main__":
    start = Point(-5.4, 0.1362, -0.25)  
    end = Point(5.4, 0.1362, -0.25)

    path=createPath(start,end,Vector.from_list([1,0,0]))
    for i in range(0,108):
        start.x=start.x+.1*i
        up=(updatePath(start,end,Vector.from_list([1,-0.0,-0.0]),path))
        for v in up:
            print(v)
        print("________________________________")