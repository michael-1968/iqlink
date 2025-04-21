import figures from './figures.js';
import Figure from './figure.js';
import {filename, htmlGET, htmlPOST} from './dataexchange.js'
import localStorageHandler from './localStorageHandler.js'


document.getElementById('LoadSave').style.display = 'none';
document.getElementById('dateiname-form').style.display = '';

var loadOrSaveMethod = null

// window.addEventListener('beforeunload', () => saveButtonNames());


// lädt die Figuren
figures.showFigures(document);
//showSetup();

// die Referenz zu den LoadSave-Buttons 
const loadSaveButtons = Array.from(document.getElementsByClassName('loadsavebutton')); 

// lädt die Beschriftungen der Buttons
loadButtonNames() 

// not needed (spare button)
function set() {
    console.log("set");
}

function loadButtonClicked() {
    document.getElementById('LoadSave').style.display = '';
    document.getElementById('dateiname-form').style.display = 'none';
    loadSaveButtons.forEach(button => {
        if (button.innerHTML === "..") {
            button.style.display = 'none';
        }
        else button.style.display = '';
        }
    );
    loadOrSaveMethod = onLoadButtonClick
}

function saveButtonClicked() {
    document.getElementById('LoadSave').style.display = '';
    document.getElementById('dateiname-form').style.display = '';
    loadSaveButtons.forEach(button => {
        button.style.display = '';
        }
    );
    loadOrSaveMethod = onSaveButtonClick
}

function onLoadButtonClick(button, name) {
    var fn = button.innerHTML;
    loadButtonNames();
    loadSetup(fn)
}

function onSaveButtonClick(button, fn) {
    if (fn == '') {
        if (button.innerHTML != '..') {
            saveSetup(button.innerHTML);
            saveButtonNames();
        };
    }
    else {
        button.innerHTML = fn
        document.getElementById('Input-Dateiname').value = '';
        saveSetup(fn);
        saveButtonNames();
    }
}

function saveButtonNamesOLD() {
    console.log("saveButtonNames");
    const buttonInnerHTMLs = Array.from(loadSaveButtons).map(button => button.innerHTML);
    const buttonnames = JSON.stringify(buttonInnerHTMLs);
    localStorage.setItem('buttonnames', buttonnames);
    saveButtonNamesNEW()
}

function saveButtonNames() {
    const buttonInnerHTMLs = Array.from(loadSaveButtons).map(button => button.innerHTML);
    var buttonnames = {};
    buttonInnerHTMLs.forEach((innerHTML, index) => {
        buttonnames[index] = innerHTML;
    });
    console.log("save", buttonnames);
    htmlPOST('http://localhost:8000/setup/save/buttonnames/', buttonnames)
        .then(result => {
            if (result == null) {
                console.error("Error forwarding Save-click");
            }
        })
}


function loadButtonNamesOLD() {
    console.log("loadButtonNames");
    const buttonnames = localStorage.getItem('buttonnames');
    if (buttonnames) {
        const buttonInnerHTMLs = JSON.parse(buttonnames);
        // Optionally, you can set the innerHTML of the buttons back
        buttonInnerHTMLs.forEach((innerHTML, index) => {
            if (loadSaveButtons[index]) {
                loadSaveButtons[index].innerHTML = innerHTML;
            }
        });
    }
}

function loadButtonNames() {
    var data;
    const url = "http://localhost:8000/setup/load/buttonnames/";
    htmlGET(url, "")
        .then(result => {
            if (result !== null) {
                data = result;  
                console.log("loadButtonNames-Data: ", result);
                Object.keys(data).forEach((index) => {
                    loadSaveButtons[index].innerHTML = data[index];
                });
            } else {
                console.error("Error on loading");
            }
        });
}

function loadSetup(name) {
    var data;
    console.log("load", name);
    const url = `http://localhost:8000/setup/load?filename=${encodeURIComponent(name)}`;
    htmlGET(url, "")
        .then(result => {
            if (result !== null) {
                data = result;
                localStorageHandler.deleteAll();
                figures.removeImages(document);
                const figuresToShowArray = Object.values(data);
                figuresToShowArray.forEach((item) => {
                    let fx = new Figure(item.name, item.position, item.rotation, document);
                    localStorageHandler.updateEntry(fx);
                });
            } else {
                console.error("Error on loading");
            }
        });
}

function saveSetup(name) {
    console.log("save", name);
    var setupData = figures.getFigureMemoryAsJson();
    htmlPOST('http://localhost:8000/setup/save/', {"name": name, "setup": setupData})
        .then(result => {
            if (result == null) {
                console.error("Error forwarding Save-click");
            }
        })
    document.getElementById('LoadSave').style.display = 'none';
    document.getElementById('dateiname-form').style.display = 'none';
}

function run() {
    console.log("run");
    // das Setup der Figuren
    var testdata = figures.getFigureMemoryAsJson();
    htmlPOST('http://localhost:8000/setup/receive/', testdata)
        .then(result => {
            if (result == null) {
                console.error("Error forwarding the setup before starting the calculation");
            }
        }).then(() => {
            htmlPOST('http://localhost:8000/calculation/', {cmd: 'run'})
                .then(result => {
                    if (result == null) {
                        console.error("Error forwarding the run-command");
                    }
                })
            })
}

function about() {
    var status = document.getElementById('AboutText').style.display;

    if (status === 'none') {
        fetch('about.html')
            .then(response => response.text()) // 'response' is the HTTP response object
            .then(data => { // 'data' is the text content extracted from the response
                document.getElementById('AboutText').style.display = '';
                document.getElementById('AboutText').innerHTML = data;
                document.getElementById('About').innerHTML = "Fertig"
                document.getElementById('BrettImage').style.display = 'none';
                hideImages('none');
                document.getElementById('Buttons').style.display = 'none';
            })
            .catch(error => console.error('Error loading about.html:', error));
    } else {    
        document.getElementById('AboutText').style.display = 'none';
        document.getElementById('BrettImage').style.display = '';
        hideImages('');
        document.getElementById('Buttons').style.display = '';
        document.getElementById('About').innerHTML = "About"
    }
}

// Funktion zum Verstecken aller Figuren
function hideImages(status) {
    const images = document.querySelectorAll('img');
    images.forEach(image => {
        if (filename(image.src) != "Brett") {
           image.style.display = status;
        }
   });
}

// Event-Listener für die Buttons 
document.getElementById('Set').addEventListener('click', set);
document.getElementById('Load').addEventListener('click', loadButtonClicked);
document.getElementById('Save').addEventListener('click', saveButtonClicked);
document.getElementById('Run').addEventListener('click', run);
document.getElementById('About').addEventListener('click', about);

document.getElementById('AboutText').style.display = 'none';
document.getElementById('Message').style.visibility = 'hidden';
document.getElementById('About2').style.visibility = 'hidden';


// Event-Listener der Buttons für das Laden uns Speichern. 
// Die Buttons werden durch ihre Beschriftung unterschieden.
loadSaveButtons.forEach(button => {
    button.addEventListener('click', function() {
        var newFilename = document.getElementById('Input-Dateiname').value.substring(0, 26);
        loadOrSaveMethod(button, newFilename);
    });
});

