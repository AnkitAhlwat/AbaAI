const { app, BrowserWindow } = require('electron');
const { spawn } = require('child_process');

let mainWindow;
let flaskProcess = null;
let viteServer = null;

function createViteServer() {
  viteServer = spawn('npm', ['run', 'dev'], { shell: true, stdio: 'inherit', cwd: __dirname });

  viteServer.on('close', code => {
    console.log(`Vite server exited with code ${code}`);
  });
}

function runServer() {
  flaskProcess = spawn('./app.exe', [], { shell: true });
  flaskProcess.stdout.on('data', data => {
    console.log(`Flask: ${data}`);
  });
}

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

  mainWindow.on('closed', () => {
    mainWindow = null;
    if (flaskProcess) flaskProcess.kill();
    if (viteServer) viteServer.kill();
  });

}

app.whenReady().then(() => {
  runServer();
  createViteServer();
  createWindow();
});

app.on('window-all-closed', () => {
  if (process.platform !== 'darwin') {
    app.quit();
  }
});

app.on('activate', () => {
  if (BrowserWindow.getAllWindows().length === 0) {
    createWindow();
  }
});