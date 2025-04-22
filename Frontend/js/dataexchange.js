

function htmlGET(url, query) {
    var noQuery = (!query || query.trim() === '')
    return fetch(url + (noQuery ? '' : "?" + query), {
        method: 'GET',
         headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': '{{ csrf_token }}'
        },
    })
    .then(response => response.json())
    .catch(error => {
        console.error("Error at htmlGET():", error, url, query);
        return null
    }); 
}

function htmlPOST(url, data) {
    getCookie('csrftoken');
    return fetch(url, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCookie('csrftoken')
        },
        body: JSON.stringify(data)
    })
    .then(response => response.json())
    .catch(error => {
        console.error("Error at htmlPOST:", error, url, data);
        return null
    });
}



function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
//    console.log("CookieValue: ", cookieValue);
    return cookieValue;
}

// um aus dem Pfadnahmen (html://127.../images/rot.svg) den Dateinamen (rot) zu extrahieren
function filename(pfadname) {
    var filename = pfadname;
    filename = filename.substring(filename.lastIndexOf('/') + 1)
    filename = filename.split('.')[0];
    return filename;
}

function get_version() {
    const url = `http://localhost:8000/version/`;
    htmlGET(url, "")
    .then(result => {
        if (result !== null) {
            console.log("Version: ", result);
            console.log("Version: ", result.version);
//            version = ', Version: ' + result.version
            return ', Version: ' + result.version;
        } else {
            console.log("Version: result is null");
            return '';
        }
    });
}

var version = "";

async function fetchVersion() {
    try {
        // Make a GET request to the backend endpoint
        const response = await fetch('http://localhost:8000/version/');
        
        // Check if the response is OK
        if (!response.ok) {
            throw new Error(`HTTP error! Status: ${response.status}`);
        }

        // Parse the JSON response
        const data = await response.json();

        // Define a local variable with the version content
        version = data.version;

        console.log(`Version retrieved: ${version}`);
        return version; // Return the version if needed elsewhere
    } catch (error) {
        console.error('Error fetching version:', error);
        return null; // Return null if there's an error
    }
}

fetchVersion()


export  {htmlGET, htmlPOST, getCookie, filename, fetchVersion, version};

