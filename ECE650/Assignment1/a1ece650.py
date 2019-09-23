from __future__ import print_function, division
import sys
import re


verbose = True  # Print statements to be able to understand what is happening when


class Street:
    def __init__(self, name, lines):
        self.name = name
        self.lines = lines

    def __str__(self):
        return self.name


class Line:
    def __init__(self, name, x1, y1, x2, y2, intersections = None):
        if intersections is None:
            self.intersections = {}
        self.name = name
        self.x1 = x1
        self.x2 = x2
        self.y1 = y1
        self.y2 = y2

    def __str__(self):
        return self.name


streetList = []


def getStreetName(parsedLine):
    if parsedLine.count('"') != 2: # Check the number of apostrophes
        raise Exception('Error: The command needs exactly two apostrophes for the street name')
    strtName = re.findall(r'["][a-zA-Z ]+["]', parsedLine)  # Find the street name between apostrophes
    if not strtName:
        raise Exception("Error: The street name cannot contain characters different than alphabetical")
    if verbose:
        print("getStreetName: Street name detected is:", strtName)
    strtName = re.sub(r'["]', "", strtName[0])  # Remove the apostrophes from the item found
    return strtName

def streetCheck(parsedLine):
    command = re.findall(r'[ac][ ]["][a-zA-Z ]+["][ ][\(][-]?[0-9]+[,][-]?[0-9]+[\)]', parsedLine)  # Check if the command has the full correct formatting for a or c
    if not command:
        command = re.findall(r'[r][ ]["][a-zA-Z ]+["]', parsedLine)  # Check if the command has the full correct formatting for r
        if not command:
            raise Exception("The command formatting contains errors")
        else:
            strtName = getStreetName(parsedLine)
            strtCoords = None
    else:
        strtName = getStreetName(parsedLine)
        if parsedLine.count('(') != parsedLine.count(')'):  # Count that the number of opening parenthesis and closing parenthesis coincide
            raise Exception("Error: Number of opening and closing parenthesis does not coincide")
        strtCoords = re.findall(r'[\(][-]?[0-9]+[,][-]?[0-9]+[\)]', parsedLine) # Find all coordinates
        if len(strtCoords) != parsedLine.count('('):  # Check if the number of coordinates and number of parenthesis coincide
            raise Exception("Error: There is an error on the coordinates")
    return strtName, strtCoords


def checkStreetExistance(strtName, popStreet = False):
    strtExists = False
    if len(streetList) > 0:
        for i in range(len(streetList)):  # Iterate over the streets to find the one with the same name
            if verbose:
                print("checkStreetExistance: Trying element:", streetList[i].name)
            if streetList[i].name.lower() == strtName.lower():
                strtExists = True
                if popStreet:
                    streetList.pop(i)  # Remove street from list
                    if verbose:
                        print("checkStreetExistance: Street:", strtName, "removed")
                break
    return strtExists


def addStreet(streetName, streetCoords):
    streetCheck = checkStreetExistance(streetName, False)  # Check if there exists a street with the same name
    if streetCheck:
        raise Exception("Error: A street with that name already exists")
    # Convert street coordinates into dictionary of coordinates
    coordsDict = {}
    count = 1
    streetLines = []
    pastX = 0
    pastY = 0
    for element in streetCoords:
        strtCoord = re.sub(r'[\(][\)]', "", element)
        strtCoordX = re.findall(r'[-]?[0-9]+[,]', strtCoord)
        strtCoordX = re.sub(r'[,]', "", strtCoordX[0])
        strtCoordX = int(strtCoordX)
        strtCoordY = re.findall(r'[,][-]?[0-9]+',strtCoord)
        strtCoordY = re.sub(r'[,]', "", strtCoordY[0])
        strtCoordY = int(strtCoordY)
        coordsDict['xy' + str(count)] = [strtCoordX, strtCoordY]  # Construct dictionary
        if count > 1:
            if pastX == strtCoordX and pastY == strtCoordY:
                raise Exception("Error: There cannot be line segments with the same beginning and ending points")
            else:
                line = Line(str(count-1), pastX, pastY, strtCoordX, strtCoordY)  # Construct line object
                streetLines.append(line)
        pastX = strtCoordX
        pastY = strtCoordY
        count = count+1

    if verbose:
        print("addStreet: Printing the list of coordinates saved:")
        for keys, values in coordsDict.items():
            print(keys)
            print(values)

    # Create Street object
    strt = Street(streetName, streetLines)
    # Add street to list
    streetList.append(strt)


