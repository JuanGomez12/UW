#include <iostream>
#include <fstream>
#include <sstream>
#include <string>

#include <unistd.h>

//Initialize default values for s, n, l and c
int s = 10;
int n = 5;
int l = 5;
int c = 20;
bool verbose = false;




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
        std::cout << "s = " << s << ", "
                << "n = " << n << ", "
                << "l = " << l << ", "
                << "c = " << c << std::endl;
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

    bool print =true;
    while (print){
        std::cout << "a \"vertical Street\" (20,20)(20,30)"<< std::endl;
        std::cout << "a \"Horizontal Street\" (19,25)(29,25)"<< std::endl;
        std::cout << "g"<< std::endl;
        if (verbose){
            outputFile << "printed streets and asked for graph" << std::endl;
            outputFile.close();
        }
        sleep(2);
        std::cout << "r \"vertical Street\"" << std::endl;
        std::cout << "r \"Horizontal Street\"" << std::endl;
        std::cout << "g"<< std::endl;
        sleep(10);
        //print = false;
    }
/*
// open /dev/urandom to read
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
    std::cout << "Random character: " << (unsigned int)ch << "\n";

    // read another 8-bit value
    urandom.read(&ch, 1);
    std::cout << "Random character: " << (unsigned int)ch << "\n";

    int createRand = true;
    int i=1;
    while (createRand){
    // read a random unsigned int
    unsigned int num = i;
    urandom.read((char*)&num, sizeof(int));
    std::cout << "Random character: " << num << "\n";
    i++;
        if (i>200){
            createRand = false;
        }
    }
    // close random stream
    urandom.close();
    */
    return 0;
}