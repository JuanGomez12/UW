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

/// Entry point of process A
int procA(void) {
    // Process A writing to C
    for (int i = 0; i < 100; i++)
    {
        std::cout << "Hi" << std::endl;
        usleep(5000);
    }
    std::cout << "[A] Sleeping" << std::endl;
    sleep(6);
    std::cout << "[A] Exiting" << std::endl;
    return 0;
}

/// Entry point of process B
int procB(void) {
    // Process B writing to C
    while (!std::cin.eof()) {
        // read a line of input until EOL and store in a string
        std::string line;
        std::getline(std::cin, line);
        if (line.size () > 0)
            std::cout << line << std::endl;
    }
    std::cout << "[B] saw EOF" << std::endl;
    return 0;
}

/// Entry point of process C
int procC(void) {
    // Process C reading from both A and B
    while (!std::cin.eof()) {
        // read a line of input until EOL and store in a string
        std::string line;
        std::getline(std::cin, line);
        if (line.size () > 0)
            std::cout << "[C]: " << line << std::endl;
    }
    return 0;
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



//Forking
    // create a pipe
    std::vector<pid_t> kids;

    //----------------------------------------------------------------------------------------------------------------------------------------
    //rgen process and pipes
    int rgen_to_A1[2];
    pipe(rgen_to_A1);

    //Construct command line arguments
    char* rgen_argv[10];

    rgen_argv[0] = (char*)"rgen";
    rgen_argv[1] = (char*)"-s";
    rgen_argv[2] = (char*)s;
    rgen_argv[3] = (char*)"-n";
    rgen_argv[4] = (char*)n;
    rgen_argv[5] = (char*)"-l";
    rgen_argv[6] = (char*)l;
    rgen_argv[7] = (char*)"-c";
    rgen_argv[8] = (char*)c;
    rgen_argv[9] = nullptr;
    if (verbose){
        std::cout << "[exec] executing '/mnt/c/c code/build/rgen' using execv" << std::endl;
    }

    pid_t child_pid;
    child_pid = fork ();
    if (child_pid == 0) {
        //sleep (4);
        //Configure pipes for rgen_to_A1
        close(rgen_to_A1[0]);
        dup2(rgen_to_A1[1], STDOUT_FILENO);
        close(rgen_to_A1[1]);
        execv ("/mnt/c/c code/build/rgen", rgen_argv);

        // execl("/bin/ls", "ls", "-l", nullptr);
        perror ("Error from arie");
        return 1;
    }
    else if (child_pid < 0) {
        std::cerr << "Error: could not fork\n";
        return 1;
    }
    kids.push_back(child_pid);
    //------------------------------------------------------------------------------------------------------------------------------------
    //Assignment 1 process and pipes
    int A1_to_A2[2];
    pipe(A1_to_A2);

    //Construct command line arguments
    char* a1_argv[2];
    a1_argv[0] = (char*)"ece650-a1.py";
    a1_argv[2] = nullptr;
    if (verbose){
        std::cout << "[exec] executing './ece650-a1.py' using execv" << std::endl;
    }

    child_pid = fork ();
    if (child_pid == 0) {
        //sleep (4);
        //Configure pipes for rgen_to_A1
        close(rgen_to_A1[1]);
        dup2(rgen_to_A1[0], STDIN_FILENO);
        close(rgen_to_A1[0]);

        //Configure pipes for A1_to_A2
        close(A1_to_A2[0]);
        dup2(A1_to_A2[1], STDOUT_FILENO);
        close(A1_to_A2[1]);
        execv ("./ece650-a1.py", a1_argv);

        // execl("/bin/ls", "ls", "-l", nullptr);
        perror ("Error from arie");
        return 1;
    }
    else if (child_pid < 0) {
        std::cerr << "Error: could not fork\n";
        return 1;
    }
    kids.push_back(child_pid);

    //rgen I/O config in relation to A1
    close(rgen_to_A1[0]);
    close(rgen_to_A1[1]);
    //-------------------------------------------------------------------------------------------------------------------------------------
    //Assignment 2 process and pipes
    int driver_to_A2[2];
    pipe(driver_to_A2);

    //Construct command line arguments
    char* a2_argv[2];

    a2_argv[0] = (char*)"ece650-a2";
    a2_argv[1] = nullptr;
    if (verbose){
        std::cout << "[exec] executing '/mnt/c/c code/build/ece650-a2' using execv" << std::endl;
    }

    child_pid = fork ();
    if (child_pid == 0) {
        //sleep (4);
        //Pipe config in relation to driver
        close(driver_to_A2[1]);
        dup2(driver_to_A2[0], STDIN_FILENO);
        close(driver_to_A2[0]);

        //Pipe config in relation to A1
        close(A1_to_A2[1]);
        dup2(A1_to_A2[0], STDIN_FILENO);
        close(A1_to_A2[0]);
        execv ("/mnt/c/c code/build/ece650-a2", a2_argv);

        // execl("/bin/ls", "ls", "-l", nullptr);
        perror ("Error from arie");
        return 1;
    }
    else if (child_pid < 0) {
        std::cerr << "Error: could not fork\n";
        return 1;
    }
    kids.push_back(child_pid);

    //Driver I/O config in relation to A2
    close(driver_to_A2[0]);
    dup2(driver_to_A2[1], STDOUT_FILENO);
    close(driver_to_A2[1]);

    //A1_to_A2 pipe config
    close(A1_to_A2[1]);
    close(A1_to_A2[0]);
    
    //Driver input
    while (!std::cin.eof()) {
        // read a line of input until EOL
        std::string line;
        std::getline(std::cin, line);
        if (line.empty()) {
            continue;
        }
        std::cout << line << std::endl;
    }
    std::cout << "[A3]: Saw EOF" << std::endl;
    
    int res = procB();
    for (pid_t k : kids) {
        int status;
        kill (k, SIGKILL);
        waitpid(k, &status, 0);
    }
    std::cout << "A2 returned status: " << res << std::endl;

    return 0;
}