#include "graph.hpp"

#include <iostream>
#include <vector>
#include <climits>
#include <algorithm>
#include <list>

bool verboseGraph = 1; //Makes the graph functions write more information to the console.

Graph::Graph(const int vertices): V(vertices), adjMat(vertices, std::vector<int>(vertices, 0)) {}
int Graph::getV() { return V; }

void Graph::setV(int vertices){
    V = vertices;
    std::vector<int> intVector(V, 0);
    adjMat.resize(V, intVector);
}


void Graph::addEdge(int u, int v) 
{ 
    adjMat[u][v] = 1; 
    adjMat[v][u] = 1; 
} 

void Graph::printGraph() 
{
    std::cout << "Adjacency Matrix:" << "\n" << " | ";
    for (int i = 0; i < V; ++i){
        std::cout << i << " ";
    } 
    std::cout << "\n" << "------------------------------\n";
    for (int i = 0; i < V; ++i) 
    {
        std::cout << i << "| ";
        for (int j = 0; j < V; ++j){
           std::cout << adjMat[i][j] << " ";
        }
        std::cout << "\n";
    } 
} 

bool Graph::searchShortest(int s, int d){
    //Create a copy of the adjacency matrix to operate in it and not modify the original
    std::vector<std::vector<int>> adjMatCopy = adjMat; 
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
            if (dist.at(*it) < minDist){//Find the one with the minimum distance
                minDist = dist.at(*it);
                u = *it;
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
            int v = adjMat[u][*it];
            if(v != 0){
                int alternative = dist[u] + 1; //Calculate its alternative distance. Change from 1 to v if the edges have different weights.
                if (alternative < dist[*it]){//If the new distance to this vertex is smaller than the rpeviously saved distance.
                    dist[*it] = alternative; //Set the newly found distance as the new distance in our distance vector
                    prev[*it] = u; //Set the 
                }
            }
        }
        if(u == d){
            if (verboseGraph){
                std::cout<<"Arrived at destination node";
                std::vector<int> vec;
                int location = d;
                while(location != s){
                    vec.push_back(location);
                    location = prev[location];
                }
                int vecSize = vec.size();
                for (int i = 0; i < vecSize; i++){
                    std::cout<<vec.at(i);
                    if(i < vecSize - 1){
                        std::cout<<"-";
                    }
                }
                std::cout<<"\n";
                return 1;
            }
        }
    }
    if (verboseGraph){
        std::cout<<"Path not found";
    }
    return 0;
};