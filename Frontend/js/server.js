import express from 'express';
import path from 'path';
const app = express();

const port = 3000;
const __dirname = '';

// Statische Dateien aus dem aktuellen Verzeichnis ausliefern
app.use(express.static(path.join(__dirname)));

// Server starten
app.listen(port, () => {
    console.log(`Server läuft unter http://localhost:${port}`);
});
