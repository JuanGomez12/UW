
#pragma once


#include <vector>


/* 
Graph class. Keeps a list of the total vertices in the graph, as well as its edges. 
It can also search for the shortest path using the searchShortest() function
*/
class Graph 
{ 
    int V;    //Number of vertices 
  
    std::vector<std::vector<int>> adjMat; //Adjacency matrix for the vertices
    
public:
    //Constructor for the class
    Graph(const int vertNum);
    //Function to change the number of vertices of the graph.
    void setV(const int vertNum);
    //Function to get the number of vertices of the graph.
    int getV();
    //Function that returns the adjacency amtrix of the graph
    std::vector<std::vector<int>> getAdjMat();
    // Function to add an edge to the graph with a weight. If weight is not specified it is assumed to be 1.
    bool addEdge(const int u, const int v, int w = 1);
    //Function that returns in a string form the edges of the graph
    std::string getEdges();
    // Function to print the adjacency matrix of the graph. Mainly for debugging.
    void printGraph();
    // Function that finds and prints the shortest traversal path between s and d, if it exists. 
    bool shortestPath(int s, int d);
    //Function that configures the minisat solver and tries to find the CNF-SAT of teh vertex cover of the graph
    int vertex_cover_solver();
};