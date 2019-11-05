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
bool verbose = false;


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
    std::vector<pid_t> running_proc;
    pid_t child_pid;

    //int rgen_input[2];
    //pipe(rgen_input);

    int A1_input[2];
    pipe(A1_input);

    int A2_input[2];
    pipe(A2_input);


//Assignment 1 process and pipes

    //Construct command line arguments
    char* a1_argv[2];
    a1_argv[0] = (char*)"ece650-a1.py";
    a1_argv[1] = nullptr;
    if (verbose){
        std::cout << "[A3] executing './ece650-a1.py' using execv" << std::endl;
    }
    child_pid = fork ();
    if (child_pid == 0) {
        //Close rgen_input pipes
        //close(rgen_input[1]);
        //close(rgen_input[0]);
        //Configure rgen to A1 pipes
        dup2(A1_input[0], STDIN_FILENO);
        close(A1_input[1]);
        close(A1_input[0]);
        //Configure A1 to A2 pipes
        dup2(A2_input[1], STDOUT_FILENO); //Duplicate the standard output
        close(A2_input[0]); //Close the input side of the pipe
        close(A2_input[1]); //Close the output side of the pipe
        //Run A1
        execv ("./ece650-a1.py", a1_argv);
        perror ("Error from A1");
        return 1;
    }
    running_proc.push_back(child_pid);
    //----------------------------------------------------------------------------------------------------------------------------------------
    //rgen process and pipes




    //int A2_to_All[2];
    //pipe(A2_to_All);


    
    //Construct command line arguments
    
    char* rgen_argv[10];

    //Based on answer found in https://stackoverflow.com/a/3446272.
    //Configure the buffers
    char sprintf_buffer1[20];
    char sprintf_buffer2[20];
    char sprintf_buffer3[20];
    char sprintf_buffer4[20];
    sprintf (sprintf_buffer1, "%d", s);
    sprintf (sprintf_buffer2, "%d", n);
    sprintf (sprintf_buffer3, "%d", l);
    sprintf (sprintf_buffer4, "%d", c);
    

    rgen_argv[0] = (char*)"rgen";
    rgen_argv[1] = (char*)"-s";
    rgen_argv[2] = sprintf_buffer1;
    rgen_argv[3] = (char*)"-n";
    rgen_argv[4] = sprintf_buffer2;
    rgen_argv[5] = (char*)"-l";
    rgen_argv[6] = sprintf_buffer3;
    rgen_argv[7] = (char*)"-c";
    rgen_argv[8] = sprintf_buffer4;
    rgen_argv[9] = nullptr;
    
    ///*
    /*

    */

    // char* rgen_argv[2];
    // rgen_argv[0] = (char*)"rgen";
    // rgen_argv[1] = nullptr;
   //*/
    if (verbose){
        std::cout << "[A3] executing './rgen' using execv" << std::endl;
    }

    child_pid = fork ();
    if (child_pid == 0) {
        //sleep (4);
        //Configure pipes for rgen input
        //dup2(rgen_input[0], STDIN_FILENO);
        //close(rgen_input[1]);
        //close(rgen_input[0]);
        //Configure pipes for A1_input
        dup2(A1_input[1], STDOUT_FILENO);
        close(A1_input[0]);
        close(A1_input[1]);
        //Close A2_input
        close(A2_input[0]);
        close(A2_input[1]);
        execv ("./rgen", rgen_argv);

        // execl("/bin/ls", "ls", "-l", nullptr);
        perror ("Error from rgen");
        return 1;
    }
    else if (child_pid < 0) {
        std::cerr << "Error: could not fork\n";
        return 1;
    }
    running_proc.push_back(child_pid);
    
    //------------------------------------------------------------------------------------------------------------------------------------
    
    


    child_pid = fork ();
    if (child_pid == 0) {//run input controller
        //Configure rgen pipe
        //dup2(rgen_input[1], STDOUT_FILENO);
        //close(rgen_input[0]);
        //close(rgen_input[1]);
        //Configure A2 pipe
        dup2(A2_input[1], STDOUT_FILENO);
        close(A2_input[0]);
        close(A2_input[1]);
        //Configure A1 pipe
        close(A1_input[0]);
        close(A1_input[1]);

        while (!std::cin.eof()) {
            // read a line of input until EOL and store in a string
            
            std::string line;
            std::getline(std::cin, line);
            std::cout << line << std::endl;
        }
        if (verbose){
            std::cerr <<"[inputController]: Saw EOF" << std::endl;
        }
        
        //pid_t parent_pid = getppid();
        //running_proc.push_back(parent_pid);
        //sleep(10);
        for (pid_t k : running_proc) {
            int status;
            kill (k, SIGTERM);
            waitpid(k, &status, 0);
        }
        return 0;
    }
    running_proc.push_back(child_pid);
    //------------------------------------------------------------------------------------------------------------------------------------
    //Assignment 2 process and pipes

    //A2 process
    //First configure the pipes
    //Configure pipes from A2 to rgen
    //close(rgen_input[1]);
    //close(rgen_input[0]);

    //Close the A1 input pipes
    close(A1_input[1]);
    close(A1_input[0]);

    //Config pipe to input of A2
    dup2(A2_input[0], STDIN_FILENO);
    close(A2_input[1]);
    close(A2_input[0]);

    char* a2_argv[2];
    a2_argv[0] = (char*)"ece650-a2";
    a2_argv[1] = nullptr;
    if (verbose){
        std::cout << "[A3] executing './ece650-a2' using execv" << std::endl;
    }
    
    execv ("./ece650-a2", a2_argv);
    perror ("Error from A2");
    return 1;
    return 0;
}