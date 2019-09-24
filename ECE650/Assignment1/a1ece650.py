from __future__ import print_function, division
import sys
import re


verbose = False  # Print statements to be able to understand what is happening when
oneRun = False

class Street:
    def __init__(self, name, lines):
        self.name = name
        self.lines = lines

    def __str__(self):
        return self.name

    def __repr__(self):
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

    def __repr__(self):
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
            raise Exception("Error: The command formatting contains errors, check if the coordinates are missing")
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
    # intersectionList = {}
    # vertexList = {}
    #intersectionCount = 0

    # First delete any previous intersections
    for street in streetList:
        for line in street.lines:
            line.intersections.clear()

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
                    collinear = False
                    x3 = street2.lines[l].x1
                    y3 = street2.lines[l].y1
                    x4 = street2.lines[l].x2
                    y4 = street2.lines[l].y2
                    denominator = (x1 - x2) * (y3 - y4) - (y1 - y2) * (x3 - x4)
                    if denominator != 0:  # Check if they are parallel
                        t = ((x1 - x3) * (y3 - y4) - (y1 - y3) * (x3 - x4)) / denominator
                        u = - ((x1 - x2) * (y1 - y3) - (y1 - y2) * (x1 - x3)) / denominator
                        if 0 <= t <= 1 and 0 <= u <= 1:
                            # intersectionCount = intersectionCount + 1
                            xIntersection = round(x1 + t * (x2 - x1), 2)
                            yIntersection = round(y1 + t * (y2 - y1), 2)
                            intersectionString = "(" + "{0:.2f}".format(xIntersection) + "," + "{0:.2f}".format(yIntersection) + ")"
                            # vertexList["x" + "{0:.2f}".format(x1) + "y" + "{0:.2f}".format(y1)] = [x1, y1]
                            # vertexList["x" + "{0:.2f}".format(x2) + "y" + "{0:.2f}".format(y2)] = [x2, y2]
                            # vertexList["x" + "{0:.2f}".format(x3) + "y" + "{0:.2f}".format(y3)] = [x3, y3]
                            # vertexList["x" + "{0:.2f}".format(x4) + "y" + "{0:.2f}".format(y4)] = [x4, y4]
                            # intersectionList["x" + "{0:.2f}".format(xIntersection) + "y"
                            #                  + "{0:.2f}".format(yIntersection)] = ["intersection"]
                            street1.lines[j].intersections[intersectionString] = [xIntersection, yIntersection]
                            street2.lines[l].intersections[intersectionString] = [xIntersection, yIntersection]
                    else:
                        # Special case: check if they are collinear and share a point
                        # if x1 == x3 and y1 == y3:
                        #     xIntersection = x1
                        #     yIntersection = y1
                        #     collinear = True
                        # elif x1 == x4 and y1 == y4:
                        #     xIntersection = x1
                        #     yIntersection = y1
                        #     collinear = True
                        # elif x2 == x3 and y2 == y3:
                        #     xIntersection = x2
                        #     yIntersection = y2
                        #     collinear = True
                        # elif x2 == x4 and y2 == y4:
                        #     xIntersection = x2
                        #     yIntersection = y2
                        #     collinear = True
                        # if collinear:
                        #     intersectionString = "(" + "{0:.2f}".format(xIntersection) + "," + "{0:.2f}".format(
                        #         yIntersection) + ")"
                        #     street1.lines[j].intersections[intersectionString] = [xIntersection, yIntersection]
                        #     street2.lines[l].intersections[intersectionString] = [xIntersection, yIntersection]

                        # Special case: check if one segment partially contains the other (covers collinearity)
                        if min(x1, x2) <= x3 <= max(x1, x2) and min(y1, y2) <= y3 <= max(y1, y2):
                            xIntersection = x3
                            yIntersection = y3
                            intersectionString = "(" + "{0:.2f}".format(xIntersection) + "," + "{0:.2f}".format(
                                yIntersection) + ")"
                            street1.lines[j].intersections[intersectionString] = [xIntersection, yIntersection]
                            street2.lines[l].intersections[intersectionString] = [xIntersection, yIntersection]
                        elif min(x1, x2) <= x4 <= max(x1, x2) and min(y1, y2) <= y4 <= max(y1, y2):
                            xIntersection = x4
                            yIntersection = y4
                            intersectionString = "(" + "{0:.2f}".format(xIntersection) + "," + "{0:.2f}".format(
                                yIntersection) + ")"
                            street1.lines[j].intersections[intersectionString] = [xIntersection, yIntersection]
                            street2.lines[l].intersections[intersectionString] = [xIntersection, yIntersection]
                    print("Missing case in intersection calculation: one segment within another")  # Missing case: one segment contained within another

    # if verbose:
    #     print("IntersectionDetection: Printing the list of intersections found:")
    #     for key in sorted(intersectionList.keys()):
    #         print("%s: %s" % (key, intersectionList[key]))
    #     print("IntersectionDetection: Printing the list of vertices found:")
    #     for key in sorted(vertexList.keys()):
    #         print("%s: %s" % (key, vertexList[key]))





