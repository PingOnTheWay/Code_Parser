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

1. Navigate to the root directory of the project:

2. Execute the `parse.py` script:

3. After execution, check the output files (code blocks and shell scripts) in the `test` directory.

4. To perform testing with different input files, replace the contents of `main.py` in the `test` folder with contents from any of the five provided test files located in the `source_code_for_testing` directory.

### Additional Information

- The parser currently supports static forms of `for` loops, specifically in the format `for var in [0.1, 0.2, 0.3]`. This limitation arises due to the complexity of dynamically analyzing and parsing the abstract syntax tree (AST) for dynamic content.

- To successfully convert the `main.py` script in the `test` folder into executable scripts for slurm, execute the `parse.py` script located in the root directory. This will generate corresponding scripts in the `test` folder.

- Ensure that you adjust the permissions and configurations as required by your slurm system to avoid execution errors.

### Development

- The `parse.py` script uses the Abstract Syntax Tree (AST) module to analyze and transform the Python script into a structured format, making it easier to generate executable scripts based on the parsed content.

- The tool is designed to be flexible and extendable, allowing further enhancements such as adding support for more complex loop structures and dynamic code segments.
