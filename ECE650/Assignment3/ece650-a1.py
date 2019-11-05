#!/usr/bin/env python
from __future__ import print_function, division
import sys
import re


verbose = False  # Print statements to be able to understand what is happening and when
oneRun = False  # Do not try to catch errors or recover from an exception.
countOverlappingLines = True  # Calculate the intersections of overlapping streets

if (verbose):
    print("A1 started")

class Street:
    def __init__(self, name, lines):
        self.name = name
        self.lines = lines

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.name


class Line:
    def __init__(self, name, x1, y1, x2, y2, intersections=None):
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
    """
    Receives a text line introduced by the user and tries to extract the coordinates only
    :param parsedLine: Line input by the user and that will be analyzed to find the street name
    :return: returns the name that was found, without any special characters, as a string
    """
    if parsedLine.count('"') != 2:  # Check the number of apostrophes
        raise Exception('Error: The command needs exactly two apostrophes for the street name')
    strtName = re.search(r'["][a-zA-Z ]+["]', parsedLine).group()  # Find the street name between apostrophes
    if not strtName:
        raise Exception("Error: The street name cannot contain characters different than alphabetical and spaces")
    if verbose:
        print("getStreetName: Street name detected is:", strtName)
    strtName = re.sub(r'["]', "", strtName)  # Remove the apostrophes from the item found
    return strtName

def streetCheckName(parsedLine):
    """
    Checks if the line input by the user is as what is expected by the program and returns the street name and
     coordinates
    :param parsedLine: Line input by the user to be analyzed and interpreted
    :return: strtName: street name. strtCoords: coordinate pairs as a list a la [[x1, y1], [x2, y2]]
    """
    command = re.search(r'^[ac][ ]+["][a-zA-Z ]+["][ ]+([\(][-]?[0-9]+[,][-]?[0-9]+[\)][ ]*)+$', parsedLine)  # Check if the command has the full correct formatting for a or c
    if not command:
        command = re.search(r'^[r][ ]["][a-zA-Z ]+["]$', parsedLine)  # Check if the command has the full correct formatting for r
        if not command:
            raise Exception("Error: The command formatting contains errors")
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
        if len(strtCoords) != parsedLine.count(')'):  # Check if the number of coordinates and number of parenthesis coincide
            raise Exception("Error: There is an error on the coordinates")
        if len(strtCoords) < 2:
            raise Exception("Error: Only one coordinate was input")
    return strtName, strtCoords


def checkStreetExistence(strtName, popStreet = False):
    """
    Checks if a street exists in a list, and deletes it if the popStreet boolean is True.
    :param strtName: String with the name of the street that will be searched for.
    :param popStreet: Optional boolean that indicates if the street that will be found is to be deleted.
    :return: strtExists: Boolean that indicates if the street was found in the list of streets
    """
    strtExists = False
    if len(streetList) > 0:
        for i in range(len(streetList)):  # Iterate over the streets to find the one with the same name
            if verbose:
                print("checkStreetExistence: Trying element:", streetList[i].name)
            if streetList[i].name.lower() == strtName.lower():
                strtExists = True
                if popStreet:
                    streetList.pop(i)  # Remove street from list
                    if verbose:
                        print("checkStreetExistence: Street:", strtName, "removed")
                return strtExists
    return strtExists


def addStreet(streetName, streetCoords):
    streetCheck = checkStreetExistence(streetName, False)  # Check if there exists a street with the same name
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


def removeStreet(strtName):
    """
    Runs the checkStreetExistence function with the popStreet variable set as true, which deletes the street from the
    list
    :param strtName: Name of the street to be removed
    :return: Nothing
    """
    if verbose:
        print("removeStreet: Trying to remove", strtName)
    strtExists = checkStreetExistence(strtName, True)
    if strtExists == False:  # If street is not found
        raise Exception("Error: " + strtName + " not found on the list of streets")


def areStreetsWithinStreets(p1, p2, q1, q2):
    withinStreets = False
    if min(p1, p2) <= min(q1, q2) <= max(q1, q2) <= max(p1, p2):
        withinStreets = True
    return withinStreets


