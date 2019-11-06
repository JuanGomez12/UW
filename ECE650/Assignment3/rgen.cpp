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
int num_tries = 30; //number of tries each creation of the street will have
bool verbose = false;


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
//bool buildStreets(int s_val, int n_val, int c_val){
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
        Street street(0, strt_name);
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
                if (street.addSegment(x1, y1, x2, y2, false)){//The segment is compatible with the rest of segments of the street
                    if (!intersection_detected){
                        if (j == street_segments - 1 && i > 0){//Last segment of the second street onward
                            for (unsigned int m = 0; m < streets.size(); m++){//Traverse all the previous streets
                                Street prev_street = streets.at(m);
                                int prev_street_segments = prev_street.getSegments();
                                for (int n = 0; n < prev_street_segments; ++n){//Traverse each of the previous street's segments
                                    std::vector<int> prev_coords = prev_street.getSegmentCoords(n); // Get the previous streets coords
                                    int x3 = prev_coords.at(0);
                                    int y3 = prev_coords.at(1);
                                    int x4 = prev_coords.at(2);
                                    int y4 = prev_coords.at(3);
                                    if (street.checkIntersect(x3, y3, x4, y4, true)){//Check if the prev street's segment's coords intersect the new street's
                                        //If they do intersect, add street and mark the bool as true
                                        intersection_detected = true;
                                        segment_added = true;
                                        street.addSegment(x1, y1, x2, y2, true);
                                        break;
                                        if (verbose){
                                            std::cout << "Intersection between streets found, between points: (" << x1 << "," << y1 << ") ("<< x2 << "," << y2;
                                            std::cout << ") and (" << x3 << "," << y3 << ") ("<< x4 << "," << y4 << ")" << std::endl;
                                        }
                                    }
                                    else{
                                        //If they don't, try with a new segment
                                        continue;
                                    }
                                }
                            }
                        }
                        else{//Not the last segment of the second road onward
                            street.addSegment(x1, y1, x2, y2, true);
                            segment_added = true;
                            break; //break out of the k loop
                        }
                    }
                    else{
                        //Already found an intersection in the graph, add the street
                        street.addSegment(x1, y1, x2, y2, true);
                        segment_added = true;
                        break; //break out of the k loop
                    }
                    
                }
            }
            if (!segment_added){//Segment could not be added after num_tries attempts, show error
                std::cerr << "Error: Failed to generate valid input after " << num_tries << " attempts." << std::endl;
                streets.clear();
                return streets;
            }
        }
        if (verbose){
            street.printSegments();
        }
        streets.push_back(street);
    }
    return streets;
}

void printStreets(std::vector<Street> streets){//Function to add the streets using the a command for A1
    for(unsigned int i = 0; i < streets.size(); ++i){
        Street street = streets.at(i);
        std::cout << "a \"" << street.getName() << "\" "  << street.getSegmentsString() << std::endl;
        //std::cerr << "a \"" << street.getName() << "\" "  << street.getSegmentsString() << std::endl;
    }
    std::cout << "g" << std::endl;
    //std::cerr << "g" << std::endl;

}

void deleteStreets(std::vector<Street> streets){//Function to remove the streets using the r command for A1
    for(unsigned int i = 0; i < streets.size(); ++i){
        Street street = streets.at(i);
        std::cout << "r \"" << street.getName() << "\"" << std::endl;
        //std::cerr << "r \"" << street.getName() << "\"" << std::endl;
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

    // expected options are '-s', '-n', '-n' and '-c value'
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
        std::cout << "s = " << s << ", "
                << "n = " << n << ", "
                << "l = " << l << ", "
                << "c = " << c << std::endl;
        //outputFile.close();
    }

    if (verbose){
            if (optind < argc) {
            std::cout << "Found positional arguments\n";
            for (index = optind; index < argc; index++)
                std::cout << "Non-option argument: " << argv[index] << "\n";
        }
    }
    


    bool keepRunning = false;
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
        }
    }
    if (verbose){
            std::cout << "[rgen]: Received EOF" << std::endl;
        }
    return 0;
}