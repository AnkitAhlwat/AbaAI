const { app, BrowserWindow } = require('electron');
const { spawn } = require('child_process');

let flaskProcess = null;

function createWindow() {
  mainWindow = new BrowserWindow({
    width: 800,
    height: 600,
    webPreferences: {
      nodeIntegration: true,
      contextIsolation: false,
    }
  });

  const startURL = 'http://localhost:5173';

  mainWindow.loadURL(startURL);
  mainWindow.on('closed', function () {
    mainWindow = null;
  });
// Start Flask server
flaskProcess = spawn('path/to/your/flask/executable', [], { shell: true });
flaskProcess.stdout.on('data', (data) => {
  console.log(`Flask: ${data}`);
});
}

app.on('ready', createWindow);

app.on('window-all-closed', function () {
  if (flaskProcess) flaskProcess.kill();
  if (process.platform !== 'darwin') {
    app.quit();
  }
});

app.on('activate', function () {
  if (BrowserWindow.getAllWindows().length === 0) {
    createWindow();
  }
});
