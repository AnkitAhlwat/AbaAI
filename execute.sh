#!/bin/bash

# Start the flask server
echo "Starting the flask server"

# Change directory to the abaai-server directory
cd abaai-server

echo "Initializing virtual environment"
python3 -m venv venv

echo "Activating virtual environment"
source venv/bin/activate

echo "Installing requirements"
pip install -r requirements.txt

echo "Starting the backend server"
python app.py

# Start the react server
echo "Starting the react server"

cd ../abaai-client

echo "Installing node modules"
npm install

echo "Starting the frontend server"
npm run dev
