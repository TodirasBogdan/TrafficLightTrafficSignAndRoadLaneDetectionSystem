from ultralytics import YOLO


class TrafficDetector:
    def __init__(self):
        # Load the custom traffic light detection YOLOv8 model
        self.model_traffic_light = YOLO("../weights/traffic_lights/best.pt")
        # Load the custom traffic sign detection YOLOv8 model
        self.model_traffic_sign = YOLO("../weights/traffic_signs/best.pt")

    def detect_traffic_lights(self, frame, confidence):
        # Run YOLOv8 traffic light detection on the frame
        results_traffic_light = self.model_traffic_light(frame, imgsz=640, conf=confidence)
        # Place the traffic light detection results on the frame
        frame = results_traffic_light[0].plot()
        return frame

    def detect_traffic_signs(self, frame, confidence):
        # Run YOLOv8 traffic sign detection on the frame
        results_traffic_sign = self.model_traffic_sign(frame, imgsz=640, conf=confidence)
        # Place the traffic sign detection results on the frame
        frame = results_traffic_sign[0].plot()
        return frame
