  
cmake_minimum_required(VERSION 2.8)
project(ece650-a3)

## ECE650 Specific configuration start here
## Project specific configurations go here

# enable c++11 support
set (CMAKE_CXX_FLAGS "-std=c++11 -Wall ${CMAKE_CXX_FLAGS}")
set(CMAKE_INSTALL_PREFIX ${CMAKE_BINARY_DIR}/run)
# Enable clang-tidy with all the checks except fuchsia default arguments
# set(CMAKE_CXX_CLANG_TIDY "clang-tidy;-checks=*,-fuchsia-default-arguments")

# create the main executable
## add additional .cpp files if needed
add_executable(ece650-a2 ece650-a2.cpp parser.cpp graph.cpp)
add_executable(rgen rgen.cpp)
add_executable(ece650-a3 driver.cpp)
add_executable(ece650-a3-test driverTest.cpp)
add_executable(a1runtest a1run_test.cpp)

# create the executable for tests
add_executable(tests test.cpp)
install(PROGRAMS ece650-a1.py DESTINATION bin)
install(TARGETS rgen ece650-a2 ece650-a3 ece650-a3-test a1runtest RUNTIME DESTINATION bin)