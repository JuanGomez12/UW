#include <iostream>
#include <fstream>
#include <sstream>
#include <string>
#include <vector>

#include <unistd.h>
#include <signal.h>
#include <sys/wait.h>

//Initialize default values for s, n, l and c
int s = 10;
int n = 5;
int l = 5;
int c = 20;
bool verbose = true;

unsigned int getRnd(){//Random number generator
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

    return (unsigned int)ch;
}

//Function for randomly creating the names of the streets.
//Based on the answers in: http://www.cplusplus.com/forum/windows/88843/
static const char alphanum[] =
"abcdefghijklmnopqrstuvwxyz";
int stringLength = sizeof(alphanum) - 1;
std::string genRndStrt(){
    std::string rnd_str;
    for(unsigned int i = 0; i < 26; ++i){
        char c = alphanum[getRnd() % stringLength];
        std::string s(1, c);
        //std::cout << "character found is: " << s << std::endl;
        rnd_str = rnd_str + s;
    }
    return rnd_str;
}

int main (int argc, char **argv)
{
    //Optain the command line arguments for the program
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
    std::cout << "s = " << s << ", "
              << "n = " << n << ", "
              << "l = " << l << ", "
              << "c = " << c << std::endl;
    }


    if (optind < argc) {
        std::cout << "Found positional arguments\n";
        for (index = optind; index < argc; index++)
            std::cout << "Non-option argument: " << argv[index] << "\n";
    }

    int i=0;
    while(i < 20){
        i++;
        std::cout << "random street name: " << genRndStrt() << std::endl;
        sleep(1);
    }
}