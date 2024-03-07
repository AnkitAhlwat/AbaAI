# Start the flask server
Write-Output "Starting the flask server"

# Change directory to the abaai-server directory
Set-Location abaai-server

Write-Output "Initializing virtual environment"
python -m venv venv

Write-Output "Activating virtual environment"
.\venv\Scripts\Activate.ps1

Write-Output "Installing requirements"
pip install -r requirements.txt

# Start the backend server in a separate PowerShell window
Start-Process -FilePath "python" -ArgumentList "app.py" -NoNewWindow

# Start the react server
Write-Output "Starting the react server"

Set-Location ../abaai-client

Write-Output "Installing node modules"
npm install

Write-Output "Starting the frontend server"
npm run dev

Write-Output "Process completed. Press any key to continue..."
pause
