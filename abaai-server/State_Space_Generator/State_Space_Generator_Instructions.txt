Generator.exe Instructions Manual

Running the Generator on Windows

1. Ensure 'generator.exe' and the 'input_files' and 'output_files' folders are in the same directory.

2. Prepare input files:
   - Input files must be in the format 'Test<#>.input', where '<#>' is any sequence of whole number (positive) digits. For example, 'Test1.input', 'Test2.input', etc.
   - Place these files into the 'input_files' folder.

3. Run the executable:
   - On Windows, simply double-click 'generator.exe' to run it. Alternatively, you can open Command Prompt, navigate to the directory containing 'generator.exe', and run it by typing './generator.exe' and pressing Enter.

4. Retrieve your output:
   - After 'generator.exe' finishes running, check the 'output_files' folder. You will find the generated files named corresponding to your input files, with '.game' and '.board' extensions. For example, for 'Test1.input', you will find 'Test1.game' and 'Test1.board'.



Running on MacOS

Preparing to Run the Generator:

1. Ensure you have the 'generator' executable in your desired directory, along with the 'input_files' and 'output_files' folders.

2. Place your input files, adhering to the naming format 'Test<number>.input' (e.g., 'Test1.input', 'Test2.input'), into the 	'input_files' folder.


Running the Generator:

1. Open the Terminal application. You can find it using Spotlight (Cmd + Space) by typing "Terminal" and pressing Enter.

2. Use the 'cd' command to navigate to the directory containing your 'generator' executable. Example:
cd /path/to/your/directory

3. Before running the executable for the first time, you may need to grant it execute permission. Run the following command:
chmod +x generator

4. To run the program, type:
./generator


Accessing the Output:

Check the 'output_files' folder after running the executable. You will find the results, named correspondingly to your input files but with '.game' and '.board' extensions (e.g., 'Test1.game', 'Test1.board').