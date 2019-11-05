
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
    int segments;    //Number of segments

    std::string name; //name of the street

    std::vector<std::vector<int>> coordMat; //Coordinates matrix for the segments
public:
    //Constructor for the class
    Street(const int segmentNum, std::string streetName);
    //Function to change the number of segments of the street.
    void setSegments(const int segmentNum);
    //Function to get the number of segments of the street.
    int getSegments();
    //Function for changing the name of the street
    void setName(const std::string streetName);
    //Function for retrieving the name of the street
    std::string getName();
    //Function to get the coordinates of a specific segment, in x1, y1, x2, y2 form
    std::vector<int> getSegmentCoords(const int segNum);
    // Function to add a segment to the street
    bool addSegment(const int x1, const int y1, const int x2, const int y2, const bool addStreet);
    //auxiliary function used for checking if a segment is contained within another
    bool segmentsWithinSegments(int p1, int p2, int q1, int q2);
    //Function that calculates the different intersections that can exist with respect to the selected segment
    bool checkIntersect(const int x3, const int y3, const int x4, const int y4, const bool checkAll);
    // Function to print the segment coordinates for debugging
    void printSegments();
    //Function that returns a string with the coordinates of the street in a (#,#)(#,#) format
    std::string getSegmentsString();
};