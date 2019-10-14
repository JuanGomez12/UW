#include "parser.hpp"

#include <iostream>
#include <sstream>
#include <string>

bool parse_line (const std::string &line,
                 char &cmd, int &argnum, std::string &argstr, std::string &err_msg) {

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
        std::string edges;
        input >> edges;
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
        argstr = edges;
        return true;
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
        argnum = num;
        argstr = std::to_string(num2);
        return true;
    }
    else {
        err_msg = "Unknown command";
        return false;
    }

}
