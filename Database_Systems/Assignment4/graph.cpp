/** Graph class file **/

#include <climits>
#include <iostream>
#include <list>
#include <memory> // defines std::unique_ptr
#include <vector>


#include "graph.hpp"
//#include "minisat/core/SolverTypes.h" // defines Var and Lit
#include "minisat/core/Solver.h" // defines Solver



bool verboseGraph = false; //Makes the graph functions write more information to the CLI.

Graph::Graph(const int vertNum): V(vertNum), adjMat(vertNum, std::vector<int>(vertNum, 0)) {}

int Graph::getV() { return V; }


void Graph::setV(const int vertNum){
    Graph::V = vertNum;
    Graph::adjMat.assign(vertNum, std::vector<int>(vertNum, 0));
}

std::vector<std::vector<int>> Graph::getAdjMat(){
    return Graph::adjMat;
}

bool Graph::addEdge(int u, int v, int w){ 
    if (u < Graph::V && v < Graph::V){
        Graph::adjMat[u][v] = w; //Set a weight of w to the edge located in u,v in the adjacency matrix
        Graph::adjMat[v][u] = w; //Set a weight of w to the edge located in v,u in the adjacency matrix
        return true;
    }
    return false;
} 

std::string Graph::getEdges(){
    std::string edges = "E {";
    for (int i = 0; i < Graph::V; ++i){//Iterate over the rows of the matrix
            for (int j = i + 1; j < Graph::V; ++j){//Iterate over the columns of the matrix
                if (Graph::adjMat[i][j] > 0){
                    std::string str_i(1, i);
                    std::string str_j(1, j);
                    edges = edges + "<" + str_i + "," + str_j + ">";
                    if (j < Graph::V - 1){
                        edges = edges + ",";
                    }
                }
            }
        } 
    edges = edges + "}";
    return edges;
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
    }
    else if(s == d){//Check if s and d are the same vertex
        std::cout << s << "-" << d << "\n";
        return true;
    }
    else{
        int maxInt = INT_MAX; //Maximum value that an int can be
        std::list<int> Q(V); //Create queue
        std::vector<int> distVec(V, maxInt); //Create distance vector
        std::vector<int> prevVec(V, maxInt); //Create previous vertex vector
        
        for(int i = 0; i < V; i ++) {
            Q.push_front(i);
        }
        distVec.at(s) = 0;
        int minDist;
        int u;
        while (!Q.empty()) { //While there are elements not processed in our queue
            u = Q.front(); //Select the first vertex of Q
            minDist = distVec.at(u); //Select the first element of Q's distance as the minimum 
            for(int it : Q) {//Iterate over all the elements still on the queue
                if (distVec.at(it) < minDist) {//Figure if the vertex being inspected has a smaller distance than the previous min
                    minDist = distVec.at(it);//If it is so, set is as the new minimum distance
                    u = it;//Assign that vertex as the one that will be calculated
                }
            }
            if (verboseGraph){
                std::cout << "vertex selected: " << u << "\n";
                std::cout << "Min distance: " << minDist << "\n";
            }
            Q.remove(u); //Remove u from our queue
            for(int it : Q) {//Iterate over all of the vertices still in the Q
                int v = adjMat.at(u).at(it);
                if(v != 0) {
                    int alternative = distVec.at(u); //Set the alternative distance as the distance to the vertex u
                    if (alternative != maxInt){//If the alternative distacne is smaller than the maximum possible value (infinite)
                        alternative = distVec.at(u) + 1; //Calculate its alternative distance. Change from 1 to v if the edges have different weights.
                    }
                    if (alternative < distVec.at(it)) {//If the new distance to this vertex is smaller than the previously saved distance.
                        distVec.at(it) = alternative; //Set the newly found distance as the new distance in our distance vector
                        prevVec.at(it) = u; //Set the 
                    }
                }
            }
            //If u is the destination it means we got to our destination in one of the shortest paths possible.
            if(u == d and prevVec[d] != maxInt) {
                //Optimal path found
                if (verboseGraph) {
                    std::cout<<"shortestPath: Arrived at destination node\n";
                }
                //Print the optimal path
                //First recreate the vector for the optimal path from destination to source
                std::vector<int> pathVec;
                int location = d;
                while(location != s) {
                    pathVec.push_back(location);
                    location = prevVec[location];
                    if (location == maxInt){
                        if (verboseGraph) {
                            std::cout<<"shortestPath: There is no connection from: "<< location << " to the rest of the nodes\n";
                        }
                        return false;
                    }
                }
                if (verboseGraph) {
                    std::cout<<"shortestPath: Path vector recreated\n";
                }
                pathVec.push_back(s); //Add source to the vector
                int vecSize = pathVec.size();//Obtain the size of the array
                for (int i = vecSize - 1; i >= 0; i--) {
                    std::cout << pathVec.at(i);//Print the vertex
                    if(i > 0){
                        std::cout << "-";//If it is not the last vertex, add a hyphen
                    }
                    else{
                        std::cout << "\n";//End the line
                    }
                }
                return true;
            }
        }
        if (verboseGraph) {
            std::cout<<"Path not found";
        }
    }
    return false;
}

