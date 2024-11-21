
import cv2
import sys
import struct
from object import ObjectDetector

# 객체 탐지 초기화
detector = ObjectDetector(
    model_path="yolov3.weights",
    config_path="yolov3.cfg",
    labels_path="coco.names"
)

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

        # 객체 탐지 수행
        detections = detector.detect(frame)
        print(f"탐지 결과: {detections}", file=sys.stderr)

        # 프레임 전송
        ret, buffer = cv2.imencode('.jpg', frame)
        if not ret:
            print("프레임 인코딩 실패", file=sys.stderr)
            break

        sys.stdout.buffer.write(struct.pack('<L', len(buffer)))
        sys.stdout.buffer.flush()
        sys.stdout.buffer.write(buffer)
        sys.stdout.buffer.flush()

    cap.release()

if __name__ == "__main__":
    main()