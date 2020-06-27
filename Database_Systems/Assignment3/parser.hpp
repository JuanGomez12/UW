
#pragma once

#include <string>
#include <vector>

/**
 * Parses a command line.
 * Returns a character of a command and an optional argument depending on the command.
 * Returns true on success and false on a parsing error.
 * On error, err_msg contains the error message
 */
bool parse_line (const std::string &line,
                 char &cmd, int &argnum, std::vector<int> &numVec, std::string &err_msg);
