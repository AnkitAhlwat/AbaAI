@echo off

rem Start the flask server
echo Starting the flask server

rem Change directory to the abaai-server directory
cd abaai-server

echo Initializing virtual environment
python -m venv venv

echo Activating virtual environment
call venv\Scripts\activate

echo Installing requirements
pip install -r requirements.txt

rem Start the backend server
start /MIN cmd /C "python app.py"

rem Start the react server
echo Starting the react server

rem Change directory to the abaai-client directory
cd ../abaai-client

rem Debugging: Output the current directory
echo Current directory: %CD%

echo Installing node modules
npm install

rem Start the frontend server
start /MIN cmd /C "npm run dev"

echo App started
