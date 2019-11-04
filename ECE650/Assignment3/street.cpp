/** Graph class file **/

#include <climits>
#include <iostream>
#include <list>
#include <vector>

#include "street.hpp"


bool verboseStreet = false; //Makes the street functions write more information to the CLI.

Street::Street(const int segmentNum): segments(segmentNum), coordMat(segmentNum, std::vector<int>(4, 0)) {}
    
    int Street::getSegments(){
        return Street::segments;
    }

    std::vector<int> Street::getSegmentCoords(const int segNum){
        std::vector<int> seg = coordMat.at(segNum);
        return seg;
    }

    bool Street::addSegment(const int x1, const int y1, const int x2, const int y2){
        //Check if it is not the first segment to be added to the street
        if (!coordMat.empty()){
            //Check if the previous coordinates correspond to the same coordinates for the next point
            std::vector<int> seg = coordMat.back();
            if (seg.at(2) != x1 && seg.at(3) != y1){
                //The segment that was tried to introduce does not share coordinates with the past segment
                if (verboseStreet){
                    std::cout << "segment that was tried to introduce does not share coordinates with past: x3, y3 != x1, y1:"<< seg[2] << seg[3] << x1 << y1 << std::endl;
                }
                return false;
            }
            //Check if new coordinate intersects past coordinates
            if (Street::checkIntersect(x1, y1, x2, y2, false)){
                if(verboseStreet){
                    std::cout << "street::addSegment: segment intersected others, could not be added" << std::endl;
                }
                return false;  
            }
        }
        //Does not intersect with other segments, then can be added
        std::vector<int> newSeg;
        newSeg.push_back(x1);
        newSeg.push_back(y1);
        newSeg.push_back(x2);
        newSeg.push_back(y2);
        coordMat.push_back(newSeg);

        Street::segments = Street::segments + 1;
        if(verboseStreet){
            std::cout << "street::addSegment: segment added, total segments: " << segments << std::endl;
        }
        return true;
    }
    
    bool Street::segmentsWithinSegments(int p1, int p2, int q1, int q2){//x1, x2, x3, x4
        if ((std::min(p1, p2) <= std::min(q1, q2)) && (std::min(q1, q2) <= std::max(q1, q2)) && (std::max(q1, q2) <= std::max(p1, p2))){
            if (verboseStreet){
                std::cout << "segment contained within other segment: ";
                std::cout << std::min(p1, p2) << " <= " << std::min(q1, q2) << " <= " << std::max(q1, q2) << " <= " << std::max(p1, p2) << std::endl;
            }
            return true;
        }
        //Special case: check if one segment partially overlaps the other (covers collinearity)
        
    return false;
    }

    bool Street::checkIntersect(const int x3, const int y3, const int x4, const int y4, const bool checkAll){
        int streetSegments;
        if (checkAll){
            streetSegments = Street::segments;
        }
        else{
            streetSegments = Street::segments - 1;
        }
        //Check all segments except the last one (contigous one)
        for (int i = 0; i < streetSegments; ++i){
            if (verboseStreet){
                std::cout << "checkIntersect: checking segment " << i << std::endl;
            }
            std::vector<int> seg = coordMat.at(i);
    	    int x1 = seg[0];
            int y1 = seg[1];
            int x2 = seg[2];
            int y2 = seg[3];
            float denominator = (x1 - x2) * (y3 - y4) - (y1 - y2) * (x3 - x4);
                    if (denominator != 0){  // Check if they are parallel
                        float t = ((x1 - x3) * (y3 - y4) - (y1 - y3) * (x3 - x4)) / denominator;
                        float u = - ((x1 - x2) * (y1 - y3) - (y1 - y2) * (x1 - x3)) / denominator;
                        if ((0 <= t) && (t <= 1) && (0 <= u) && (u <= 1)){
                            // there is an intersection between the points
                            return true;
                        }
                    }
                    else if(Street::segmentsWithinSegments(x1, x2, x3, x4) && Street::segmentsWithinSegments(y1, y2, y3, y4)){//Segments contain themselves
                        return true;
                    }
                    else if(Street::segmentsWithinSegments(x3, x4, x1, x2) && Street::segmentsWithinSegments(y3, y4, y1, y2)){
                        return true;
                    }
        }
        //Now check the previous segment
        if (!coordMat.empty()){
            std::vector<int> seg = coordMat.back();
            int x1 = seg[0];
            int y1 = seg[1];
            int x2 = seg[2];
            int y2 = seg[3];
            //Check if new segment is contained within the past one
            if(Street::segmentsWithinSegments(x1, x2, x3, x4) && Street::segmentsWithinSegments(y1, y2, y3, y4)){
                        return true;
            }
            else if(Street::segmentsWithinSegments(x3, x4, x1, x2) && Street::segmentsWithinSegments(y3, y4, y1, y2)){
                        return true;
            }
        }
        return false;
    }

    void Street::printSegments(){
        std::cout << "printing segments:" << std::endl;
        for (int i = 0; i < Street::segments; ++i){
            std::cout << "segment " << i << ": (" << coordMat[i][0] << "," << coordMat[i][1] << ") ---> (";
            std::cout << coordMat[i][2] << "," << coordMat[i][3] << ")" << std::endl;
        }
        //std::cout << "done printing street segments" << std::endl;
    }