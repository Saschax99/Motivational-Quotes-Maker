
#from moviepy.video.io.VideoFileClip import VideoFileClip
from moviepy.editor import VideoFileClip, TextClip, CompositeVideoClip
import cv2
import numpy as np

class VideoEdit:
    def __init__(self):
        pass
    
    def cut_video(self, start, end, file, output):
        """Set the start and end times of the subclip you want to cut"""
        start_time = start # seconds
        end_time = end # seconds
        # Load the original video into a VideoFileClip object
        video = VideoFileClip(file)
        # Use the subclip method to cut the video
        subclip = video.subclip(start_time, end_time)
        # Write the subclip to a new video file with a frame rate of 60fps
        subclip.write_videofile(output, fps=60)

    def add_text_to_video(self, text, video, output):
        # Load the video file
        cap = cv2.VideoCapture(video)

        # Define the text and font properties
        font = cv2.FONT_HERSHEY_SIMPLEX
        font_size = 15
        font_thickness = 2

        # Create a blank image with the same size as the video frames
        frame_width = int(cap.get(3))
        frame_height = int(cap.get(4))
        blank_image = np.zeros((frame_height, frame_width, 3), np.uint8)

        # Draw the text with a black outline on the blank image
        (text_width, text_height), _ = cv2.getTextSize(text, font, font_size, font_thickness)
        text_x = int((frame_width - text_width) / 2)
        text_y = int(frame_height / 4 - text_height / 2)

        # Draw the text with a black outline on the blank image
        outline_size = 7
        text_color = (255, 255, 255)  # white
        outline_color = (0, 0, 0)  # black
        cv2.putText(blank_image, text, (text_x-outline_size, text_y), font, font_size, outline_color, font_thickness+2, cv2.LINE_AA)
        cv2.putText(blank_image, text, (text_x+outline_size, text_y), font, font_size, outline_color, font_thickness+2, cv2.LINE_AA)
        cv2.putText(blank_image, text, (text_x, text_y-outline_size), font, font_size, outline_color, font_thickness+2, cv2.LINE_AA)
        cv2.putText(blank_image, text, (text_x, text_y+outline_size), font, font_size, outline_color, font_thickness+2, cv2.LINE_AA)

        # Draw the text with the desired color on top of the black outline
        cv2.putText(blank_image, text, (text_x, text_y), font, font_size, text_color, font_thickness, cv2.LINE_AA)

        # Loop over the video frames and add the text to each frame
        frames_with_text = []
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break
            frame_with_text = cv2.addWeighted(frame, 1, blank_image, 1, 0)
            frames_with_text.append(frame_with_text)

        # Save the result as a new video file
        out = cv2.VideoWriter(output, cv2.VideoWriter_fourcc(*'mp4v'), cap.get(cv2.CAP_PROP_FPS), (frame_width, frame_height))
        for frame_with_text in frames_with_text:
            out.write(frame_with_text)
        out.release()

        # Release the video capture object
        cap.release()

if __name__ == '__main__':
    VideoEdit().add_text_to_video("Be yourself; everyone else is already taken. -author", "background_videos/0-30.mp4", "output.mp4")
