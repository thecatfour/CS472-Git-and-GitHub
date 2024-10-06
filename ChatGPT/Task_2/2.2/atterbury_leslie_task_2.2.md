# Documentation: Bash Script for Espresso Compiler Unit Testing

## Overview
This Bash script is used to run unit tests for a specified version of an Espresso compiler.
The script organizes the results of these tests into appropriate directories for different versions of Espresso, namely `Espresso`, `Espresso_Plus`, and `Espresso_Star`. 
It handles both "Good" and "Bad" test cases for each version and outputs the test results into separate files.

## Usage
To use this script, follow these steps:

1. **Enter the compiler name**: 
   When the script runs, it will prompt you to enter the name of the compiler you want to test. 
   This name will be used to generate a results folder and will be referenced throughout the testing process.

   ```bash
   Enter compiler name: <CompilerName>
   ```

2. **Delete old data**: 
   The script will automatically delete any previous results folder for the specified compiler to ensure a fresh start.

3. **Generate directory structure**:
   - The script will create new directories to organize the tests and results.
   - For each Espresso version (`Espresso`, `Espresso_Plus`, `Espresso_Star`), the script will create separate `Good` and `Bad` folders where the corresponding test results will be stored.
   
   After this step, your folder structure will look like:
   ```
   <CompilerName>Results/
   ├── Espresso/
   │   ├── Good/
   │   └── Bad/
   ├── Espresso_Plus/
   │   ├── Good/
   │   └── Bad/
   └── Espresso_Star/
       ├── Good/
       └── Bad/
   ```

4. **Run the tests**: 
   The script uses the function `doTests()` to run unit tests. It does the following for each category (`GoodTests` and `BadTests`) and for each version of Espresso:
   - Checks if any tests are present in the specified directory (e.g., `./tests/Espresso/GoodTests`).
   - If tests are found, it iterates over the test files, runs the compiler on each test file, and captures the output in a corresponding `.txt` file.
   - These output files are then moved to the appropriate folder (`Good` or `Bad`) under the relevant Espresso version directory.

### Parameters in the `doTests()` function:

- **$1**: The test type (`GoodTests` or `BadTests`).
- **$2**: The name of the compiler entered by the user.
- **$3**: The output file path where results will be stored.
- **$4**: The Espresso version type (`Espresso`, `Espresso_Plus`, or `Espresso_Star`).

For example, the following command runs the "Good" tests for the `Espresso` version:
```bash
doTests GoodTests $COMPILERNAME "$COMPILERNAME"Results/Espresso/Good Espresso
```

### Test Output:
The output for each test is written into a `.txt` file, named according to the test's filename (without the extension). 
Each result is stored in the appropriate directory (`Good` or `Bad`), based on the test type and Espresso version.

## Directory for Test Files
Your tests should be located in the following structure:
```
tests/
├── Espresso/
│   ├── GoodTests/
│   └── BadTests/
├── Espresso_Plus/
│   ├── GoodTests/
│   └── BadTests/
└── Espresso_Star/
    ├── GoodTests/
    └── BadTests/
```
The script will look for test files within these directories and will execute the tests accordingly.

## Example
If you have a compiler named `EspressoCompiler`, and test files in the following locations:
- `tests/Espresso/GoodTests/test1.esp`
- `tests/Espresso/BadTests/test2.esp`

You would:
1. Run the script.
2. Enter the compiler name `EspressoCompiler` when prompted.
3. The script will create a folder `EspressoCompilerResults/` and organize the test results into:
   ```
   EspressoCompilerResults/
   ├── Espresso/
   │   ├── Good/
   │   │   └── test1.txt
   │   └── Bad/
   │       └── test2.txt
   ├── Espresso_Plus/
   ├── Espresso_Star/
   ```

The contents of `test1.txt` and `test2.txt` will be the output of running the `EspressoCompiler` on those test files.

## Error Handling
If no tests are found in the expected directory (e.g., `./tests/Espresso/GoodTests`), the script will output:
```
No tests in ./tests/Espresso/GoodTests were found.
```

## Conclusion
This script automates the process of running unit tests for different versions of the Espresso compiler. 
By specifying the compiler name, the script generates directories for the results, runs both "Good" and "Bad" tests, and stores the outputs in an organized manner.