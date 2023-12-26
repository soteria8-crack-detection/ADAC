import os
import cv2

class VideoProcessor:
    """
    Utility class for processing videos and extracting frames.

    Parameters:
        - video_path (str): Path to the input video file.
        - output_folder (str): Output folder for storing extracted frames.

    Methods:
        - generate_filename(time_in_sec): Generate a filename based on the given time in seconds.
        - calculate_time_in_sec(cap): Calculate the time in seconds for the next frame.
        - extract_frames_from_video(): Extract frames from the input video and save them to the output folder.

    Example:
        video_processor = VideoProcessor(video_path='path/to/video.mp4', output_folder='path/to/output')
        video_processor.extract_frames_from_video()
    """
    
    def __init__(self, video_path, output_folder):
        """
        Initializes the VideoProcessor class.

        Parameters:
            - video_path (str): Path to the input video file.
            - output_folder (str): Output folder for storing extracted frames.
        """
        self.video_path = video_path
        self.output_folder = output_folder

    def generate_filename(self, time_in_sec):
        """
        Generate a filename based on the given time in seconds.

        Parameters:
            - time_in_sec (float): Time in seconds.

        Returns:
            - filename (str): Generated filename.
        """
        if time_in_sec == 0:
            return "frame_0.0s.jpg"
        else:
            return f'frame_{time_in_sec}s.jpg'

    def calculate_time_in_sec(self, cap):
        """
        Calculate the time in seconds for the next frame.

        Parameters:
            - cap: OpenCV VideoCapture object.

        Returns:
            - time_in_sec (float): Time in seconds for the next frame.
        """
        return 1 / cap.get(cv2.CAP_PROP_FPS)

    def extract_frames_from_video(self):
        """
        Extract frames from the input video and save them to the output folder.
        """
        cap = cv2.VideoCapture(self.video_path)
        if not cap.isOpened():
            raise ValueError("Error: Cannot open video.")
        
        time_in_sec = 0

        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break
            
            frame = cv2.resize(frame, (1280, 720))
            time_in_sec += self.calculate_time_in_sec(cap)
            filename = self.generate_filename(time_in_sec)
            filepath = os.path.join(self.output_folder, filename)
            cv2.imwrite(filepath, frame)

        cap.release()
        