def intersectionDetection():
    intersectionList = {}
    vertexList = {}
    intersectionCount = 0
    edgeList = {}
    vertexDict = {}
    for i in range(len(streetList)-1):
        # Get one street
        street1 = streetList[i]
        if verbose:
            print("intersectionDetection: Comparing street 1:", street1)
        for j in range(len(street1.lines)):
            if verbose:
                print("intersectionDetection: Comparing street 1 segment", j)
            x1 = street1.lines[j].x1
            y1 = street1.lines[j].y1
            x2 = street1.lines[j].x2
            y2 = street1.lines[j].y2
            # Get the list of the rest of streets
            for k in range(i+1, len(streetList), 1):
                street2 = streetList[k]
                if verbose:
                    print("intersectionDetection: Comparing street 2:", street2)
                for l in range(len(street2.lines)):
                    if verbose:
                        print("intersectionDetection: Comparing street 2 segment", l)
                    x3 = street2.lines[l].x1
                    y3 = street2.lines[l].y1
                    x4 = street2.lines[l].x2
                    y4 = street2.lines[l].y2
                    denominator = (x1 - x2) * (y3 - y4) - (y1 - y2) * (x3 - x4)
                    if denominator != 0:  # Check if they are parallel
                        t = ((x1 - x3) * (y3 - y4) - (y1 - y3) * (x3 - x4)) / denominator
                        u = - ((x1 - x2) * (y1 - y3) - (y1 - y2) * (x1 - x3)) / denominator
                        if 0 <= t <= 1 and 0 <= u <= 1:
                            intersectionCount = intersectionCount + 1
                            xIntersection = round(x1 + t * (x2 - x1), 2)
                            yIntersection = round(y1 + t * (y2 - y1), 2)
                            intersectionString = "x" + "{0:.2f}".format(xIntersection) + "y" + "{0:.2f}".format(yIntersection)
                            vertexList["x" + "{0:.2f}".format(x1) + "y" + "{0:.2f}".format(y1)] = [x1, y1]
                            vertexList["x" + "{0:.2f}".format(x2) + "y" + "{0:.2f}".format(y2)] = [x2, y2]
                            vertexList["x" + "{0:.2f}".format(x3) + "y" + "{0:.2f}".format(y3)] = [x3, y3]
                            vertexList["x" + "{0:.2f}".format(x4) + "y" + "{0:.2f}".format(y4)] = [x4, y4]
                            intersectionList["x" + "{0:.2f}".format(xIntersection) + "y"
                                             + "{0:.2f}".format(yIntersection)] = ["intersection"]
                            street1.lines[j].intersections[intersectionString] = [xIntersection, yIntersection]
                            street2.lines[l].intersections[intersectionString] = [xIntersection, yIntersection]
                    else:
                        # Special case: check if they are collinear and share a point
                        if x1 == x3 and y1 == y3:
                            xIntersection = x1
                            yIntersection = y1
                            intersectionString = "x" + "{0:.2f}".format(xIntersection) + "y" + "{0:.2f}".format(
                                yIntersection)
                            street1.lines[j].intersections[intersectionString] = [xIntersection, yIntersection]
                            street2.lines[l].intersections[intersectionString] = [xIntersection, yIntersection]
                        elif x1 == x4 and y1 == y4:
                            xIntersection = x1
                            yIntersection = y1
                            intersectionString = "x" + "{0:.2f}".format(xIntersection) + "y" + "{0:.2f}".format(
                                yIntersection)
                            street1.lines[j].intersections[intersectionString] = [xIntersection, yIntersection]
                            street2.lines[l].intersections[intersectionString] = [xIntersection, yIntersection]
                        elif x2 == x3 and y2 == y3:
                            xIntersection = x2
                            yIntersection = y2
                            intersectionString = "x" + "{0:.2f}".format(xIntersection) + "y" + "{0:.2f}".format(
                                yIntersection)
                            street1.lines[j].intersections[intersectionString] = [xIntersection, yIntersection]
                            street2.lines[l].intersections[intersectionString] = [xIntersection, yIntersection]
                        elif x2 == x4 and y2 == y4:
                            xIntersection = x2
                            yIntersection = y2
                            intersectionString = "x" + "{0:.2f}".format(xIntersection) + "y" + "{0:.2f}".format(
                                yIntersection)
                            street1.lines[j].intersections[intersectionString] = [xIntersection, yIntersection]
                            street2.lines[l].intersections[intersectionString] = [xIntersection, yIntersection]
                            print("Missing case in intersection calculation: one segment within another") # Missing case: one segment contained within another

    vertexList = dict(vertexList.items() + intersectionList.items())  # Combine vertices
    if verbose:
        print("IntersectionDetection: Printing the list of intersections found:")
        for key in sorted(intersectionList.keys()):
            print("%s: %s" % (key, intersectionList[key]))
        print("IntersectionDetection: Printing the list of vertices found:")
        for key in sorted(vertexList.keys()):
            print("%s: %s" % (key, vertexList[key]))

    # Let's reconstruct the edges:
    for street in streetList:  # Let's iterate over every street
        for segment in street.lines:  # Iterate over every segment of each street
            if len(segment.intersections) == 0:  # Check if the segment has intersections, if not skip it
                continue
            x1 = segment.x1
            y1 = segment.y1
            x2 = segment.x2
            y2 = segment.y2

            if x2 > x1:
                for key in sorted(segment.intersections.keys()):
                    if key != "x" + "{0:.2f}".format(x1) + "y" + "{0:.2f}".format(y1):
                        edgeList["x" + "{0:.2f}".format(x1) + "y" + "{0:.2f}".format(y1) + "," + key] = []
                        x1 = segment.intersections[key][0]
                        y1 = segment.intersections[key][1]
                if x1 != x2 and y1 != y2:
                    edgeList["x" + "{0:.2f}".format(x1) + "y" + "{0:.2f}".format(y1) + "," + "x" +
                             "{0:.2f}".format(x2) + "y" + "{0:.2f}".format(y2)] = []
            elif x2 == x1:  # Segments are vertical
                if y2 > y1:
                    for key in sorted(segment.intersections.keys()):
                        if key != "x" + "{0:.2f}".format(x1) + "y" + "{0:.2f}".format(y1):
                            edgeList["x" + "{0:.2f}".format(x1) + "y" + "{0:.2f}".format(y1) + "," + key] = []
                            x1 = segment.intersections[key][0]
                            y1 = segment.intersections[key][1]
                    if x1 != x2 and y1 != y2:
                        edgeList["x" + "{0:.2f}".format(x1) + "y" + "{0:.2f}".format(y1) + "," + "x" +
                                 "{0:.2f}".format(x2) + "y" + "{0:.2f}".format(y2)] = []
                elif y2 < y1:
                    for key in reversed(sorted(segment.intersections.keys())):
                        if key != "x" + "{0:.2f}".format(x1) + "y" + "{0:.2f}".format(y1):
                            edgeList["x" + "{0:.2f}".format(x2) + "y" + "{0:.2f}".format(y2) + "," + key] = []
                            x2 = segment.intersections[key][0]
                            y2 = segment.intersections[key][1]
                    if x1 != x2 and y1 != y2:
                        edgeList["x" + "{0:.2f}".format(x2) + "y" + "{0:.2f}".format(y2) + "," + "x" +
                                 "{0:.2f}".format(x1) + "y" + "{0:.2f}".format(y1)] = []
            elif x2 < x1:
                for key in reversed(sorted(segment.intersections.keys())):
                    if key != "x" + "{0:.2f}".format(x1) + "y" + "{0:.2f}".format(y1):
                        edgeList["x" + "{0:.2f}".format(x2) + "y" + "{0:.2f}".format(y2) + "," + key] = []
                        x2 = segment.intersections[key][0]
                        y2 = segment.intersections[key][1]
                if x1 != x2 and y1 != y2:
                    edgeList["x" + "{0:.2f}".format(x2) + "y" + "{0:.2f}".format(y2) + "," + "x" +
                             "{0:.2f}".format(x1) + "y" + "{0:.2f}".format(y1)] = []
            if verbose:
                print("Sort finished")

    vertexCount = 1
    for key in edgeList.keys():
        vertex1 = re.findall(r'[x][-]?[0-9]+[\.]?[0-9]*[y][-]?[0-9]+[\.]?[0-9]*[,]', key)
        vertex1 = re.sub(r'[x,]', "", vertex1[0])
        vertex1 = re.sub(r'[y]', ",", vertex1)
        vertex2 = re.findall(r'[,][x][-]?[0-9]+[\.]?[0-9]*[y][-]?[0-9]+[\.]?[0-9]*', key)
        vertex2 = re.sub(r'[x,]', "", vertex2[0])
        vertex2 = re.sub(r'[y]', ",", vertex2)
        if vertex1 not in vertexDict.keys():
            vertexDict[vertex1] = vertexCount
            vertexCount = vertexCount + 1
        if vertex2 not in vertexDict.keys():
            vertexDict[vertex2] = vertexCount
            vertexCount = vertexCount + 1
        edgeList[key] = [str(vertexCount-2) + "," + str(vertexCount-1)]
    if verbose:
        print("IntersectionDetection: Printing the list of vertices: ")
        for value in sorted(vertexDict.values()):
            print(value)
        sortedVertexDict = sorted((value, key) for (key, value) in vertexDict.items())
        print("Sorted vertices:")
        for element in sortedVertexDict:
            print(str(element[0]) + ": " + element[1])
        print("IntersectionDetection: Printing the list of edges found:")
        #for key in sorted(edgeList.keys()):
        #    print("%s: %s" % (key, edgeList[key]))
        for value in sorted(edgeList.values()):
            print(value)
        print("done") #vertex pairs are not printing correctly, check afterwards


