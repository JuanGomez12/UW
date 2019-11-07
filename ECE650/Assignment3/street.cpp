/** Graph class file **/

#include <climits>
#include <iostream>
#include <list>
#include <vector>

#include "street.hpp"


bool verboseStreet = false; //Makes the street functions write more information to the CLI.

Street::Street(std::string streetName): totalCoords(0), name(streetName) {}
    
    int Street::getSegments(){
        return Street::totalCoords - 1;
    }


    void Street::setName(std::string streetName){
        Street::name = streetName;
    }
    
    std::string Street::getName(){
        return Street::name;
    }

    std::vector<int> Street::getCoords(const int segNum){
        // std::cerr << "[street::getCoords] returning coord " << segNum << " of a max possible of " << Street::totalCoords << std::endl;
        return Street::coordVec.at(segNum);
    }

    bool Street::addCoord(const int x1, const int y1){
        //Check if there are any other coords already in the street
        if (Street::totalCoords > 0){
            //Check if the segment that would be created would have a distance of 0
            // std::cerr << "[Street::addCoord] Getting the previous coords" << std::endl;
            std::vector<int> prev_coords = Street::coordVec.at(Street::totalCoords - 1);
            if ((x1 == prev_coords.at(0)) && (y1 == prev_coords.at(1))){
                //Previous pair and current pair are the same
                if(verboseStreet){
                    std::cout << "street::addSegment: Start and finish coordinates are the same" << std::endl;
                }
                return false;
            }
            else{
                //Check if there are no collisions with segments already on the list
                // std::cerr << "[Street::addCoord] Checking collisions" << std::endl;
                if (Street::checkCollisions(x1, y1)){
                    //There was a collision
                    if(verboseStreet){
                        std::cout << "street::addSegment: segment intersected others, could not be added" << std::endl;
                    }
                    return false;  
                }
            }
        }
        
        std::vector<int> newSeg;
        newSeg.push_back(x1);
        newSeg.push_back(y1);
        Street::coordVec.push_back(newSeg);
        Street::totalCoords = Street::totalCoords + 1;
        if(verboseStreet){
            std::cerr << "street::addCoord in street: " <<  Street::getName() << " coord added, with coordinates: " << x1 << " " << y1 << std::endl;
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

    
  
    bool Street::checkCollisions(const int x4, const int y4){
        int x1, y1, x2, y2, x3, y3;
        //First check if there is at least one segment in the street
        if (Street::totalCoords > 1){
            //Check if there is any overlap between this segment and the previous one
            // std::cerr << "[Street::checkCollisions] Setting the previous coords" << std::endl;
            // std::cerr << "[Street::addCoord] Total number of coords is " << Street::totalCoords << std::endl;
            x1 = Street::coordVec.at(Street::totalCoords - 2).at(0);
            y1 = Street::coordVec.at(Street::totalCoords - 2).at(1); 
            x2 = Street::coordVec.at(Street::totalCoords - 1).at(0);
            y2 = Street::coordVec.at(Street::totalCoords - 1).at(1);
            x3 = x2;
            y3 = y2;
            //std::cerr << "[Street::checkCollisions] Previous coords set" << std::endl;
            if(Street::segmentsWithinSegments(x1, x2, x3, x4) && Street::segmentsWithinSegments(y1, y2, y3, y4)){//Segments contain themselves
                return true;
            }
            else if(Street::segmentsWithinSegments(x3, x4, x1, x2) && Street::segmentsWithinSegments(y3, y4, y1, y2)){
                return true;
            }
        }
        //Check if there is any intersection between this segment and the previous one
        for (int i = 1; i < Street::totalCoords - 1; ++i){//Iterate over all of the totalCoords
            //std::cerr << "[Street::addCoord] Checking intersection between coords" << std::endl;
            x1 = Street::coordVec.at(i - 1).at(0);
            y1 = Street::coordVec.at(i - 1).at(1); 
            x2 = Street::coordVec.at(i).at(0);
            y2 = Street::coordVec.at(i).at(1);
            x3 = x2;
            y3 = y2;
            float denominator = ((x1 - x2) * (y3 - y4)) - ((y1 - y2) * (x3 - x4));
            if (denominator != 0){  // Check if they are parallel
                float t = ((x1 - x3) * (y3 - y4) - (y1 - y3) * (x3 - x4)) / denominator;
                float u = ((x1 - x2) * (y1 - y3) - (y1 - y2) * (x1 - x3)) / ((-1) * denominator);
                if (((0 <= t) && (t <= 1)) && ((0 <= u) && (u <= 1))){
                    // there is an intersection between the points
                    if (verboseStreet){
                        std::cerr << "[checkCollision] Found intersection with t, u formula with coordinates: (" << x1 << "," << y1 << ")" << "(" << x2 << "," << y2 << ")"; 
                        std::cerr << " and (" << x3 << "," << y3 << ")" << "(" << x4 << "," << y4 << ")" << std::endl;
                        std::cerr << "denominator = " << denominator << ", t = " << t << " u = " << u << std::endl;
                    }
                    return true;
                }
            }
        }
        //There are not previous totalCoords, so there are no collisions
        return false;
    }


    bool Street::checkIntersect(const int x3, const int y3, const int x4, const int y4){
        int streetSegments = totalCoords - 1; //Number of segments on the street
        for (int i = 0; i < streetSegments; ++i){//Iterate over all the segments
            if (verboseStreet){
                std::cout << "checkIntersect: checking segment " << i << std::endl;
            }
            int x1 = Street::coordVec.at(i).at(0);
            int y1 = Street::coordVec.at(i).at(1); 
            int x2 = Street::coordVec.at(i + 1).at(0);
            int y2 = Street::coordVec.at(i + 1).at(1);
            float denominator = ((x1 - x2) * (y3 - y4)) - ((y1 - y2) * (x3 - x4));
            if (denominator != 0){  // Check if they are parallel
                float t = ((x1 - x3) * (y3 - y4) - (y1 - y3) * (x3 - x4)) / denominator;
                float u = ((x1 - x2) * (y1 - y3) - (y1 - y2) * (x1 - x3)) / ((-1) * denominator);
                if (((0 <= t) && (t <= 1)) && ((0 <= u) && (u <= 1))){
                    // there is an intersection between the points
                    if (verboseStreet){
                        std::cerr << "[checkIntersect] Found intersection with t, u formula with coordinates: (" << x1 << "," << y1 << ")" << "(" << x2 << "," << y2 << ")"; 
                        std::cerr << " and (" << x3 << "," << y3 << ")" << "(" << x4 << "," << y4 << ")" << std::endl;
                        std::cerr << "denominator = " << denominator << ", t = " << t << " u = " << u << std::endl;
                    }
                    return true;
                }
            }
        }
        return false;
    }

    void Street::printSegments(){
        for (int i = 0; i < Street::totalCoords; ++i){
            std::cout << "segment " << i << ": (" << coordVec[i][0] << "," << coordVec[i][1] << ") ---> (";
            std::cout << coordVec[i + 1][2] << "," << coordVec[i + 1][3] << ")" << std::endl;
        }
        //std::cout << "done printing street totalCoords" << std::endl;
    }

    std::string Street::getSegmentsString(){
        std::string streetString;
        for (int i = 0; i < Street::totalCoords; ++i){//Iterate over all the totalCoords in the street
            std::vector<int> coords = Street::coordVec[i];//Obtain one of the vectors that has the coordinates
            streetString = streetString + "(" + std::to_string(coords[0]) + "," + std::to_string(coords[1]) + ")";//Print just the last pair of coordinates
        }
        return streetString;
    }