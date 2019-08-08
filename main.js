const electron = require('electron');
const {app, BrowserWindow} = require('electron');

let menu = "main";

function createWindow(){
    let win = new BrowserWindow({
        width:1000,
        height:600,
        webPreferences:{
            nodeIntegration:true
        }
    });
    win.webContents.openDevTools();
    win.setMenu(null);
    win.loadFile(__dirname+`/html/${menu}.html`);

}

app.on('ready', createWindow);

// 전체적인 기능은 다 main.html에 있음