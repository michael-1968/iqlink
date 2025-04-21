import { htmlGET, htmlPOST }  from "./dataexchange.js";
import figures from "./figures.js"; 
import { filename } from "./dataexchange.js";

function clockProgress() {
    showSetup();
}

function clockText() {
    showCalculationtext();
}

function showCalculationtext() {
    // var data;
    htmlGET("http://127.0.0.1:8000/calculation/text/", "")
        .then(result => {
            if (result !== null) {
                document.getElementById("Progress").innerHTML = 
                `Info: <strong>${result.calculationtext}</strong>Status: <strong>${result.status}</strong>`;
            } else {
                console.error("Error fetching calculation text");
            }
        });
}

function showSetup() {
    var data;
//    removeImages();
    htmlGET("http://127.0.0.1:8000/calculation/progress/", "")
        .then(result => {
            if (result !== null) {
                data = result;
//                console.log("Data: ", data);
                figures.showProgress(data, document);
            } else {
                console.error("Error fetching counter");
            }
        });
}


// TEST-Funktion
document.getElementById('Me').addEventListener('click', function() {
    var newValue = 10;  // Example value to send to the backend
    var inputElement = document.getElementById("Input-Top");
    newValue = parseFloat(inputElement.value);
    newValue = isNaN(newValue) ? 0 : newValue;
    htmlPOST('http://localhost:8000/counter/update/', { new_value: newValue })
        .then(result => {
            if (result == null) {
                console.error("Error forwarding Me-click");
            }
        })
});

// Um die Parameter hochzuladen
document.getElementById('Dont').addEventListener('click', function() {
    var parameterTop = document.getElementById("Input-Top");    
    var parameterBottom = document.getElementById("Input-Bottom");
    htmlPOST('http://localhost:8000/calculation/parameter/', { ParameterTop: parameterTop.value, ParameterBottom: parameterBottom.value })
        .then(result => {
            if (result == null) {
                console.error("Error forwarding Dont-click");
            }
        })
});

document.getElementById('Stop').addEventListener('click', function() {
    console.log("pause");
    htmlPOST('http://localhost:8000/calculation/', {cmd: 'pause'})
        .then(result => {
            if (result == null) {
                console.error("Error forwarding Done-click");
            }
        })
});

//document.getElementById('Me').style.visibility = 'hidden';
document.getElementById('Me').innerHTML = 'Test';
document.getElementById('Dont').innerHTML = 'Update Parameter';
document.getElementById('Label-Top').innerHTML = "Parameter Top";
document.getElementById('Label-Bottom').innerHTML = "Parameter Bottom";

// Fetch counter value every second
setInterval(clockProgress, 100);
setInterval(clockText, 100);


