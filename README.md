# AbaAI

## Introduction

AbaAI is an ambitious project aimed at developing a sophisticated AI to excel at the Abalone board game. By exploring and implementing advanced heuristics and strategies, our AI seeks to achieve unparalleled mastery of the game.

## Project Goals

- To develop an AI that can consistently outperform human players in Abalone.
- To explore various heuristics and algorithms to find the most effective strategies for winning.
- To contribute to the AI and board game community by providing a fully open-source solution.

## Application Website

You can access the application via the following url:

[Aba AI](https://aba-ai.vercel.app/)

NOTE: This is hosted using a free cloud hosting service, and may not respond properly all the time.

## Running the State-Space Generator

*Simplified instructions in GENERATOR_INSTRUCTIONS.md

Can be run from AbaAI/abaai-server/State_Space_Generator/state_space_generator.exe directly without the need for downloading if the repo is cloned (instructions below)

### Prerequisites

- Working Test.input files

### Step 1: Download State_Space_Generator.zip

1. Locate the file

```
On the repository main page, find State_Space_Generator.zip
Alternatively, it may be located in:
".\AbaAI\abaai-server\abalone\ai\State_Space_Generator.zip"
```

2. Download and unzip the file

```
Can be dowloaded directly in the directry if the repository is cloned, unzip the file by right-clicking it and selecting "Extract All..."
Alternatively, select the .zip folder in the repository, then in the github code file header select the dowload icon 
```

3. Insert input files and run the Executable

```
Navigate into the downloaded "State_Space_Generator" folder
Insert as many Test<#>.input files in the "input_files" folder as desired
Run the executable by double-clicking it, or by opening the command prompt in the "State_Space_Generator" and typing:
"state_space_generator_main.exe"
```

4. Find output files

```
Navigate to the "output_files" folder to find the Test<#>.move and Test<#>.board files for all input files
```

## Local Installation

### Prerequisites

- Python 3.11 or higher is installed on your computer. [Install Python Here](https://www.python.org/downloads/?trk=cndc-detail)
- Node 20.11 or higher is installed on your computer. [Install Node Here](https://nodejs.org/en/download/)

### Step 1: Clone the project to your computer and navigate to directory

```
git clone <project url> <directory name>
cd <directory name>
```

### Step 2: Start the backend Python server

1. Change directory to the `abaai-server` directory

    ```
    cd abaai-server
    ```

2. Initalize a python virtual environment

- Windows

    ```
    python -m venv venv
    ```

- Linux/MacOS

    ```
    python3 -m venv venv
    ```

3. Activate the virtual environment

- Windows

    ```
    .\venv\Scripts\activate
    ```

- Linux/MaxOS

    ```
    source venv/bin/activate
    ```

4. Install the dependencies from the `requirements.txt` file

    ```
    pip install -r requirements.txt
    ```

5. Start the application server

- Windows

    ```
    python app.py
    ```

- Linux/MaxOS

    ```
    python3 app.py
    ```

### Step 3: Start the front end React server

1. Open a separate terminal window

2. Change directory to the `abaai-client` directory. (from root directory)

    ```
    cd abaai-client
    
    or
    
    cd ../abaai-client // if navigating from abaai-server directory
    ```

3. Install the node dependencies

    ```
    npm install
    ```

4. Start the React server

    ```
    npm run dev
    ```

### Step 4: Have fun
