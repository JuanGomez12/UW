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
    while (!std::cin.eof()) {

        // read a line of input until EOL and store in a string
        std::string line;
        std::getline(std::cin, line);

        // if nothing was read, go to top of the while to check for eof
        if (line.size() == 0) {
            continue;
        }

        char cmd;
        int num = 2;
        std::string arg;

        std::string err_msg;
        Graph graph(num);

        if (parse_line(line, cmd, num, arg, err_msg)) {
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
                            std::cout << "E selected with edges: " << arg << "\n" ;
                        }
                        //Add edges to graph
                        graph.printGraph();
                        vertex_selected = 0;
                        edges_selected = 1;
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
                            std::cout << "S selected with path from vertex: " << num << " to vertex: " << std::stoi(arg) << "\n";
                        }
                        break;
                    }
                    else{
                    std::cerr << "Error: " << "Invalid command sequence" << "\n";
                        vertex_selected = 0;
                        edges_selected = 0;
                    }
                }
            }
        }
        else {
            std::cerr << "Error: " << err_msg << "\n";
            vertex_selected = 0;
            edges_selected = 0;
        }
    }
}
