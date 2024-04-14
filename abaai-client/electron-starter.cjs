const { app, BrowserWindow, protocol } = require('electron');
const path = require('path');

let mainWindow;
const preloadPath = path.join(process.resourcesPath, 'app.asar.unpacked', 'preload.js');

function createWindow() {
  mainWindow = new BrowserWindow({
    width: 800,
    height: 600,
    webPreferences: {
      nodeIntegration: true, // consider security implications
      contextIsolation: false, // for security, usually set to true
      preload: preloadPath
    }
  });

  // Correct path for loading index.html with file protocol
  mainWindow.loadURL(`file://${path.join(process.resourcesPath, 'dist', 'index.html')}`);

  mainWindow.on('closed', () => {
    mainWindow = null;
  });
}

// Register custom protocol once
app.whenReady().then(() => {
  protocol.registerFileProtocol('app', (request, callback) => {
    const url = request.url.replace(/^app:\/\//, '');
    callback({ path: path.normalize(`${__dirname}/${url}`) });
  });
  
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
