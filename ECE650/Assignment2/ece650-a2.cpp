/** Main file */
#include <iostream>
#include <sstream>
#include <vector>

#include "parser.hpp"
#include "graph.hpp"

bool verbose = true;
bool vertex_selected = false;
bool edges_selected = false;

int main(int argc, char** argv) {

 //   Parser reg;
    // read from stdin until EOF
    Graph graph(20);
    bool errorState = false;
    while (!std::cin.eof()) {
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
                case 'V': {
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
                    if (vertex_selected && !errorState) {
                        if (verbose){
                            std::cout << "E selected with edges: " << "\n";
                            for(auto it = numVec.cbegin(); it != numVec.cend(); it++) {
                                std::cout << *it << "\n";
                            }
                        }
                        //Add edges to graph
                        while(!numVec.empty()) {
                            int edge1 = numVec.back();
                            numVec.pop_back();
                            int edge2 = numVec.back();
                            numVec.pop_back();
                            if(!graph.addEdge(edge1, edge2)) {
                                errorState = 1;
                                err_msg = "Problem introducing the edges, possibly out of bounds";
                                break;
                            }
                        }
                        if (!errorState) {
                            if (verbose) {
                                std::cout << "Edges added";
                                graph.printGraph();
                            }
                            vertex_selected = 0;
                            edges_selected = 1;
                        }
                        else{
                            if (verbose) {
                                std::cout << "Error: Edges could not be added, out of bounds\n";
                                graph.printGraph();
                            }
                        }

                    }
                    else {
                        err_msg =  "Tried to create edges without defining vertex number first";
                        errorState = true;
                        vertex_selected = false;
                        edges_selected = false;
                    }
                    break;
                }
                case 'S': {
                    if (edges_selected && !vertex_selected){
                        //Search for shortest path
                        if (verbose) {
                            std::cout << "S selected with path from vertex: " << numVec[0] << " to vertex: " << numVec[1] << "\n";
                        }
                        if (numVec[0] < graph.getV() && numVec[1] < graph.getV()) {//Check if path selected has vertices smaller than the maximum allowed
                            if (graph.shortestPath(numVec[0], numVec[1])) {
                                if (verbose){
                                    std::cout<<"Shortest path found\n";
                                }
                            }
                            else {
                                errorState = true;
                                err_msg = "Shortest path not found. It is possible that there is no path between the selected vertices.";
                            }
                        }
                        else {
                            errorState = true;
                            err_msg = "Path contains one or more vertices outside of maximum size of graph";
                        }
                        
                    }
                    else{
                    err_msg = "Invalid command sequence";
                        errorState = true;
                        vertex_selected = false;
                        edges_selected = false;
                    }
                    break;
                }
            }
            if (errorState) {
                std::cerr << "Error: " << err_msg << "\n";
                errorState = false;
            }
        }
        else {
            std::cerr << "Error: " << err_msg << "\n";
            errorState = false;
            vertex_selected = 0;
            edges_selected = 0;
        }
    }
}