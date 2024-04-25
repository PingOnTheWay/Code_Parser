# Code_Parser

This project provides a tool to parse the `main.py` script from the `test` directory and generate corresponding Python and shell scripts for execution on slurm systems.

## Getting Started

These instructions will help you get a copy of the project up and running on your local machine for development and testing purposes.

### Prerequisites

- Python 3.8 and above
- pm4py
- pickle
- Any additional libraries or tools if necessary.

### Installation

1. Clone the repository:

2. Navigate to the project directory:

### Usage

To parse the `main.py` script from the `test` folder and generate the required outputs, including Python and shell scripts executable on a slurm system, follow the steps below:

1. Navigate to the root directory of the project.

2. Execute the `parse.py` script. To execute the parse.py script with the necessary modifications, follow these steps:
   
   2.1 Modify the Python Interpreter Path: You will need to update the path to your Python interpreter on line 329 of the parse.py script. Locate the line where the Python command is set and replace the existing path with the path to the Python interpreter on your system. For example, if your Python interpreter is located at /usr/bin/python3, you should change the line to reflect this path.
   #### Before
   base_command = "/path/to/old/python /path/to/your/script.py"

   #### After
   base_command = "/usr/bin/python3 /path/to/your/script.py"
  
   2.2 Update SLURM Environment Addresses: On lines 360 and 381, update the addresses to match those in your SLURM environment. You'll need to ensure these paths are accessible and correct within the SLURM job context.

Modify the Python Interpreter Path: You will need to update the path to your Python interpreter on line 329 of the parse.py script. Locate the line where the Python command is set and replace the existing path with the path to the Python interpreter on your system. For example, if your Python interpreter is located at /usr/bin/python3, you should change the line to reflect this path.

3. After execution, check the output files (code blocks and shell scripts) in the `test` directory.

4. To perform testing with different input files, replace the contents of `main.py` in the `test` folder with contents from any of the five provided test files located in the `source_code_for_testing` directory.

### Additional Information

- The parser currently supports static forms of `for` loops, specifically in the format `for var in [0.1, 0.2, 0.3]`. This limitation arises due to the complexity of dynamically analyzing and parsing the abstract syntax tree (AST) for dynamic content.

- To successfully convert the `main.py` script in the `test` folder into executable scripts for slurm, execute the `parse.py` script located in the root directory. This will generate corresponding scripts in the `test` folder.

- Ensure that you adjust the permissions and configurations as required by your slurm system to avoid execution errors.

### Development

- The `parse.py` script uses the Abstract Syntax Tree (AST) module to analyze and transform the Python script into a structured format, making it easier to generate executable scripts based on the parsed content.

- The tool is designed to be flexible and extendable, allowing further enhancements such as adding support for more complex loop structures and dynamic code segments.