Minisat::Var convertToVar(int integerValue){
    return integerValue - 1;
}

int Graph::vertex_cover_solver() {
    int kVal = 1;
    bool problemSolved = false;
     //-----------------------------------------------------------------------------------------------------------

    // -- allocate on the heap so that we can reset later if needed
    std::unique_ptr<Minisat::Solver> solver(new Minisat::Solver());
    //Minisat::Solver solver;
    for (int k = kVal; k <= V; ++k){//Try to find the vertex cover with the minimum number of k possible
        solver.reset (new Minisat::Solver()); //reset the solver
        for (int i = 1; i <= k * V; ++i){
            solver->newVar();//Define the variables
        }
        // ------------------------------------------------------------------
        //Let's add the group of clauses related to the first argument
        for (int i = 1; i <= k; ++i){
            Minisat::vec<Minisat::Lit> litVec; //Create the literal vector
            int value = i;
            litVec.push(Minisat::mkLit(convertToVar(value))); //Push the first value to the vector
            for (int j = 1; j < V; ++j){
                value = value + k;
                litVec.push(Minisat::mkLit(convertToVar(value)));
            }
            solver->addClause(litVec); //Add the clause
        }
        if (solver->solve()){
            std::cout<< "Problem solvable for argument 1 on k = " << k << std::endl;
        }
        // ------------------------------------------------------------------
        // Now the second group of clauses, related to the second argument
        for (int i = 0; i < V; ++i){
            for (int j=0; j < k - 1; ++j){
                for(int m = j + 1; m < k; ++m){
                    Minisat::vec<Minisat::Lit> litVec; //Create the literal vector
                    litVec.push(~Minisat::mkLit(convertToVar(1+ i * k + j)));
                    litVec.push(~Minisat::mkLit(convertToVar(1+ i * k + m)));
                    solver->addClause(litVec); //Add the clause
                    if (verboseGraph){
                        std::cout << 1 + i * k + j << " ";
                        std::cout << 1 + i * k + m << std::endl;
                    }
                }
            }
        }
        if (solver->solve()){
            std::cout<< "Problem solvable for argument 2 on k = " << k << std::endl;
        }
        // ------------------------------------------------------------------
        // The third group of clauses, related to the third argument
        for (int i = 1; i <= k; ++i){
            for (int j = i; j <= k * V; j = j + k){
                for(int m = j + k; m <= k * V; m = m + k){
                    Minisat::vec<Minisat::Lit> litVec; //Create the literal vector
                    litVec.push(~Minisat::mkLit(convertToVar(j)));
                    litVec.push(~Minisat::mkLit(convertToVar(m)));
                    solver->addClause(litVec); //Add the clause
                    if (verboseGraph){
                        std::cout << j << " ";
                        std::cout << m << std::endl;
                    }
                }
            }
        }
        if (solver->solve()){
            std::cout << "Problem solvable for argument 3 on k = " << k << std::endl;
        }
        // ------------------------------------------------------------------
        // The fourth group of clauses, related to the edges of the graph
        int adjMatSize = adjMat.size();
        for(int i = 0; i < adjMatSize; ++i){
            for (int j = i; j < adjMatSize; ++j){
                if (adjMat.at(i).at(j) != 0){
                    Minisat::vec<Minisat::Lit> litVec; //Create the literal vector
                    for (int m = 0; m < k; m++){
                        if (verboseGraph){
                            std::cout << (i*k + m + 1) << " ";
                            std::cout << (j*k + m + 1) << std::endl;
                        }
                        litVec.push(Minisat::mkLit(convertToVar(i*k + m + 1)));
                        litVec.push(Minisat::mkLit(convertToVar(j*k + m + 1)));
                    }
                    solver->addClause(litVec); //Add the clause
                }
            }
        }
        if (solver->solve()){
            std::cout<< "Problem solvable for argument 4 on k = " << k << std::endl;
        }
        // ------------------------------------------------------------------
        //Try solving for this value of k
        problemSolved = solver->solve();
        std::cout<< "Value of solver: " << problemSolved <<std::endl;
        if (problemSolved){
        //if (!problemSolved){
            kVal = k; // Optimal value of k found
            
            //Obtain the real values of the vertices
            std::vector<int> verticesList;
            for (int i = 1; i <= k * V; ++i){
                std::cout<< "Value number " << i << " is: " << Minisat::toInt(solver->modelValue(convertToVar(i))) << std::endl;
                if (Minisat::toInt(solver->modelValue(convertToVar(i))) == 0){ // 0 means the variable is set to true
                    int numVar = i;
                    int vertexCounter = -1;
                    while(numVar > 0){
                        vertexCounter = vertexCounter + 1;
                        numVar = numVar - k;
                    }
                    verticesList.push_back(vertexCounter + 1);
                    if (true){
                        std::cout<< "Total number of vertices are:  "<< k << ", one of them is number: " << vertexCounter << std::endl;
                    }
                }
            }
            

            //return the vertices
            break;
        }
    return 0;
}
