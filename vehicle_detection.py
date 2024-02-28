import cv2
import numpy as np
import csv
import datetime

class VehicleDetector:
    def __init__(self, weights_file, config_file, class_names_file, video_source):
        self.net = cv2.dnn.readNet(weights_file, config_file)
        self.classes = []
        with open(class_names_file, 'r') as file:
            self.classes = [line.strip() for line in file.readlines()]
        self.video_source = video_source
    
    def determine_side(self, centroid_x, frame_width):
        # Example logic to determine side based on centroid's x-coordinate
        if centroid_x < frame_width // 2:
            return "north"  # Example side names: north, south, east, west
        else:
            return "south"  # Assuming the center of the frame divides the road into two sides

    def detect_vehicles(self):
        print("video source: ", self.video_source)
        cap = cv2.VideoCapture(self.video_source)
        vehicle_data = {}

        while True:
            ret, frame = cap.read()
            if not ret:
                break

            height, width, _ = frame.shape
            blob = cv2.dnn.blobFromImage(
                frame, 1 / 255.0, (416, 416), swapRB=True, crop=False)
            self.net.setInput(blob)
            output_layers_names = self.net.getUnconnectedOutLayersNames()
            layer_outputs = self.net.forward(output_layers_names)

            boxes = []
            confidences = []
            class_ids = []
            detections = []  # Initialize detections list

            for output in layer_outputs:
                for detection in output:
                    scores = detection[5:]
                    class_id = np.argmax(scores)
                    confidence = scores[class_id]
                    if confidence > 0.5 and class_id == 2:  # Class ID 2 represents vehicles
                        center_x = int(detection[0] * width)
                        center_y = int(detection[1] * height)
                        w = int(detection[2] * width)
                        h = int(detection[3] * height)
                        x = int(center_x - w / 2)
                        y = int(center_y - h / 2)
                        boxes.append([x, y, w, h])
                        confidences.append(float(confidence))
                        class_ids.append(class_id)

                        # Assign side information based on camera position
                        # Assuming the camera covers one side of the road each
                        side = self.determine_side(center_x, width)
                        detections.append((class_id, (x, y, w, h), side))

            indexes = cv2.dnn.NMSBoxes(
                boxes, confidences, score_threshold=0.5, nms_threshold=0.4)

            vehicles = []
            for i in range(len(boxes)):
                if i in indexes:
                    x, y, w, h = boxes[i]
                    label = self.classes[class_ids[i]]
                    vehicles.append((label, (x, y, w, h), side))
                    cv2.rectangle(frame, (x, y), (x + w, y + h),
                                (0, 255, 0), 2)
                    cv2.putText(frame, label, (x, y - 5),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

            vehicle_data["current_frame"] = frame
            vehicle_data["vehicles"] = vehicles

            cv2.imshow("Vehicle Detection", frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        cap.release()
        cv2.destroyAllWindows()

        print(f"Detected {len(vehicles)} vehicles on {self.video_source}")

        return vehicle_data
