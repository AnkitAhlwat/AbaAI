@echo off

rem Start the flask server
cd abaai-server

echo Initializing virtual environment
python -m venv venv

echo Activating virtual environment
call venv\Scripts\activate

echo Installing requirements
pip install -r requirements.txt

echo Starting the backend server
python app.py


rem Start the react server
cd ../abaai-client

echo Installing node modules
npm install

echo Starting the frontend server
npm run dev

pause
