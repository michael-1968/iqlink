
import { htmlGET, htmlPOST, filename, fetchVersion }  from "./dataexchange.js";
import Figure from './figure.js';
import figures from './figures.js';
import localStorageHandler from './localStorageHandler.js'
let nameOfLastClickedFigure = '';

// localStorageHandler.deleteAll();

figures.showFigures(document);

// die zu bearbeitende Figur
var fx = localStorageHandler.figure(nameOfLastClickedFigure);
console.log("fx: "+fx, nameOfLastClickedFigure);    

// die Referenz zu den Zellen 
const cells = Array.from(document.getElementsByClassName('figur')); 


// Event-Listener für die Buttons 
document.getElementById('Rotation-Plus').addEventListener('click', rotatePlus);
document.getElementById('Rotation-Minus').addEventListener('click', rotateMinus);
document.getElementById('Flip').addEventListener('click', flip);
document.getElementById('oben-links').addEventListener('click', obenlinks);
document.getElementById('oben-rechts').addEventListener('click', obenrechts);
document.getElementById('links').addEventListener('click', links);
document.getElementById('rechts').addEventListener('click', rechts);
document.getElementById('unten-links').addEventListener('click', untenlinks);
document.getElementById('unten-rechts').addEventListener('click', untenrechts);
document.getElementById('back').addEventListener('click', back);
document.getElementById('off').style.visibility = 'hidden';
document.getElementById('Lady').innerHTML = 'Clear All';
document.getElementById('Lady').addEventListener('click', clear);
document.getElementById('done').addEventListener('click', done);
document.getElementById('Message').style.visibility = 'hidden';

// Event-Listener der Zellen und Platzieren der Figuren. 
// Die Buttons werden durch den Dateinamen der Images identifizert, nicht durch deren ID.
cells.forEach(image => {
    image.addEventListener('click', function() {
        var fn = filename(image.src);
        var fxx = figures.getFigure(fn);
        console.log("Setuplisteners - getFigure: ", fn, fxx);
        nameOfLastClickedFigure = fn;
        if (fxx === undefined) {
            fx = new Figure(fn, {"X": 1, "Y": 1}, {"rotX": 0, "rotY": 0, "rotZ": 0}, document); 
            figures.addFigure(fx);     
        }
        else {
            console.log("Setuplisteners - refresh figure: ", fxx, fn, fxx.calculationPosition, fxx.calculationRotation);
            // if (fx !== undefined) {
            //         figures.removeFigure(fx);
            //     }
            console.log("Setuplisteners - removeImagesByFilename: ", fn);    
            removeImagesByFilename(fn);        
            fx = new Figure(fn, fxx.calculationPosition, fxx.calculationRotation, document);
            figures.addFigure(fx);
            console.log("Setuplisteners - new figure: ", fx);
        }
    });
});

// Rotationen
function rotatePlus() {
    fx.rotate({"rotX": 0, "rotY": 0, "rotZ": 60});
    removeMessage();
    localStorageHandler.updateEntry(fx);
}
function rotateMinus() {
    fx.rotate({"rotX": 0, "rotY": 0, "rotZ": -60});
    removeMessage();
    localStorageHandler.updateEntry(fx);
}
function flip() {
    fx.rotate({"rotX": 180, "rotY": 0, "rotZ": 0});
    removeMessage();
    localStorageHandler.updateEntry(fx);
}

// Bewegungen
function obenlinks() {
    fx.move({"X": -1, "Y": -1});
    removeMessage();
    localStorageHandler.updateEntry(fx);
}
function obenrechts() {
    fx.move({"X": +1, "Y": -1});
    removeMessage();
    localStorageHandler.updateEntry(fx);
}
function links() {
    fx.move({"X": -1, "Y": 0});
    removeMessage();
    localStorageHandler.updateEntry(fx);
}
function rechts() {
    fx.move({"X": +1, "Y": 0});
    removeMessage();
    localStorageHandler.updateEntry(fx);
}
function untenlinks() {
    fx.move({"X": -1, "Y": +1});
    removeMessage();
    localStorageHandler.updateEntry(fx);
}
function untenrechts() {
    fx.move({"X": +1, "Y": +1});
    removeMessage();
    localStorageHandler.updateEntry(fx);
}

function back() {
    console.log("back: ", fx);
    removeMessage();
    figures.removeFigure(fx);
    figures.removeImages(document);
    figures.showFigures(document);
}

function clear() {
    removeMessage();
    figures.clearMemory();
    figures.removeImages(document);
}

function done() {
    console.log("Done");
    // das Setup der Figuren
    var testdata = figures.getFigureMemoryAsJson();
    htmlPOST('http://localhost:8000/setup/receive/', testdata)
        .then(result => {
            if (result == null) {
                console.error("Error forwarding Done-click");
            } else {
                console.log("Done-click: ", result);
                if (result.status != "OK") {
                    document.getElementById('Message').style.visibility = 'visible';
                    document.getElementById('Message').innerHTML = result.message;
                } else {
                    removeMessage();
                    window.location.href = "index.html";  
                    // springt zum Hauptfenster    
                }
            }
        })
}

// Funktion zum Entfernen von Bildern mit einem bestimmten Dateinamen
function removeImagesByFilename(targetFilename) {
    const images = document.querySelectorAll('img');
    images.forEach(image => {
//        console.log("removeImagesByFilename - image.src: ", image.src, filename(image.src));
        if ((filename(image.src) === targetFilename) 
             && !image.classList.contains('figur')) {
            image.remove();
        }
    });
}

function removeMessage() {
    document.getElementById('Message').innerHTML = '';
    document.getElementById('Message').style.visibility = 'hidden';
}

fetchVersion().then(version => {
    document.getElementById('field-label').innerHTML = '20.12.2024, Michael Lanker, ' + version;
}).catch(error => {
    document.getElementById('field-label').innerHTML = '20.12.2024, Michael Lanker';
    console.error("Error fetching version:", error);
});

