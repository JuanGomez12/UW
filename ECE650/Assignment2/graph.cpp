#include "graph.hpp"

#include <iostream>
#include <vector>
#include <climits>
#include <algorithm>
#include <list>

bool verboseGraph = 1; //Makes the graph functions write more information to the console.

Graph::Graph(const int vertices): V(vertices), adjMat(vertices, std::vector<int>(vertices, 0)) {}
int Graph::getV() { return V; }

void Graph::resetAdjMat(){
    
}

void Graph::setV(const int newVertices){
    Graph::V = newVertices;
    Graph::adjMat.assign(newVertices, std::vector<int>(newVertices, 0));
}


bool Graph::addEdge(int u, int v, int w) 
{ 
    if (u < Graph::V && v < Graph::V){
        Graph::adjMat[u][v] = w; 
        Graph::adjMat[v][u] = w;
        return 1;
    }
    return 0;
} 


void Graph::printGraph() 
{
    std::cout << "Adjacency Matrix:" << "\n" << " | ";
    for (int i = 0; i < Graph::V; ++i){
        std::cout << i << " ";
    } 
    std::cout << "\n" << "------------------------------\n";
    for (int i = 0; i < Graph::V; ++i) 
    {
        std::cout << i << "| ";
        for (int j = 0; j < Graph::V; ++j){
           std::cout << Graph::adjMat[i][j] << " ";
        }
        std::cout << "\n";
    } 
} 

bool Graph::shortestPath(int s, int d){
    //Create a copy of the adjacency matrix to operate in it and not modify the original
    int maxInt = INT_MAX; //Maximum value that an int can be
    std::list<int> Q(V); //Create queue
    std::vector<int> dist(V, maxInt); //Create distance vector
    std::vector<int> prev(V, maxInt); //Create rpevious vertex vector
    
    for(int i = 0; i < V; i ++){
        Q.push_front(i);
    }
    dist.at(s) = 0;
    while (!Q.empty()){ //While there are elements not processed in our queue
        int minDist = maxInt;
        int u;
        for(auto it = Q.cbegin(); it != Q.cend(); it++){//Iterate over all the elements still on the queue
            if (dist.at(*it) < minDist){//Figure if the vertex being inspected has a smaller distance than the previous min
                minDist = dist.at(*it);//If it is so, set is as the new minimum distance
                u = *it;//Assign that vertex as the one that will be calculated
            }
        }
        Q.remove(u); //Remove u from our queue
        /*
        for (int i = 0; i < V; i ++){
            int v = adjMat[u][i];
            //If vertex is a neighbor of our test vertex u and is still in the queue:
            if(v != 0 && std::find(Q.begin(), Q.end(), i) != Q.end()){
                int alternative = dist[u] + 1; //Calculate its alternative distance. Change from 1 to v if the edges have different weights.
                if (alternative < dist[i]){//If the new distance to this vertex is smaller than the rpeviously saved distance.
                    dist[i] = alternative; //Set the newly found distance as the new distance in our distance vector
                    prev[i] = u; //Set the 
                }
            }
        }
        */
        for(auto it = Q.cbegin(); it != Q.cend(); it++){
            int v = adjMat.at(u).at(*it);
            if(v != 0){
                int alternative = dist.at(u) + 1; //Calculate its alternative distance. Change from 1 to v if the edges have different weights.
                if (alternative < dist.at(*it)){//If the new distance to this vertex is smaller than the rpeviously saved distance.
                    dist.at(*it) = alternative; //Set the newly found distance as the new distance in our distance vector
                    prev.at(*it) = u; //Set the 
                }
            }
        }
        if(u == d){
            //Optimal path found
            if (verboseGraph){
                std::cout<<"Arrived at destination node\n";
            }
            //Print the optimal path
            //First recreate the vector for the optimal path from destination to source
            std::vector<int> vec;
            int location = d;
            while(location != s){
                vec.push_back(location);
                location = prev[location];
            }
            vec.push_back(s); //Add source to the vector
            int vecSize = vec.size();//Obtain the size of the array
            for (int i = 0; i < vecSize; i++){
                std::cout<<vec.at(i);//Print the vertex
                if(i < vecSize - 1){
                    std::cout<<"-";//If it is not the last vertex, add a hyphen
                }
                else{
                    std::cout<<"\n";//End the line
                }
            }
            return 1;
        }
    }
    if (verboseGraph){
        std::cout<<"Path not found";
    }
    return 0;
};