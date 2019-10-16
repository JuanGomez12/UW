#include "graph.hpp"

#include <iostream>
#include <vector>
#include <climits>
#include <algorithm>
#include <list>

bool verboseGraph = 0; //Makes the graph functions write more information to the console.

Graph::Graph(const int vertices): V(vertices), adjMat(vertices, std::vector<int>(vertices, 0)) {}
int Graph::getV() { return V; }


void Graph::setV(const int newVertices){
    Graph::V = newVertices;
    Graph::adjMat.assign(newVertices, std::vector<int>(newVertices, 0));
}


bool Graph::addEdge(int u, int v, int w){ 
    if (u < Graph::V && v < Graph::V){
        Graph::adjMat[u][v] = w; //Set a weight of w to the edge located in u,v in the adjacency matrix
        Graph::adjMat[v][u] = w; //Set a weight of w to the edge located in v,u in the adjacency matrix
        return 1;
    }
    return 0;
} 


void Graph::printGraph() {
    std::cout << "Adjacency Matrix:" << "\n" << " |\t";
    for (int i = 0; i < Graph::V; ++i){//Iterate over the values of the matrix to create the columns
        std::cout << i << "\t";
    } 
    std::cout << "\n" << "---------------------------------------------------------------\n";//Create a line
    for (int i = 0; i < Graph::V; ++i){//Iterate over the rows of the matrix
        std::cout << i << "|\t";
        for (int j = 0; j < Graph::V; ++j){//Iterate over the columns of the matrix
           std::cout << Graph::adjMat[i][j] << "\t"; //Print the matrix
        }
        std::cout << "\n";
    } 
} 

bool Graph::shortestPath(int s, int d) {
    if (s > V - 1 || d > V - 1) {//First figure out if the selected vertices are larger than what could possibly be
        if (verboseGraph) {
            std::cout << "shortestPath: s or d are bigger than max vertices";
        }
        return false;
    }
    else{
        //Create a copy of the adjacency matrix to operate in it and not modify the original
        int maxInt = INT_MAX; //Maximum value that an int can be
        std::list<int> Q(V); //Create queue
        std::vector<int> dist(V, maxInt); //Create distance vector
        std::vector<int> prev(V, maxInt); //Create previous vertex vector
        
        for(int i = 0; i < V; i ++) {
            Q.push_front(i);
        }
        dist.at(s) = 0;
        int minDist;
        int u;
        while (!Q.empty()) { //While there are elements not processed in our queue
            u = Q.front(); //Select the first vertex of Q
            minDist = dist.at(u); //Select the first element of Q's distance as the minimum 
            for(auto it = Q.cbegin(); it != Q.cend(); it++) {//Iterate over all the elements still on the queue
                if (dist.at(*it) < minDist) {//Figure if the vertex being inspected has a smaller distance than the previous min
                    minDist = dist.at(*it);//If it is so, set is as the new minimum distance
                    u = *it;//Assign that vertex as the one that will be calculated
                }
            }
            if (verboseGraph){
                std::cout << "vertex selected: " << u << "\n";
                std::cout << "Min distance: " << minDist << "\n";
            }
            Q.remove(u); //Remove u from our queue
            for(auto it = Q.cbegin(); it != Q.cend(); it++) {
                int v = adjMat.at(u).at(*it);
                if(v != 0) {
                    int alternative = dist.at(u); //Set the alternative distance as the distance to the vertex u
                    if (alternative != maxInt){//If the alternative distacne is smaller than the maximum possible value (infinite)
                        alternative = dist.at(u) + 1; //Calculate its alternative distance. Change from 1 to v if the edges have different weights.
                    }
                    if (alternative < dist.at(*it)) {//If the new distance to this vertex is smaller than the previously saved distance.
                        dist.at(*it) = alternative; //Set the newly found distance as the new distance in our distance vector
                        prev.at(*it) = u; //Set the 
                    }
                }
            }
            //If u is the destination it means we got to our destination in one of the shortest paths possible.
            if(u == d and prev[d] != maxInt) {
                //Optimal path found
                if (verboseGraph) {
                    std::cout<<"shortestPath: Arrived at destination node\n";
                }
                //Print the optimal path
                //First recreate the vector for the optimal path from destination to source
                std::vector<int> vec;
                int location = d;
                while(location != s) {
                    vec.push_back(location);
                    location = prev[location];
                    if (location== maxInt){
                        if (verboseGraph) {
                            std::cout<<"shortestPath: There is no connection from: "<< location << " to the rest of the nodes\n";
                        }
                        return false;
                    }
                }
                if (verboseGraph) {
                    std::cout<<"shortestPath: Path vector recreated\n";
                }
                vec.push_back(s); //Add source to the vector
                int vecSize = vec.size();//Obtain the size of the array
                for (int i = vecSize - 1; i >= 0; i--) {
                    std::cout<<vec.at(i);//Print the vertex
                    if(i > 0){
                        std::cout<<"-";//If it is not the last vertex, add a hyphen
                    }
                    else{
                        std::cout<<"\n";//End the line
                    }
                }
                return 1;
            }
        }
        if (verboseGraph) {
            std::cout<<"Path not found";
        }
        return 0;
    }
}