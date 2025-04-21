async function fetchCounter() {
    try {
        const response = await fetch("http://127.0.0.1:8000/counter/");
        const result = await response.json();
        document.getElementById("counter").innerHTML = `Counter: <strong>${result.counter}</strong>`;
    } catch (error) {
        console.error("Error:", error);
        document.getElementById("counter").innerHTML = `Error Message (fetchCounter): <strong>${error}</strong>`;
    }
}
// Fetch counter value every second
setInterval(fetchCounter, 1000);

