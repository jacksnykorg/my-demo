import React, { useState } from 'react';
import './App.css';

function App() {
  const [title, setTitle] = useState('');
  const [description, setDescription] = useState('');
  const [error, setError] = useState('');
  
  // New state to hold the richer data from the API
  const [score, setScore] = useState(null);
  const [riskLevel, setRiskLevel] = useState('');
  const [factors, setFactors] = useState([]);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    setScore(null);
    setRiskLevel('');
    setFactors([]);

    try {
      const response = await fetch('http://localhost:3000/prioritize', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ title, description }),
      });

      if (!response.ok) {
        throw new Error('Failed to get a response from the API.');
      }

      const data = await response.json();
      // Set all the new state variables from the response
      setScore(data.risk_score);
      setRiskLevel(data.risk_level);
      setFactors(data.factors);

    } catch (err) {
      setError(err.message);
    }
  };

  return (
    <div className="container">
      <h1>Task Risk Prioritizer</h1>
      <p className="subtitle">Powered by NLP 🧠</p>
      <form onSubmit={handleSubmit}>
        <div className="form-group">
          <label htmlFor="title">Task Title</label>
          <input
            type="text"
            id="title"
            value={title}
            onChange={(e) => setTitle(e.target.value)}
            required
          />
        </div>
        <div className="form-group">
          <label htmlFor="description">Task Description</label>
          <textarea
            id="description"
            value={description}
            onChange={(e) => setDescription(e.target.value)}
            required
            rows={4}
          ></textarea>
        </div>
        <button type="submit">Calculate Risk</button>
      </form>

      {score !== null && (
        <div className="result-card">
          <div className="result-header">
            <h3>Risk Analysis Complete</h3>
            <div className={`risk-level ${riskLevel.toLowerCase()}`}>{riskLevel}</div>
          </div>
          <div className="score-display">
            Calculated Risk Score: <span>{score}</span>
          </div>
          <div className="factors">
            <h4>Contributing Factors:</h4>
            <ul>
              {factors.map((factor, index) => (
                <li key={index}>{factor}</li>
              ))}
            </ul>
          </div>
        </div>
      )}
      {error && <p className="error">{error}</p>}
    </div>
  );
}

export default App;