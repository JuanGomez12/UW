#pragma once

//#include <list> 
#include <vector>

/* 
Graph class. Keeps a list of the total vertices in the graph, as well as its edges. 
It can also search for the shortest path using the searchShortest() function
*/
class Graph 
{ 
    int V;    // No. of vertices 
  
    std::vector<std::vector<int>> adjMat;
public: 
    Graph(const int vertNum);  // Constructor 
    //Function to change the number of vertices of the graph
    void setV(int vertNum);
    //Function to get the number of vertices of the graph
    int getV();
    // Function to add an edge to the graph
    void addEdge(const int u, const int v);  
    // Function to print the graph. Mainly for debugging
    void printGraph();
    // Function that finds and prints the shortest traversal path between s and d, if it exists. 
    bool searchShortest(int s, int d);
}; 
