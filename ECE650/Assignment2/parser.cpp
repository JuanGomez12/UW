#include "parser.hpp"

#include <iostream>
#include <sstream>
#include <string>
#include <vector>

bool parse_line (const std::string &line,
                 char &cmd, int &argnum, std::vector<int> &numVec, std::string &err_msg) {

    std::istringstream input(line);

    // remove whitespace
    ws(input);

    if (input.eof()) {
        err_msg = "Empty command";
        return false;
    }

    char ch;
    input >> ch;

    if (input.fail()) {
        err_msg = "Failed to read input";
        return false;
    }

    if (ch == 'V') {
        int num;
        input >> num;
        if (input.fail()) {
            err_msg = "Missing or bad argument";
            return false;
        }
        ws(input);
        if (!input.eof()) {
            err_msg = "Unexpected argument";
            return false;
        }
        cmd = ch;
        argnum = num;
        return true;
    }
    else if (ch == 'E') {
        /*
        int num;
        input >> num;
        if (input.fail()) {
            err_msg = "Missing or bad argument";
            return false;
        }
        std::cout<< "Edge: Number found: "<< num;
        ws(input);
        if (!input.eof()) {
            err_msg = "Unexpected argument";
            return false;
        }
        cmd = ch;
        //argstr = edges;
        return true;
        */
       char character;
       int edge;
       input >> character;
       if (input.fail() || character != '{'){
           err_msg = "Missing or bad argument, possibly missing '{'";
           return false;
       }
       while (!input.eof()){
           input >> character;
            if (input.fail() || character != '<'){
                err_msg = "Missing or bad argument, possibly missing '<'";
                return false;  
            }
            input >> edge;
            if(input.fail()){
                err_msg = "Missing or bad argument, expected number";
                return false;  
            }
            numVec.push_back(edge);
            input >> character;
            if (input.fail() || character != ','){
                err_msg = "Missing or bad argument, possibly missing ','";
                return false;  
            }
            input >> edge;
            if(input.fail()){
                err_msg = "Missing or bad argument, expected number";
                return false;  
            }
            numVec.push_back(edge);
            input >> character;
            if (input.fail() || character != '>'){
                err_msg = "Missing or bad argument, possibly missing '>'";
                return false;  
            }
            input >> character;
            if (character == ',' || character == '}'){
                input >> character;
            }
            else if(input.fail()){
                err_msg = "Missing or bad argument, possibly missing '>'";
                return false;  
            }
       }
    }
    else if (ch == 'S') {
        int num;
        input >> num;
        if (input.fail()) {
            err_msg = "Missing or bad argument";
            return false;
        }

        int num2;
        input >> num2;
        if (input.fail()) {
            err_msg = "Missing or bad argument";
            return false;
        }

        ws(input);
        if (!input.eof()) {
            err_msg = "Unexpected argument";
            return false;
        }

        cmd = ch;
        numVec.clear();
        numVec.push_back(num);
        numVec.push_back(num2);
        return true;
    }
    else {
        err_msg = "Unknown command";
        return false;
    }

}
