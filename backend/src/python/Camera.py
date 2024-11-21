import cv2
import base64
import sys
import time

def stream_camera():
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("카메라를 열 수 없습니다.")
        sys.exit(1)

    try:
        while True:
            ret, frame = cap.read()
            if not ret:
                print("프레임을 읽을 수 없습니다.")
                break

            _, buffer = cv2.imencode('.jpg', frame)
            frame_base64 = base64.b64encode(buffer).decode('utf-8')

            # Base64 프레임 출력
            print(frame_base64)
            sys.stdout.flush()  # 출력 버퍼 비우기 (Node.js가 즉시 수신 가능)

            time.sleep(0.03)  # 30 FPS 속도로 조정
    finally:
        cap.release()

if __name__ == "__main__":
    stream_camera()