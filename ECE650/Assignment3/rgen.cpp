
#include <iostream>
#include <fstream>
#include <string>
#include <vector>

#include "street.hpp"
//#include <ctype.h>
#include <unistd.h>
#include <stdlib.h> 
//#include <sys/poll.h>

//Initialize default values for s, n, l and c
int s = 10;
int n = 5;
int l = 5;
int c = 20;
int num_tries = 25; //number of tries each creation of the street will have
bool verbose = false;
bool printCommands = false;


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

std::vector<Street> buildStreets(int s_val, int n_val, int c_val){
    //std::cerr << "running buildstreets" <<std::endl;
//bool buildStreets(int s_val, int n_val, int c_val){
    //First obtain the specifications of the streets:
    //Number of streets for the current specification:
    
    int strt_num = abs(getRnd()) % (s_val - 2 + 1) + 2; //Random range based on the answer found on https://stackoverflow.com/a/7560151
    // if (strt_num < 2){
    //     strt_num = 2;
    // }
    if (verbose){
        std::cerr << "Random number of streets: " << strt_num << std::endl;
    }
    //Maximum size of the coordinate system:
    int coords = abs(getRnd()) % (c_val - 1 + 1) + 1; //Random range based on the answer found on https://stackoverflow.com/a/7560151
    // if (coords < 1){
    //     coords = 1;
    // }
    if (verbose){
        std::cerr << "Range of coords: " << coords << std::endl;
    }

    std::vector<std::string> strt_names;
    std::vector<Street> streets;

    bool intersection_detected = false; //Boolean that indicates if there is at least one pair of streets that intersect
    for(int i = 0; i < strt_num; i++){
        //Get the street name
        std::string strt_name = genRndStrt();
        if (verbose){
            std::cerr << "Creating street: " << strt_name << ", street number: " << i << std::endl;
        }

        //strt_names.push_back(strt_name);
        //Create a street object
        Street street(strt_name);
        //Find how many segments the street will have
        int street_segments = abs(getRnd()) % (n_val - 1 + 1) + 1; //Random range based on the answer found on https://stackoverflow.com/a/7560151
        if (verbose){
            std::cerr << "Random number of segments of street " << i << ": " << street_segments << std::endl;
        }
        // if (street_segments < 1){
        //     street_segments = 1;
        // }
        //Create the street segments
        //Add the first segment
        int x1 = getRnd() % (coords + 1);
        int y1 = getRnd() % (coords + 1);
        //std::cerr << "(x1,y1) =" << x1 << ", " << y1 << std::endl;
        street.addCoord(x1, y1);
        //Create the rest of the segments
        for (int j = 1; j <= street_segments; ++j){
            if (verbose){
                std::cerr << "Segment " << j << std::endl;
            }
            bool segment_added = false;
            for (int k = 0; k < num_tries; ++k){
                if (!segment_added){
                    x1 = getRnd() % (coords + 1);
                    y1 = getRnd() % (coords + 1);
                    if (verbose){
                        std::cerr << "(x1,y1) =" << x1 << ", " << y1 << std::endl;
                    }
                    
                    if (i == 0){//Check if it is the first street
                            // std::cerr << "Adding new coordinate to street" << std::endl;
                        if (street.addCoord(x1, y1)){
                            segment_added = true;
                            break;
                        }
                    }
                    if (!intersection_detected){//Is there already an intersection in the graph?
                        //Get the previous points of the street to form the segment
                        // std::cerr << "Getting past coordinates " << j << " of a total of " << street_segments << std::endl;
                        std::vector<int> prev_coord = street.getCoords(j - 1);
                        int x_prev = prev_coord.at(0);
                        int y_prev = prev_coord.at(1);
                        if (j == street_segments - 1){//Check if it is the last segment of the street
                            for (int m = 0 ; m < i; ++m){//Compare if they might have formed an intersection with a previous street
                                Street prev_street = streets.at(m);
                                if (prev_street.checkIntersect(x_prev, y_prev, x1, y1)){
                                    if (street.addCoord(x1, y1)){
                                        segment_added = true;
                                        intersection_detected = true;
                                        break;
                                    }
                                }
                                else{//There is no intersection
                                    if (i != strt_num - 1){//Check if it is not the last segment of the last street
                                        if (street.addCoord(x1, y1)){
                                            segment_added = true;
                                            break;
                                        }
                                    }
                                }
                            }
                        }
                        else{//It is not the last segment of a previous street
                            if (street.addCoord(x1, y1)){
                                segment_added = true;
                                break;
                            }
                        }
                    }
                    else{//There's already an intersection on the graph, just try to add the point
                        if (street.addCoord(x1, y1)){
                            segment_added = true;
                            break;
                        }
                    }
                }
                
            }
            if (!segment_added){//Segment could not be added after num_tries attempts, show error
                std::cerr << "Error: Failed to generate valid input after " << num_tries << " attempts." << std::endl;
                streets.clear();
                return streets;
            }
        }
        streets.push_back(street);//Add the street to the lsit of streets
    }
    return streets;//Return the street vector
}

