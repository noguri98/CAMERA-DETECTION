
import cv2
import numpy as np

class ObjectDetector:
    def __init__(self, model_path, config_path, labels_path):
        # YOLO 모델 로드
        self.net = cv2.dnn.readNet(model_path, config_path)
        self.labels = open(labels_path).read().strip().split("\n")

    def detect(self, frame):
        # YOLO 입력 설정
        blob = cv2.dnn.blobFromImage(frame, 1/255.0, (416, 416), swapRB=True, crop=False)
        self.net.setInput(blob)
        
        # 네트워크 추론
        layer_names = self.net.getLayerNames()
        output_layers = [layer_names[i[0] - 1] for i in self.net.getUnconnectedOutLayers()]
        detections = self.net.forward(output_layers)

        results = []
        (H, W) = frame.shape[:2]

        for output in detections:
            for detection in output:
                scores = detection[5:]
                class_id = np.argmax(scores)
                confidence = scores[class_id]

                if confidence > 0.5:  # 신뢰도 임계값
                    box = detection[0:4] * np.array([W, H, W, H])
                    (centerX, centerY, width, height) = box.astype("int")
                    x = int(centerX - (width / 2))
                    y = int(centerY - (height / 2))
                    results.append({
                        "label": self.labels[class_id],
                        "confidence": float(confidence),
                        "box": (x, y, int(width), int(height))
                    })

        return results