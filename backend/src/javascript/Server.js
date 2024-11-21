const express = require('express');
const { spawn } = require('child_process');
const app = express();
const port = 3001;

app.get('/camera', (req, res) => {
  res.writeHead(200, {
    'Content-Type': 'multipart/x-mixed-replace; boundary=frame',
    'Cache-Control': 'no-cache',
    'Connection': 'keep-alive',
    'Pragma': 'no-cache',
  });

  const pythonProcess = spawn('/Users/nogyumin/사용자/노규민/Practice/CAMERA-DETECTION/venv/bin/python3', ['/Users/nogyumin/사용자/노규민/Practice/CAMERA-DETECTION/backend/src/python/camera.py']);
  let buffer = Buffer.alloc(0);

  pythonProcess.stdout.on('data', (data) => {
    buffer = Buffer.concat([buffer, data]);

    while (buffer.length >= 4) {
      // 데이터 크기 읽기
      const frameSize = buffer.readUInt32LE(0);

      if (buffer.length >= frameSize + 4) {
        const frame = buffer.slice(4, frameSize + 4);
        buffer = buffer.slice(frameSize + 4);

        // 클라이언트에 전송
        res.write(`--frame\r\n`);
        res.write(`Content-Type: image/jpeg\r\n`);
        res.write(`Content-Length: ${frame.length}\r\n\r\n`);
        res.write(frame);
        res.write('\r\n');
      } else {
        break;
      }
    }
  });

  pythonProcess.stderr.on('data', (data) => {
    console.error(`stderr: ${data}`);
  });

  pythonProcess.on('close', (code) => {
    console.log(`Python 프로세스 종료: 코드 ${code}`);
    res.end();
  });

  req.on('close', () => {
    pythonProcess.kill();
  });
});

app.listen(port, () => {
  console.log(`서버가 http://localhost:${port} 에서 실행 중입니다.`);
});