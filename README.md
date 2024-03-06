# AbaAI

## Introduction
AbaAI is an ambitious project aimed at developing a sophisticated AI to excel at the Abalone board game. By exploring and implementing advanced heuristics and strategies, our AI seeks to achieve unparalleled mastery of the game.

## Project Goals
- To develop an AI that can consistently outperform human players in Abalone.
- To explore various heuristics and algorithms to find the most effective strategies for winning.
- To contribute to the AI and board game community by providing a fully open-source solution.

## Getting started

### Step 1: Clone the project to your computer

### Step 2: Start the backend Python server
1. Change directory to the `abaai-server` directory
    ```
    cd abaai-server
    ```
2. Initalize a python virtual environment
    ```
    python -m venv venv
    ```
3. Activate the virtual environment
    ```
    ./venv/Scripts/activate
    ```
4. Install the dependencies from the `requirements.txt` file
    ```
    pip install -r requirements.txt
    ```
5. Start the application server
    ```
    python app.py
    ```

### Step 3: Start the front end React server
1. Change directory to the `abaai-client` directory.
    ```
    cd abaai-client
    
    or
    
    cd ../abaai-client // if navigating from abaai-server directory
    ```
2. Install the node dependencies
    ```
    npm install
    ```
3. Start the React server
    ```
    npm run dev
    ```

### Step 4: Have fun!