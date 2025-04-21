

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

export  {htmlGET, htmlPOST, getCookie, filename};