def checkLine(parsedLine):
    if verbose:
        print("CheckLine: Input line is: ", parsedLine)
    cmnd=re.match(r'\b[acgr]', parsedLine)  # Check if line has a command at the beginning
    if cmnd:  # If a command is found
        cmnd = cmnd.group()  # Assign the string instead of the object
        if verbose:
            print('CheckLine: Command match found:', cmnd)
    else:
        raise Exception('Error: The command needs to be one of the following options: a, c, r or g followed by a single space and no space or character before the command')
    if cmnd == 'a':
        # Shortest line that can be made is: a "a" (#,#)(#,#)
        # Less than that and any command would be incomplete
        if len(parsedLine)<16:
            raise Exception('Error: Add command too short, it cannot be a valid command')
        strtName, strtCoords = streetCheck(parsedLine)  # Call the streetCheck function
        if verbose:
            print("CheckLine: Street name is", strtName)
            print("CheckLine: Street coordinates are", strtCoords)
        addStreet(strtName, strtCoords) # Call the add street function
    elif cmnd == 'c':
        strtName, strtCoords = streetCheck(parsedLine)
        print('Change street')
    elif cmnd == 'r':
        strtName = streetCheck(parsedLine)[0]
        removeStreet(strtName)

    elif cmnd == 'g':
      print('Graph')
      graphStuff()
    else:
        raise Exception('Error: Command not in the list of possible commands')


