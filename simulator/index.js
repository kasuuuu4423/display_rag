const electron = require('electron');
const app = electron.app;
const BrowserWindow = electron.BrowserWindow;
const { ipcMain } = require('electron');

let mainWindow = null;

app.on('window-all-closed', function() {
  if (process.platform !== 'darwin') {
    app.quit();
  }
});

app.on('ready', function() {
  mainWindow = new BrowserWindow({width: 800, height: 600, webPreferences: {
    nodeIntegration: true,
  }});
  mainWindow.loadURL('file://' + __dirname + '/render.html');
  mainWindow.openDevTools();

  mainWindow.on('closed', function() {
    mainWindow = null;
  });

  let PORT = 10001;
  let HOST = '127.0.0.1';

  let dgram = require('dgram');
  let server = dgram.createSocket('udp4');

  server.on('listening', function () {
    let address = server.address();
    console.log('UDP Server listening on ' + address.address + ":" + address.port);
  });

  server.on('message', function (msg, remote) {
    mainWindow.webContents.send('msg', msg);
    let decode = new TextDecoder().decode(msg);
    if(decode.startsWith('/init/')){
      let ack = new Buffer("1");
      server.send(ack, 0, ack.length, 11001, '127.0.0.1', function(err, bytes) {
      });
    }
  });
  server.bind(PORT, HOST);
});