def vertexCheck(comparisonKey, vertexCounter, vertexDict):
    vertexValue = None
    if comparisonKey not in vertexDict.keys():  # Check if first node is already included in the vertex list
        vertexValue = "V" + str(vertexCounter)
        vertexDict[comparisonKey] = vertexValue
        vertexCounter = vertexCounter + 1
    else:  # If it is, grab it
        vertexValue = vertexDict[comparisonKey]
    return vertexValue, vertexCounter, vertexDict


def graphConstruction():
    edgeList = {}
    vertexDict = {}
    vertexCounter = 1
    # Let's reconstruct the edges:
    for street in streetList:  # Let's iterate over every street
        for segment in street.lines:  # Iterate over every segment of each street
            if len(segment.intersections) == 0:  # Check if the segment has intersections, if not skip it
                continue
            x1 = float(segment.x1)
            y1 = float(segment.y1)
            x2 = float(segment.x2)
            y2 = float(segment.y2)

            sortNeeded = False
            reverseSegment = False

            if x2 > x1:
                sortNeeded = True
            elif x2 == x1:  # Segments are vertical
                if y2 > y1:
                    sortNeeded = True
                elif y2 < y1:
                    sortNeeded = True
                    reverseSegment = True
            elif x2 < x1:
                sortNeeded = True
                reverseSegment = True
            # Falta que el sorting sea hecho con respecto a los valores numericos, no al string

            segmentIntersections = sorted(segment.intersections.values(), key=lambda tup: (tup[0], tup[1]))

            if sortNeeded and not reverseSegment:
                for element in segmentIntersections:
                    key = "(" + "{0:.2f}".format(element[0]) + "," + "{0:.2f}".format(element[1]) + ")"
                    comparisonKey = "(" + "{0:.2f}".format(x1) + "," + "{0:.2f}".format(y1) + ")"
                    vertexValue, vertexCounter, vertexDict = vertexCheck(comparisonKey, vertexCounter, vertexDict)
                    vertexValue2, vertexCounter, vertexDict = vertexCheck(key, vertexCounter, vertexDict)

                    if key != comparisonKey: # If coordinate pair is not the same as the intersection being analyzed, add edge
                        edgeList["<" + vertexValue + "," + vertexValue2 + ">"] = []
                        # Change coordinate pair being analyzed for just analyzed intersection coordinates:
                        x1 = segment.intersections[key][0]
                        y1 = segment.intersections[key][1]
                if x1 != x2 or y1 != y2:  # If intersection coordinates and final coordinates are not the same:
                    comparisonKey = "(" + "{0:.2f}".format(x1) + "," + "{0:.2f}".format(y1) + ")"
                    vertexValue, vertexCounter, vertexDict = vertexCheck(comparisonKey, vertexCounter, vertexDict)

                    comparisonKey = "(" + "{0:.2f}".format(x2) + "," + "{0:.2f}".format(y2) + ")"
                    vertexValue2, vertexCounter, vertexDict = vertexCheck(comparisonKey, vertexCounter, vertexDict)
                    edgeList["<" + vertexValue + "," + vertexValue2+ ">"] = []

            elif sortNeeded and reverseSegment:
                for element in segmentIntersections:
                    key = "(" + "{0:.2f}".format(element[0]) + "," + "{0:.2f}".format(element[1]) + ")"
                    comparisonKey = "(" + "{0:.2f}".format(x2) + "," + "{0:.2f}".format(y2) + ")"
                    vertexValue, vertexCounter, vertexDict = vertexCheck(comparisonKey, vertexCounter, vertexDict)
                    vertexValue2, vertexCounter, vertexDict = vertexCheck(key, vertexCounter, vertexDict)

                    if key != comparisonKey:
                        edgeList["<" + vertexValue + "," + vertexValue2 + ">"] = []
                        x2 = segment.intersections[key][0]
                        y2 = segment.intersections[key][1]
                if x1 != x2 or y1 != y2:  # If intersection coordinates and final coordinates are not the same:
                    comparisonKey = "(" + "{0:.2f}".format(x2) + "," + "{0:.2f}".format(y2) + ")"
                    vertexValue, vertexCounter, vertexDict = vertexCheck(comparisonKey, vertexCounter, vertexDict)

                    comparisonKey = "(" + "{0:.2f}".format(x1) + "," + "{0:.2f}".format(y1) + ")"
                    vertexValue2, vertexCounter, vertexDict = vertexCheck(comparisonKey, vertexCounter, vertexDict)
                    edgeList["<" + vertexValue + "," + vertexValue2 + ">"] = []

    if verbose:
        print("IntersectionDetection: Printing the list of vertices found:")
        for key in sorted(vertexDict.keys()):
            print("%s: %s" % (key, vertexDict[key]))
        print("IntersectionDetection: Printing the list of vertices found:")
        for key in sorted(edgeList.keys()):
            print("%s: %s" % (key, edgeList[key]))
    return vertexDict, edgeList


