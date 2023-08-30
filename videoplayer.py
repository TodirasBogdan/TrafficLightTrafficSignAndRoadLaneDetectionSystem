import os
from tkinter.filedialog import askopenfile
import cv2
from roadlanelinedetector import process_frame
from trafficdetector import TrafficDetector


def rescale_frame(frame, percent):
    width = int(frame.shape[1] * percent / 100)
    height = int(frame.shape[0] * percent / 100)
    dim = (width, height)
    return cv2.resize(frame, dim, interpolation=cv2.INTER_AREA)


class VideoPlayer:

    def __init__(self):
        self.file_path = None
        self.traffic_detector = TrafficDetector()

    def open_file(self):
        file = askopenfile(mode="r",
                           filetypes=[("Video Files", ["*.mp4"]), ("Image Files", ["*.jpg", "*.jpeg", "*.png"])])
        self.file_path = file.name
        return self.file_path

    def play_video(self, traffic_light, traffic_sign, road_lane, rescale_percent, confidence):
        # Check file extension
        extension = os.path.splitext(self.file_path)[-1].lower()

        # Check if the file is an image
        if extension in [".jpg", ".jpeg", ".png"]:
            image = cv2.imread(self.file_path)

            # Detect traffic lights
            if traffic_light == "on":
                image = self.traffic_detector.detect_traffic_lights(image, confidence)

            # Detect traffic signs
            if traffic_sign == "on":
                image = self.traffic_detector.detect_traffic_signs(image, confidence)

            # Detect road lane lines
            if road_lane == "on":
                image = process_frame(image)

            image = rescale_frame(frame=image, percent=rescale_percent)
            cv2.imshow(winname="Press q to exit", mat=image)
            # Exit if any key is pressed
            cv2.waitKey(0)
            # Close the display window
            cv2.destroyAllWindows()

        # Check if the file is a video
        elif extension == ".mp4":
            capture = cv2.VideoCapture(self.file_path)

            while capture.isOpened():
                # Read a frame from the video
                success, frame = capture.read()

                if success:

                    # Detect Traffic Lights
                    if traffic_light == "on":
                        frame = self.traffic_detector.detect_traffic_lights(frame, confidence)

                    # Detect Traffic Signs
                    if traffic_sign == "on":
                        frame = self.traffic_detector.detect_traffic_signs(frame, confidence)

                    if road_lane == "on":
                        # Detect road lane lines
                        frame = process_frame(frame)

                    # Display the annotated frame
                    frame = rescale_frame(frame=frame, percent=rescale_percent)
                    cv2.imshow(winname="Press q to exit", mat=frame)

                    # Break the loop if 'q' is pressed
                    if cv2.waitKey(1) & 0xFF == ord("q"):
                        break
                else:
                    # Break the loop if the end of the video is reached
                    break

            # Release the video capture object and close the display window
            capture.release()
            cv2.destroyAllWindows()
