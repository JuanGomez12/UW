
#pragma once


#include <vector>


/* 
Graph class. Keeps a list of the total vertices in the graph, as well as its edges. 
It can also search for the shortest path using the searchShortest() function
*/
class Street 
{ 
    int segments;    //Number of segments
  
    std::vector<std::vector<int>> coordMat; //Coordinates matrix for the segments
public:
    //Constructor for the class
    Street(const int segmentNum);
    //Function to change the number of segments of the street.
    void setSegments(const int segmentNum);
    //Function to get the number of segments of the street.
    int getSegments();
    //Function to get the coordinates of a specific segment, in x1, y1, x2, y2 form
    std::vector<int> getSegmentCoords(const int segNum);
    // Function to add a segment to the street
    bool addSegment(const int x1, const int y1, const int x2, const int y2);
    //auxiliary function used for checking if a segment is contained within another
    bool segmentsWithinSegments(int p1, int p2, int q1, int q2);
    //Function that calculates the different intersections that can exist with respect to the selected segment
    bool checkIntersect(const int x3, const int y3, const int x4, const int y4, const bool checkAll);
    // Function to print the segment coordinates for debugging
    void printSegments();
};