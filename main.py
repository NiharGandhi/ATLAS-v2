import cv2
from vehicle_detection import VehicleDetector
from vehicle_tracking import VehicleTracker
from traffic_hub import TrafficHub


def main():
    # Initialize vehicle detector, tracker, and traffic hub...
    weights_file = "yolov4-tiny.weights"
    config_file = "yolov4-tiny.cfg"
    class_names_file = "coco.names"
    video_sources = {
        'north': "north_video.mp4",
        'south': "south_video.mp4",
        'east': "east_video.mp4",
        'west': "west_video.mp4"
    }

    detectors = {}
    trackers = {}
    hubs = {}

    for side, video_source in video_sources.items():
        detectors[side] = VehicleDetector(
            weights_file, config_file, class_names_file, video_source)
        trackers[side] = VehicleTracker()
        hubs[side] = TrafficHub()

    cap_dict = {side: cv2.VideoCapture(video_source)
                for side, video_source in video_sources.items()}

    while True:
        for side, cap in cap_dict.items():
            ret, frame = cap.read()
            if not ret:
                break
            cv2.imshow(side, frame)

            # Detect vehicles on each side of the road...
            vehicle_data = detectors[side].detect_vehicles()
            print(f"Detected vehicles on {side} side:", len(
                vehicle_data['vehicles']))

            # Track vehicles over time...
            tracked_data = trackers[side].update(vehicle_data['vehicles'])

            # Send tracked data to the traffic hub...
            hubs[side].receive_data(side, tracked_data)

        # Control signal timing based on traffic analysis...
        for side, hub in hubs.items():
            print(f"Controlling signals for {side} side...")
            hub.control_signals()

        if cv2.waitKey(1) == ord('q'):
            break

    for cap in cap_dict.values():
        cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
