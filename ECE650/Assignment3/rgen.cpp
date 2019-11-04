#include <iostream>
#include <fstream>
#include <sstream>
#include <string>
#include <vector>

#include "street.hpp"
#include <ctype.h>
#include <unistd.h>
#include <sys/poll.h>

//Initialize default values for s, n, l and c
int s = 10;
int n = 5;
int l = 5;
int c = 20;
int num_tries = 25; //number of tries each creation of the street will have
bool verbose = true;


int getRnd(){//Random number generator
    //open /dev/urandom to read
    std::ifstream urandom("/dev/urandom");
    // check that it did not fail
    if (urandom.fail()) {
        std::cerr << "Error: cannot open /dev/urandom\n";
        return 1;
    }

    // read a random 8-bit value.
    // Have to use read() method for low-level reading
    char ch = 'a';
    urandom.read(&ch, 1);
    // cast to integer to see the numeric value of the character
    /*
    if (verbose){
        std::cout << "Random character: " << (unsigned int)ch << "\n";
    }
    */
    
    // close random stream
    urandom.close();

    return (int)ch;
}

//Function for randomly creating the names of the streets.
//Based on the answers in: http://www.cplusplus.com/forum/windows/88843/
static const char alphanum[] =
"abcdefghijklmnopqrstuvwxyz";
int stringLength = sizeof(alphanum) - 1;
std::string genRndStrt(){
    std::string rnd_str;
    for(int i = 0; i < 31; ++i){
        char c = alphanum[getRnd() % stringLength];
        //std::cout << "character found is: " << s << std::endl;
        if (isalpha(c)){
            std::string s(1, c);
            rnd_str = rnd_str + s;
        }
    }
    rnd_str = rnd_str + " Street";
    return rnd_str;
}

bool buildStreets(int s_val, int n_val, int c_val){
    //First obtain the specifications of the streets:
    //Number of streets for the current specification:
    int strt_num = getRnd() % s_val;
    if (strt_num < 2){
        strt_num = 2;
    }
    //Maximum size of the coordinate system:
    int coords = getRnd() % (c_val + 1);
    if (coords < 1){
        coords = 1;
    }

    std::vector<std::string> strt_names;
    std::vector<Street> streets;

    bool intersection_detected = false; //Boolean that indicates if there is at least one pair of streets that intersect
    for(int i = 0; i < strt_num; i++){
        //Get the street name
        std::string strt_name = genRndStrt();
        if (verbose){
            std::cout<< "Creating street: " << strt_name << ", street number: " << i << std::endl;
        }

        strt_names.push_back(strt_name);
        //Create a street object
        Street street(0);
        //Find how many segments the street will have
        int street_segments = getRnd() % (n_val + 1);
        if (street_segments < 1){
            street_segments = 1;
        }
        //Create the street segments
        for (int j = 0; j < street_segments; ++j){
            bool segment_added = false;
            for (int k = 0; k < num_tries; ++k){
                int x1;
                int y1;
                if (j == 0){//First coordinate of the first segment
                    x1 = getRnd() % (coords + 1);
                    y1 = getRnd() % (coords + 1);
                }
                else{//Get the coordinates of the previous segment
                    std::vector<int> prev_coords = street.getSegmentCoords(j - 1);
                    x1 = prev_coords.at(2);
                    y1 = prev_coords.at(3);
                }
                int x2 = getRnd() % (coords + 1);
                int y2 = getRnd() % (coords + 1);
                if (street.addSegment(x1, y1, x2, y2)){
                    segment_added = true;
                    for (int m = 0; m < streets.size(); ++m){//Check if there is an intersection with another previously built street
                       Street street2 = streets.at(m);
                        for (int n = 0; n < street2.getSegments(); ++n){//Traverse the segments of one of the streets and look for an intersection
                            std::vector<int> prev_coords = street2.getSegmentCoords(n);
                            int x3 = prev_coords.at(0);
                            int y3 = prev_coords.at(1);
                            int x4 = prev_coords.at(2);
                            int y4 = prev_coords.at(3);
                            if (street.checkIntersect(x3, y3, x4, y4, true) && !intersection_detected){//If an intersection is found between two streets, modify the boolean
                                intersection_detected = true;
                                if (verbose){
                                std::cout << "Intersection between streets found!" << std::endl;
                                }
                            }
                        } 
                    }
                    break;
                }
            }
            if (!segment_added){//Segment could not be added after num_tries attempts, show error
                std::cerr << "Error: Failed to generate valid input after " << num_tries << " attempts." << std::endl;
                return false;
            }
        }
        if (verbose){
            street.printSegments();
        }
        streets.push_back(street);
    }
    //Create the next street
    return true;
}

int main (int argc, char **argv)
{
    std::ofstream outputFile;
    if (verbose){
        outputFile.open("rgenData.txt");
        outputFile << "rgen started" << std::endl;
        
    }

    std::string s_value;
    std::string n_value;
    std::string l_value;
    std::string c_value;
    int index;
    int cmd;

    opterr = 0;

    // expected options are '-a', '-b', and '-c value'
    while ((cmd = getopt (argc, argv, "s:n:l:c:")) != -1)
        switch (cmd)
            {
            case 's':
                s_value = optarg;
                s = atoi(s_value.c_str());
                break;
            case 'n':
                n_value = optarg;
                n = atoi(n_value.c_str());
                break;
            case 'l':
                l_value = optarg;
                l = atoi(l_value.c_str());
                break;
            case 'c':
                c_value = optarg;
                c = atoi(c_value.c_str());
                break;
            }

    if (verbose){
        outputFile << "s = " << s << ", "
                << "n = " << n << ", "
                << "l = " << l << ", "
                << "c = " << c << std::endl;
        //outputFile.close();
    }


    if (optind < argc) {
        std::cout << "Found positional arguments\n";
        for (index = optind; index < argc; index++)
            std::cout << "Non-option argument: " << argv[index] << "\n";
    }


    int tried = 0;
    while (tried < 3){//Write code that creates the streets
        if (!buildStreets(s, n, c)){
            tried = tried+1;
        }
        else{
            std::cout << "----------------------STREET BUILT SUCCESFULLY----------------------" << std::endl;
        }

    }
    
    
    
    //while(getppid()!= 1) {
    /*
    while (!std::cin.eof()) {
        
        std::string line;
        std::getline(std::cin, line);
        std::cerr << "[rgen]: Read: " << line << std::endl;
        */
    while(false){
    //while(!std::cin.eof()){
        std::cout << "a \"vertical Street\" (20,20)(20,30)"<< std::endl;
        std::cout << "a \"Horizontal Street\" (19,25)(29,25)"<< std::endl;
        std::cout << "g"<< std::endl;
        if (verbose){
            outputFile << "printed streets and asked for graph" << std::endl;
        }
        sleep(3);
        std::cout << "r \"vertical Street\"" << std::endl;
        std::cout << "r \"Horizontal Street\"" << std::endl;
        if (verbose){
            outputFile << "deleted streets" << std::endl;
        }
        sleep(2);
        
    }
    if (verbose){
            std::cerr << "[rgen]: Received EOF" << std::endl;
            outputFile << "[rgen]: received EOF" << std::endl;
            outputFile.close();
        }
/*
// 
    */
    return 0;
}