def removeStreet(strtName):
    if verbose:
        print("removeStreet: Trying to remove", strtName)
    strtExists = checkStreetExistance(strtName, True)
    if strtExists == False:  # If street is not found
        raise Exception("Error: " + strtName + " not found on the list of streets")

def printStreetList():
    print("printStreetList: Total number of streets: ", len(streetList))
    for i in range(len(streetList)):
        print("printStreetList: Street number", i, ":", streetList[i].name)

def graphStuff():
    if streetList==[]:
        print("V = {\n\n}")
        print("E = {\n\n}")
    else:
        intersectionDetection()


def main():

    #    while True:
    #        try:
    #            if verbose:
    #                print('Please input a command: \n' )
    #            line = sys.stdin.readline()
    #            if re.match('exit', line, re.I):
    #                sys.exit(0)
    #            checkLine(line)
    #        except Exception as ex:
    #            sys.stderr.write(str(ex) + '\n')
    # DO SOMETHING
    # return(1)

    # return exit code 0 on successful termination

    counter = 0
    while True:
        if counter < 1:
            line = 'a "Weber Street" (-10,-10) (2,-1) (2,2) (5,5) (5,6) (3,8)'
            checkLine(line)
            line = 'a "King Street S" (4,2) (4,8)'
            checkLine(line)
            line = 'a "Davenport Road" (1,4) (5,8) (10,10)'
            checkLine(line)
            line = 'a "Tarnulfo Street" (6,4)(5,4)(5,6)(6,7)'
            checkLine(line)
            counter = counter+1
        if verbose:
            print('Please input a command: \n' )
        line = sys.stdin.readline()
        if re.match('exit', line, re.I):
            sys.exit(0)
        checkLine(line)
        # return exit code 0 on successful termination


if __name__ == '__main__':
    main()