def intersectionDetection():
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
            for k in range(i + 1, len(streetList), 1):
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
                            # intersectionCount = intersectionCount + 1
                            xIntersection = round(x1 + t * (x2 - x1), 2)
                            yIntersection = round(y1 + t * (y2 - y1), 2)
                            intersectionString = "(" + "{0:.2f}".format(xIntersection) + "," + "{0:.2f}".format(yIntersection) + ")"
                            street1.lines[j].intersections[intersectionString] = [xIntersection, yIntersection]
                            street2.lines[l].intersections[intersectionString] = [xIntersection, yIntersection]

                    else:

                        # Special case in which one segment is contained within the other
                        if areStreetsWithinStreets(x1, x2, x3, x4) and areStreetsWithinStreets(y1, y2, y3, y4):
                            if countOverlappingLines:
                                # Segment x3,y3 - x4,y4 is contained within x1,y1 - x2,y2
                                xIntersection = x4
                                yIntersection = y4
                                intersectionString = "(" + "{0:.2f}".format(xIntersection) + "," + "{0:.2f}".format(
                                    yIntersection) + ")"
                                street1.lines[j].intersections[intersectionString] = [xIntersection, yIntersection]
                                street2.lines[l].intersections[intersectionString] = [xIntersection, yIntersection]
                                xIntersection = x3
                                yIntersection = y3
                                intersectionString = "(" + "{0:.2f}".format(xIntersection) + "," + "{0:.2f}".format(
                                    yIntersection) + ")"
                                street1.lines[j].intersections[intersectionString] = [xIntersection, yIntersection]
                                street2.lines[l].intersections[intersectionString] = [xIntersection, yIntersection]
                        elif areStreetsWithinStreets(x3, x4, x1, x2) and areStreetsWithinStreets(y3, y4, y1, y2):
                            if countOverlappingLines:
                                # Segment x1,y1 - x2,y2 is contained within x3,y3 - x4,y4
                                xIntersection = x1
                                yIntersection = y1
                                intersectionString = "(" + "{0:.2f}".format(xIntersection) + "," + "{0:.2f}".format(
                                    yIntersection) + ")"
                                street1.lines[j].intersections[intersectionString] = [xIntersection, yIntersection]
                                street2.lines[l].intersections[intersectionString] = [xIntersection, yIntersection]
                                xIntersection = x2
                                yIntersection = y2
                                intersectionString = "(" + "{0:.2f}".format(xIntersection) + "," + "{0:.2f}".format(
                                    yIntersection) + ")"
                                street1.lines[j].intersections[intersectionString] = [xIntersection, yIntersection]
                                street2.lines[l].intersections[intersectionString] = [xIntersection, yIntersection]

                        # Special case: check if one segment partially overlaps the other (covers collinearity)
                        elif min(x1, x2) <= x3 <= max(x1, x2) and min(y1, y2) <= y3 <= max(y1, y2):
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


def vertexCheck(comparisonKey, vertexCounter, vertexDict):
    vertexValue = None
    if comparisonKey not in vertexDict.keys():  # Check if first node is already included in the vertex list
        vertexValue = str(vertexCounter)
        vertexDict[comparisonKey] = vertexValue
        vertexCounter = vertexCounter + 1
    else:  # If it is, grab it
        vertexValue = vertexDict[comparisonKey]
    return vertexValue, vertexCounter, vertexDict


def graphConstruction():
    edgeList = {}
    vertexDict = {}
    vertexCounter = 0
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


def graphStuff():
    """
Calls the intersectionDetection function and the graphConstruction function, and then proceeds to output those results
into the required printing format
    """

    intersectionDetection()
    vertices, edges = graphConstruction()
    if len(vertices) > 0:
        verticesNumber = int(max(vertices.values())) + 1 
    else:
        verticesNumber = 0

    print("V " + str(verticesNumber)) #A3 way of printing the results
    
    edgeString = "E {"
    totalEdges = len(edges)
    printerCount = 1
    for key in sorted(edges.keys()):
        if printerCount < totalEdges:
            edgeString = edgeString + key + "," + " "
        else:
            edgeString = edgeString + key
        printerCount = printerCount + 1
    edgeString = edgeString + "}"
    print(edgeString)
    sys.stdout.flush()
    #A1 way of printing the results:
    #--First for V
    #vrtxCounter = 0
    #print("V = {")
    #for key in sorted(vertices.keys()):
    #    vrtxCounter = vrtxCounter + 1
    #    if int(vertices[key]) < 10:
    #        print("  %s:  %s" % (vertices[key], key))
    #    else:
    #        print("  %s: %s" % (vertices[key], key))
    #print("}")
    #--Now for E
    #print("E = {")
    #totalEdges = len(edges)
    #printerCount = 1
    #for key in sorted(edges.keys()):
    #    if printerCount < totalEdges:
    #        print("  " + key + ",")
    #    else:
    #        print("  " + key)
    #    printerCount = printerCount + 1
    #print("}")



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
        strtName, strtCoords = streetCheckName(parsedLine)  # Call the streetCheckName function
        if verbose:
            print("CheckLine: Street name is", strtName)
            print("CheckLine: Street coordinates are", strtCoords)
        addStreet(strtName, strtCoords) # Call the add street function
    elif cmnd == 'c':
        if verbose:
            print('Change street')
        strtName, strtCoords = streetCheckName(parsedLine)
        removeStreet(strtName)
        addStreet(strtName, strtCoords)
    elif cmnd == 'r':
        if verbose:
            print('Remove street')
        strtName = streetCheckName(parsedLine)[0]
        removeStreet(strtName)
    elif cmnd == 'g':
        if verbose:
            print('Graph')
        graphStuff()
    else:
        raise Exception('Error: Command not in the list of possible commands')


def printStreetList():
    print("printStreetList: Total number of streets: ", len(streetList))
    for i in range(len(streetList)):
        print("printStreetList: Street number", i, ":", streetList[i].name)


def main():
    if not oneRun:
        while True:
            try:
                if verbose:
                    print('Please input a command: \n')
                line = sys.stdin.readline()
                if line == '':
                    break
                checkLine(line)
            except Exception as ex:
                sys.stderr.write(str(ex) + '\n')
        sys.exit(0)
    else:
        while True:
            if verbose:
                print('Please input a command: \n')
            line = sys.stdin.readline()
            if line == '':
                break
            checkLine(line)
        if verbose:
            print("[A1]: Saw EOF")
        #sys.stderr.write("[A1]: Saw EOF")
        sys.exit(0)

    # return exit code 0 on successful termination


if __name__ == '__main__':
    main()
