/** Main file */

#include <iostream>
#include <sstream>
#include <string>
#include <vector>

#include "graph.hpp"
#include "parser.hpp"


bool verbose = false; //Write stuff to the command line to diagnose problems or see what's happening
bool vertex_selected = false; //Indicates that the vertex size for the graph has been selected
bool edges_selected = false; //Indicates that the edges have been input

int main() {
    if (verbose){
        std::cout << "A2 started" << std::endl;
    }
/* // main for when it is desired to accept arguments when running the code:
int main(int argc, char** argv) {
    //Check if any arguments were used when running the code
    for (int i = 0; i < argc; ++i) {
        std::string arg = argv[i];
        if (arg == "--verbose"|| arg == "-v") {//Check if the verbose flag was indicated
            verbose = true; //If it was indicated, set the verbose to true
        }
    }
*/
    Graph graph(0);//Set a default graph size of 0
    //Set the error state of the application to fasle. This is used to know if there is an error that should be reported or printed
    bool errorState = false; 
    while (!std::cin.eof()) {
    //while (true) {
        // read a line of input until EOL and store it in a string
        std::string line;
        std::getline(std::cin, line);

        // if nothing was read, go to top of the while to check for eof
        if (line.empty()) {
            continue;
        }

        /*Create a char, int, vector of type int and string to store the command, number of vertices,
        edges and source and destination vertices, and error messages, respectively
        */
        char cmd;
        int num;
        std::vector<int> numVec;
        std::string err_msg;

        if (parse_line(line, cmd, num, numVec, err_msg)) {//If there is a line that was read correctly
            switch (cmd) {
                case 'V': {
                    //Create graph with number of vertices = to num
                    graph.setV(num);
                    vertex_selected = true;
                    edges_selected = false;
                    if (verbose){
                        std::cout << "V selected with value: " << num << "\n" ;
                        graph.printGraph();
                    }
                    break;
                }
                case 'E':{
                    //Try to add the edges into the graph
                    //First, check if the vertex command was the command previously input and if the program is not in an error state
                    if (vertex_selected && !errorState) {
                        //Add edges to graph
                        while(!numVec.empty()) {
                            int edge1 = numVec.back();
                            numVec.pop_back();
                            int edge2 = numVec.back();
                            numVec.pop_back();
                            if(!graph.addEdge(edge1, edge2)) {
                                errorState = true;
                                err_msg = "Problem introducing the edges, possibly out of bounds";
                                break;
                            }
                        }
                        if (!errorState) {
                            if (verbose) {
                                std::cout << "Edges added";
                                graph.printGraph();
                            }
                            //If there was no error state, modify the flags for vertex_selected and edges_selected
                            vertex_selected = false;
                            edges_selected = true;
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
                case 's': {
                    //Check if the edges were selected first and there was no V command in the middle of the process
                    if (edges_selected && !vertex_selected){
                        if (verbose) {
                            std::cout << "S selected with path from vertex: " << numVec[0] << " to vertex: " << numVec[1] << "\n";
                        }
                        //Search for shortest path
                        if (numVec[0] < graph.getV() && numVec[1] < graph.getV()) {//Check if path selected has vertices smaller than the max allowed
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
                        //Uncommenting the following lines forces a start over on error:
                        //vertex_selected = false;
                        //edges_selected = false;
                    }
                    break;
                }
            }
            if (errorState) {
                //std::cerr << "Error: " << err_msg << "\n"; //Print error message to standard error
                std::cerr << "Error: " << err_msg << "\n"; //Print error message to standard output
                errorState = false;
            }
        }
        else {
            //std::cerr << d"Error: " << err_msg << "\n"; //Print error message to standard error
            std::cerr << "Error: " << err_msg << "\n"; //Print error message to standard output
            errorState = false;
            //Uncommenting the following lines forces a start over on error:
            //vertex_selected = false;
            //edges_selected = false;
        }
    }
    if (verbose){
        std::cerr << "[A2]: Saw EOF" << std::endl;
    }
    return 0; //Return 0 after EOF
}
