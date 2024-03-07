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

rem Start the backend server in a separate command prompt window
start "Backend Server" /B python app.py

rem Start the react server
echo Starting the react server

cd ../abaai-client

echo Installing node modules
npm install

echo Starting the frontend server
npm run dev

pause