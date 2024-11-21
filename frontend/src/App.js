import React from 'react';
import './App.css';

function App() {

  return (
    <div className="frame-box">
      <img
        className='frame'
        src="http://localhost:3001/camera"
        alt="카메라 스트리밍"
        // style={{ width: '100%', height: 'auto' }}
      />
    </div>
  );
}

export default App;