# Introduction

## Requirements

- Ubuntu 18.04
- Python 3.6.9

## Structure

- `documents`: contains test instructions 
- `input_data`: includes all input CSV files
- `output_data`: includes all output CSV files
- `solution`: contains the source code

# Usage

## Running the Program

1. Extract the zip file and navigate to the `solution` directory
2. Execute the program by running `python robot_scheduler.py`
3. The console will provide a shortcut result of the total time spent by each robot.

## Expected Output

The program takes all input CSV files from the `input_data` directory and generates two output CSV files in the `out_data` directory. The `robot_info.csv` file reports the time each robot takes to complete its path, and the `platform_info.csv` file reports the visitors to each node.

# Potential Improvements

- Used Python to speed up development; however, in a production environment, it would be advisable to use C++.
- Further abstraction of the `Platform` and `RobotScheduler` classes can help modularize the FSM algorithm function.
- To improve efficiency and readability, `robots` can be implemented using priority queue instead of list.


