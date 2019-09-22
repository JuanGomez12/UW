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
    def __init__(self, name, x1, y1, x2, y2):
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
    if strtName == []:
        raise Exception("Error: The street name cannot contain characters different than alphabetical")
    if verbose:
        print("getStreetName: Street name detected is:", strtName)
    strtName = re.sub(r'["]',"",strtName[0]) # Remove the apostrophes from the item found
    return strtName

def streetCheck(parsedLine):
    command = re.findall(r'[ac][ ]["][a-zA-Z ]+["][ ][\(][-]?[0-9]+[,][-]?[0-9]+[\)]', parsedLine)  # Check if the command has the full correct formatting for a or c
    if command == []:
        command = re.findall(r'[r][ ]["][a-zA-Z ]+["]', parsedLine)  # Check if the command has the full correct formatting for r
        if command == []:
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
        strtCoordX = re.findall(r'[-]?[0-9]+[,]',strtCoord)
        strtCoordX = re.sub(r'[,]',"",strtCoordX[0])
        strtCoordX = int(strtCoordX)
        strtCoordY = re.findall(r'[,][-]?[0-9]+',strtCoord)
        strtCoordY = re.sub(r'[,]',"",strtCoordY[0])
        strtCoordY = int(strtCoordY)
        coordsDict['xy' + str(count)] = [strtCoordX, strtCoordY] # Construct dictionary
        if count>1:
            line = Line(str(count-1), pastX, pastY, strtCoordX, strtCoordY) # Construct line object
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
                    if denominator != 0:
                        t = ((x1 - x3) * (y3 - y4) - (y1 - y3) * (x3 - x4)) / denominator
                        u = - ((x1 - x2) * (y1 - y3) - (y1 - y2) * (x1 - x3)) / denominator
                        if 0 <= t <= 1 and 0 <= u <= 1:  # Falta chequear si las lineas son colineales
                            intersectionCount = intersectionCount + 1
                            xIntersection = round(x1 + t * (x2 - x1), 2)
                            yIntersection = round(y1 + t * (y2 - y1), 2)
                            intersectionList[str(intersectionCount) + '. ' + street1.name + ' - ' + street2.name] =\
                                [round(x1 + t * (x2 - x1), 2), round(y1 + t * (y2 - y1), 2)]
                            vertexList["(" + "{0:.2f}".format(x1) + "," + "{0:.2f}".format(y1) + ")"] = []
                            vertexList["(" + "{0:.2f}".format(x2) + "," + "{0:.2f}".format(y2) + ")"] = []
                            vertexList["(" + "{0:.2f}".format(x3) + "," + "{0:.2f}".format(y3) + ")"] = []
                            vertexList["(" + "{0:.2f}".format(x4) + "," + "{0:.2f}".format(y4) + ")"] = []
                            vertexList["(" + "{0:.2f}".format(xIntersection) + "," + "{0:.2f}".format(yIntersection) + ")"] = []
    if verbose:
        print("IntersectionDetection: Printing the list of intersections found:")
        for key in sorted(intersectionList.keys()):
            print("%s: %s" % (key, intersectionList[key]))
        print("IntersectionDetection: Printing the list of vertices found:")
        for key in sorted(vertexList.keys()):
            print("%s: %s" % (key, vertexList[key]))



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

    counter=0
    while True:
        if counter < 1:
            line = 'a "Weber Street" (-10,-10) (2,-1) (2,2) (5,5) (5,6) (3,8)'
            checkLine(line)
            line = 'a "King Street S" (4,2) (4,8)'
            checkLine(line)
            line = 'a "Davenport Road" (1,4) (5,8) (10,10)'
            checkLine(line)
            line = 'a "Tarnulfo Street" (6,4)(5,5)(5,6)(6,7)'
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
