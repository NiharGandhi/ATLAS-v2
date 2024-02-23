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
    signal_timings = {side: 0 for side in video_sources.keys()}

    for side, video_source in video_sources.items():
        detectors[side] = VehicleDetector(
            weights_file, config_file, class_names_file, video_source)
        trackers[side] = VehicleTracker()
        hubs[side] = TrafficHub()

    # Create windows for displaying video streams
    cv2.namedWindow('Adaptive Traffic Lights')

    while True:
        frames = []
        for side, detector in detectors.items():
            ret, frame = cv2.VideoCapture(video_sources[side]).read()
            if not ret:
                break

            # Detect vehicles on each side of the road...
            vehicle_data = detector.detect_vehicles()
            tracked_data = trackers[side].update(vehicle_data['vehicles'])
            hubs[side].receive_data(side, tracked_data)

            # Control signal timing based on traffic analysis...
            total_vehicles = len(tracked_data)
            if total_vehicles > 0:
                # Adjust signal timing based on the number of vehicles
                # Each vehicle takes 2 seconds, max 30 seconds
                signal_timings[side] = min(total_vehicles * 2, 30)

            # Display text indicating signal timing
            cv2.putText(frame, f"Signal Time: {signal_timings[side]} seconds", (
                10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

            # Resize frame to fit in a grid layout
            frame = cv2.resize(frame, (300, 300))
            frames.append(frame)

        # Combine frames into a single image using horizontal concatenation
        grid_image = cv2.hconcat(frames)

        # Display the combined grid image
        cv2.imshow('Adaptive Traffic Lights', grid_image)

        # Check for user input to exit
        if cv2.waitKey(1) == ord('q'):
            break

    # Release video capture objects and close all OpenCV windows
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()