def checkLine(parsedLine):
    if verbose:
        print("CheckLine: Input line is: ", parsedLine)
    cmnd = re.match(r'\b[acgr]', parsedLine)  # Check if line has a command at the beginning
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
        if verbose:
            print('Change street')
        strtName, strtCoords = streetCheck(parsedLine)
        removeStreet(strtName)
        addStreet(strtName, strtCoords)
    elif cmnd == 'r':
        if verbose:
            print('Remove street')
        strtName = streetCheck(parsedLine)[0]
        removeStreet(strtName)
    elif cmnd == 'g':
        if verbose:
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
    """
Calls the intersectionDetection function and the graphConstruction function, and then proceeds to output those results
into the required printing format
    """
    intersectionDetection()
    vertices, edges = graphConstruction()
    print("V = {")
    for key in sorted(vertices.keys()):
        print("%s: %s" % (vertices[key], key))
    print("}")
    print("E = {")
    totalEdges = len(edges)
    printerCount = 1
    for key in sorted(edges.keys()):
        if printerCount < totalEdges:
            print(key + ",")
        else:
            print(key)
        printerCount = printerCount + 1
    print("}")


def main():
    if not oneRun:
        while True:
            try:
                if verbose:
                    print('Please input a command: \n' )
                line = sys.stdin.readline()
                if line == '':
                    break
                #    sys.exit(0)
                checkLine(line)
            except Exception as ex:
                sys.stderr.write(str(ex) + '\n')
        sys.exit(0)
    else:
        while True:
            if verbose:
                print('Please input a command: \n' )
            line = sys.stdin.readline()
            if line == '':
                break
            #    sys.exit(0)
            checkLine(line)
        sys.exit(0)

    # return exit code 0 on successful termination


if __name__ == '__main__':
    main()
