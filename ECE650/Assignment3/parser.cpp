/** Parser function file **/

#include <iostream>
#include <sstream>
#include <string>
#include <vector>

#include "parser.hpp"


bool parse_line (const std::string &line,
                 char &cmd, int &argnum, std::vector<int> &numVec, std::string &err_msg) {

    std::istringstream input(line);

    //Remove whitespace
    ws(input);

    if (input.eof()) {
        err_msg = "Empty command";
        return false;
    }

    char ch;
    input >> ch; //Find if the first element was a character, and what character is it

    if (input.fail()) {
        err_msg = "Failed to read input";
        return false;
    }
    //Check if the command was a V
    if (ch == 'V') {
        cmd = 'N'; //Make the command a different value so that in case something fails it doesn't interfere
        int num;
        input >> num; //Check if the input is a number
        if (input.fail()) {//It seems like it wasn't
            err_msg = "Missing or bad argument";
            return false;
        }
        ws(input);//Remove all whitespace from the input
        if (!input.eof()) {//Check if there was anything else on the input (it shouldn't be)
            err_msg = "Unexpected argument";
            return false;
        }
        cmd = ch; //Set the command
        argnum = num; //Add the found number into the argnum
        return true;
    }
    //Check if the command was an E
    if (ch == 'E') {
        cmd = 'N'; //Make the command a different value so that in case something fails it doesn't interfere
        char character;
        int edge;
        input >> character;
       
        //We now need to see if we can find the pattern for the {<#,#>,<#,#>,...}
        if (input.fail() || character != '{'){//Check for the first part of the edges argument, the {
           err_msg = "Missing or bad argument, possibly missing '{'";
           return false;
        }
        //The rest of the argument can be cyclical, so we can scan it using a while loop
        bool doneParsing = false;
        input >> character;
        while (!doneParsing){
            if (input.fail() || character != '<'){//Check for the second part of the argument, the <
                err_msg = "Missing or bad argument, possibly missing '<'";
                return false;  
            }
            input >> edge; //Check if it can add the first number of the number pair
            if(input.fail()){
                err_msg = "Missing or bad argument, expected first number of a pair";
                return false;  
            }
            numVec.push_back(edge); //If it was able of reading it, save the first number in the array
            input >> character;
            if (input.fail() || character != ','){//Check for the comma that follows
                err_msg = "Missing or bad argument, possibly missing ','";
                return false;  
            }
            input >> edge; //Check if it can read the second number of the number pair
            if(input.fail()){
                err_msg = "Missing or bad argument, expected second number of a pair";
                return false;  
            }
            numVec.push_back(edge); //If it was able of reading it, save the second number in the array
            input >> character;
            if (input.fail() || character != '>'){//Find the > that closes the number pair
                err_msg = "Missing or bad argument, possibly missing '>'";
                return false;  
            }
            input >> character;
            if (character == '}'){//It seems like it is the end of the string, but let's make sure that there isn't anything else
                ws(input);
                if (input.eof()) {
                    doneParsing = true;
                }
                else{
                    err_msg = "Unexpected argument";
                    return false;
                }
            }
            else if(character == ','){//It seems like there are more elements and it is not the end of the stream
                input >> character;
            }
            else{//Something seems to have gone wrong or there was a character missing
                err_msg = "Missing or bad argument";
                return false;  
            }
        }
        cmd = ch;
        return true;
    }
    //Check if the command was an s
    if (ch == 's') {//s selected
        cmd = 'N'; //Make the command a different value so that in case something fails it doesn't interfere
        int num;
        input >> num; //Check if the first element is a number
        if (input.fail()) {//It seems liek it wasn't
            err_msg = "Missing or bad argument";
            return false;
        }

        int num2;//Check to see if the next element is also a number
        input >> num2;
        if (input.fail()) {//It seems like it wasn't
            err_msg = "Missing or bad argument";
            return false;
        }

        ws(input);//Remove all whitespace
        if (!input.eof()) {//Check if that was the end of the line, if not, display an error
            err_msg = "Unexpected argument";
            return false;
        }

        cmd = ch; //Add the command that was issued
        numVec.clear(); //Clear the number vector
        numVec.push_back(num);//Push the first number
        numVec.push_back(num2);//Push the second number
        return true;
    }
    err_msg = "Unknown command";
    return false;
}
