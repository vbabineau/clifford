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
        path.remove(v)
        newV = dirVect.multiply(birdsEyePath.dot(dirVect))
        if round(newV.dot(dirVect),2)!=0:
            path.insert(0,newV)
            break
    return path

if __name__ =="__main__":
    start = Point(0.25,0.036,4.9)
    end = Point(5.4,0.036,-.25)

    print(createPath(start,end,Vector.from_list([0,0,1])))