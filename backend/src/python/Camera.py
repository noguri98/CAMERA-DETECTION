import cv2
import sys
import struct

def main():
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("카메라를 열 수 없습니다.", file=sys.stderr)
        sys.exit(1)

    while True:
        ret, frame = cap.read()
        if not ret:
            print("프레임을 읽을 수 없습니다.", file=sys.stderr)
            break

        ret, buffer = cv2.imencode('.jpg', frame)
        if not ret:
            print("프레임 인코딩 실패", file=sys.stderr)
            break

        # 디버깅: 전송할 데이터 크기 출력
        # print(f"전송할 프레임 크기: {len(buffer)} 바이트", file=sys.stderr)

        sys.stdout.buffer.write(struct.pack('<L', len(buffer)))
        sys.stdout.buffer.flush()
        sys.stdout.buffer.write(buffer)
        sys.stdout.buffer.flush()

    cap.release()

if __name__ == "__main__":
    main()