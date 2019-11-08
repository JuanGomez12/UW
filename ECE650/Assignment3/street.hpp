
#pragma once


#include <vector>
#include <istream>
#include <ostream>


/* 
Graph class. Keeps a list of the total vertices in the graph, as well as its edges. 
It can also search for the shortest path using the searchShortest() function
*/
class Street 
{ 
    int totalCoords;//Number of coordinates

    std::string name; //name of the street

    std::vector<std::vector<int>> coordVec; //Coordinate matrix for the segments
public:
    //Constructor for the class
    Street(std::string streetName);
    //Function to change the number of segments of the street.
    void setSegments(const int segmentNum);
    //Function to get the number of segments of the street.
    int getSegments();
    //Function for changing the name of the street
    void setName(const std::string streetName);
    //Function for retrieving the name of the street
    std::string getName();
    //Function to get the coordinates of a specific segment, in x1, y1, x2, y2 form
    std::vector<int> getCoords(const int segNum);
    // Function to add a segment to the street
    bool addCoord(const int x1, const int y1);
    //auxiliary function used for checking if a segment is contained within another
    bool segmentsWithinSegments(const int p1, const int p2, const int q1, const int q2);
    //Check if a specified point is contained within a segment
    bool pointWithinSegment(const int x, const int y, const int s_x1, const int s_y1, const int s_x2, const int s_y2);
    //Check if the street has any intersections between the segments already in the street and the new segment about to be introduced.
    //Returns false on no collisions detected
    bool checkCollisions(const int x3, const int y3);
    //Function that calculates the different intersections that can exist with respect to the selected segment
    bool checkIntersect(const int x3, const int y3, const int x4, const int y4);
    // Function to print the segment coordinates for debugging
    void printSegments();
    //Function that returns a string with the coordinates of the street in a (#,#)(#,#) format
    std::string getSegmentsString();
};