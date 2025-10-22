import React, { useState } from 'react';
import './App.css';

function App() {
  const [title, setTitle] = useState('');
  const [description, setDescription] = useState('');
  const [score, setScore] = useState(null);
  const [error, setError] = useState('');

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    setScore(null);

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
      setScore(data.risk_score);
    } catch (err) {
      setError(err.message);
    }
  };

  return (
    <div className="container">
      <h1>Task Risk Prioritizer</h1>
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
          ></textarea>
        </div>
        <button type="submit">Calculate Risk</button>
      </form>

      {score !== null && (
        <div className="result">
          <h2>Calculated Risk Score: <span>{score}</span></h2>
        </div>
      )}
      {error && <p className="error">{error}</p>}
    </div>
  );
}

export default App;