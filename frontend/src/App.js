import React, { useEffect, useState } from 'react';

function App() {

  const [message, setMessage] = useState('');

  useEffect(() => {
    fetch('http://localhost:3001/text')
      .then(response => response.text())
      .then(data => setMessage(data))
      .catch(error => console.error('Error:', error));
  }, []);

  return (
    <div>
      <h1> {message} </h1>
    </div>
  );
}

export default App;