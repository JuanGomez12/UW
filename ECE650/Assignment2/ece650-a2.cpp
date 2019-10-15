/** Main file */
#include <iostream>
#include <sstream>
#include <vector>

#include "parser.hpp"
#include "graph.hpp"

bool verbose = 1;
bool vertex_selected = 0;
bool edges_selected = 0;

int main(int argc, char** argv) {

 //   Parser reg;
    // read from stdin until EOF
    Graph graph(20);
    while (!std::cin.eof()) {
    bool errorState = 1;
        // read a line of input until EOL and store in a string
        std::string line;
        std::getline(std::cin, line);

        // if nothing was read, go to top of the while to check for eof
        if (line.size() == 0) {
            continue;
        }

        char cmd;
        int num;
        std::vector<int> numVec;

        std::string err_msg;

        if (parse_line(line, cmd, num, numVec, err_msg)) {
            switch (cmd) {
                case 'V':{
                    //Create graph with number of vertices = to num
                    graph.setV(num);
                    vertex_selected = 1;
                    edges_selected = 0;
                    if (verbose){
                        std::cout << "V selected with value: " << num << "\n" ;
                        graph.printGraph();
                    }
                    break;
                }
                case 'E':{
                    if (vertex_selected){
                        if (verbose){
                            std::cout << "E selected with edges: " << "\n";
                            for(auto it = numVec.cbegin(); it != numVec.cend(); it++){
                                std::cout << *it << "\n";
                            }
                        }
                        //Add edges to graph
                        /*
                        while(!numVec.empty()){
                            int edge1 = numVec.back();
                            numVec.pop_back();
                            int edge2 = numVec.back();
                            numVec.pop_back();
                            if(!graph.addEdge(edge1, edge2)){
                                errorState = 1;
                                err_msg = "Error introducing the edges";
                                break;
                            }
                        
                        }
                        */
                        if (!errorState){
                            vertex_selected = 0;
                            edges_selected = 1;
                        }
                        if (graph.addEdge(0,1)){
                            graph.addEdge(0,2);
                            graph.addEdge(1,3);
                            graph.addEdge(3,6);
                            graph.addEdge(2,4);
                            graph.addEdge(4,5);
                            graph.addEdge(5,6);
                            graph.addEdge(5,3);
                            graph.addEdge(1,2);
                            graph.addEdge(1,5);

                            vertex_selected = 0;
                            edges_selected = 1;
                            if (verbose){
                                std::cout << "Edges added";
                                graph.printGraph();
                            }
                        }
                        else{
                            if (verbose){
                                std::cout << "Error: Edges could not be added, out of bounds\n";
                            }
                        }

                    }
                    else{
                        std::cerr << "Error: " << "Tried to create edges without defining vertex number first" << "\n";
                        vertex_selected = 0;
                        edges_selected = 0;
                    }
                    break;
                }
                case 'S':{
                    if (edges_selected && !vertex_selected){
                        //Search for shortest path
                        if (verbose){
                            std::cout << "S selected with path from vertex: " << numVec[0] << " to vertex: " << numVec[1] << "\n";
                        }
                        if (graph.shortestPath(numVec[0], numVec[1])){
                            if (verbose){
                                std::cout<<"Shortest path found\n";
                            }
                        }
                        else{
                            errorState = 1;
                            err_msg = "Shortest path not found. It is possible that there is no path between the selected vertices.";
                        }
                    }
                    else{
                    err_msg = "Invalid command sequence";
                    //std::cerr << "Error: " << "Invalid command sequence" << "\n";
                        vertex_selected = 0;
                        edges_selected = 0;
                    }
                    break;
                }
            }
        }
        else {
            std::cerr << "Error: " << err_msg << "\n";
            errorState = 1;
            vertex_selected = 0;
            edges_selected = 0;
        }
        /*
        if (errorState){
            std::cerr << "Error: " << err_msg << "\n";
            errorState = 0;
        }
        */
    }
}