void printStreets(std::vector<Street> streets){//Function to add the streets using the 'a' command for A1 followed by the 'g' command
    for(unsigned int i = 0; i < streets.size(); ++i){
        Street street = streets.at(i);
        if (printCommands){
            std::cerr << "a \"" << street.getName() << "\" "  << street.getSegmentsString() << std::endl;
        }
        std::cout << "a \"" << street.getName() << "\" "  << street.getSegmentsString() << std::endl;
    }
    if (printCommands){
        std::cerr << "g" << std::endl;
    }
    std::cout << "g" << std::endl;
}

void deleteStreets(std::vector<Street> streets){//Function to remove the streets using the 'r' command for A1
    for(unsigned int i = 0; i < streets.size(); ++i){
        Street street = streets.at(i);
        if (printCommands){
            std::cerr << "r \"" << street.getName() << "\"" << std::endl;
        }
        std::cout << "r \"" << street.getName() << "\"" << std::endl;
    }
}

int main (int argc, char **argv)
{

    std::string s_value;
    std::string n_value;
    std::string l_value;
    std::string c_value;
    int index;
    int cmd;

    opterr = 0;

    // expected options are '-s', '-n', '-l' and '-c value'
    while ((cmd = getopt (argc, argv, "s:n:l:c:")) != -1)
        switch (cmd)
            {
            case 's':
                s_value = optarg;
                s = atoi(s_value.c_str());
                if (s < 2){
                    std::cerr << "Error: s value cannot be less than 2" << std::endl;
                    return 1;
                }
                break;
            case 'n':
                n_value = optarg;
                n = atoi(n_value.c_str());
                if (n < 1){
                    std::cerr << "Error: n value cannot be less than 1" << std::endl;
                    return 1;
                }
                break;
            case 'l':
                l_value = optarg;
                l = atoi(l_value.c_str());
                if (l < 5){
                    std::cerr << "Error: l value cannot be less than 5" << std::endl;
                    return 1;
                }
                break;
            case 'c':
                c_value = optarg;
                c = atoi(c_value.c_str());
                if (c < 1){
                    std::cerr << "Error: c value cannot be less than 1" << std::endl;
                    return 1;
                }
                break;
            }

    if (verbose){
        std::cerr << "s = " << s << ", "
                << "n = " << n << ", "
                << "l = " << l << ", "
                << "c = " << c << std::endl;
        //outputFile.close();
    }

    if (verbose){
            if (optind < argc) {
            std::cerr << "Found positional arguments\n";
            for (index = optind; index < argc; index++)
                std::cerr << "Non-option argument: " << argv[index] << "\n";
        }
    }
    


    bool keepRunning = true;
    while(keepRunning){
        std::vector<Street> streets;
        streets = buildStreets(s, n, c);
        if (!streets.empty()){
            printStreets(streets);
            int sleep_time = getRnd() % (l + 1);
            if (sleep_time < 5){
                sleep_time = 5;
            }
            sleep(sleep_time);
            deleteStreets(streets);
        }
        else{
            keepRunning = false;
            return 1;
        }
    }
    return 0;
}