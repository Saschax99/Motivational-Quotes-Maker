
#from moviepy.video.io.VideoFileClip import VideoFileClip
from moviepy.editor import VideoFileClip, TextClip, CompositeVideoClip
import cv2
import numpy as np
import os
from typing import Tuple

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

    def __combine_strings(self, str_list):
        combined_strings = []
        current_string = ''
        for string in str_list:
            if len(current_string + ' ' + string) <= 27:
                if current_string != '':
                    current_string += ' '
                current_string += string
            else:
                combined_strings.append(current_string)
                current_string = string
        combined_strings.append(current_string)
        return combined_strings

    def add_text_to_video(self, text, video, output="output.mp4"):
        # Load video
        cap = cv2.VideoCapture(video)
        fps = cap.get(cv2.CAP_PROP_FPS)
        width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

        # Define codec and output video file
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        out = cv2.VideoWriter(output, fourcc, fps, (width, height))

        # Define text parameters
        font = cv2.FONT_HERSHEY_SIMPLEX
        font_scale = 2
        font_thickness = 3
        
        # set text bundles
        words = self.__combine_strings(text.split())
        words.append("author x")
        print(words)
        
        #for word in words:
            
        text_size, _ = cv2.getTextSize(words[0], font, font_scale, font_thickness)  # size of text x and y
        text_width = text_size[0]  # text x
        text_height = int(text_size[1] * 1.75)  # text y

        # Calculate position of text
        text_x = int((width - text_width) / 2)  # Centered horizontally
        text_y = int(height / 6)  # Top fourth of the screen vertically

        print("height:", height)
        print("height:", width)
        print("textheight:", text_height)
        print("textwidth:", text_width)
        
        # Add text to each frame
        for i in range(total_frames):
            ret, frame = cap.read()

            # Create white background for text
            frame_height = int(text_height * 1.5)
            #print("frameheight:", frame_height)
            frame_width = text_width + 10
            #white_background = np.ones(((frame_height), (frame_width), 3), np.uint8) * 255
            white_background = np.ones(((frame_height*len(words)), (frame_width), 3), np.uint8) #* 255
            # Add black text to white background for each word
            for j, word in enumerate(words):
                # Add black text to white background
                cv2.putText(white_background, word, (5, (j+1)*text_height), font, font_scale, (255, 255, 255), font_thickness, cv2.LINE_AA)


            # Add black text to white background
            #cv2.putText(white_background, words[0], (5, text_height), font, font_scale, (0, 0, 0), font_thickness, cv2.LINE_AA)

            # Overlay text on frame
            frame[text_y:text_y+frame_height*len(words), text_x:text_x+frame_width] = white_background
            #frame[text_y:text_y+frame_height, text_x:text_x+frame_width] = white_background
            
            # Write frame to output video
            out.write(frame)

        # Release video capture and writer objects
        cap.release()
        out.release()

        print(f"Text '{text}' added to {video}. Output saved to {output}.")
        
        
    def add_text_to_vertical_video(self, video_path, text, output_path, font_scale=2, thickness=3, fade_in=True):
        cap = cv2.VideoCapture(video_path)
        width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        fps = int(cap.get(cv2.CAP_PROP_FPS))
        frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        #frames = fps * duration
        
        fourcc = cv2.VideoWriter_fourcc(*"mp4v")
        out = cv2.VideoWriter(output_path, fourcc, fps, (width, height))
        
        font = cv2.FONT_HERSHEY_SIMPLEX
        border = 8
        
        text_size = cv2.getTextSize(text, font, font_scale, thickness)[0]
        x = int((width - text_size[0]) / 2)
        y = int(height / 6 - text_size[1] / 2)
        alpha = 0 if fade_in else 1
        increment = 1 / frames if fade_in else -1 / frames
        
        # set text bundles
        text = self.__combine_strings(text.split())
        text.append("author x")
        print(text)
        y = 0
        for bundle in text:
            text_size = cv2.getTextSize(bundle, font, font_scale, thickness)[0]
            x = int((width - text_size[0]) / 2)
            y = int(height / 6 - text_size[1] / 2)
            # y += text_size[1] this needs to be set in correlation to few rows ahead
            alpha = 0 if fade_in else 1
            increment = 1 / int(frames / len(bundle)) if fade_in else -1 / int(frames / len(bundle))

            # print(int(height / 6 - text_size[1] / 2))  # 298
            # print(int(height / 6 / 2))  # 160
            # print(text_size[1])  # 44
            print(y)
            for i in range(int(frames / len(text))):
                ret, frame = cap.read()
                if not ret:
                    break

                overlay = frame.copy()

                overlay = cv2.rectangle(overlay, (x - text_size[0], y - text_size[1] - border), (width, y + border), (0, 0, 0), cv2.FILLED)
                overlay = cv2.putText(overlay, bundle[:int(i/frames*len(bundle)*3)], (x, y), font, font_scale, (255, 255, 255), thickness)
                cv2.addWeighted(overlay, alpha, frame, 1 - alpha, 0, frame)
                out.write(frame)

                alpha += increment

        while True:
             ret, frame = cap.read()
             if not ret:
                 break
             
        cap.release()
        out.release()

        
if __name__ == '__main__':
    path = os.path.abspath(os.path.join("..", "assets", "background_videos", "0-30.mp4"))
    #path2 = os.path.abspath(os.path.join("..", "assets", "default.mp4"))
    #VideoEdit().cut_video(0, 2, path2, path)
    #VideoEdit().add_text_to_video("adasdas Be yourself; everyone else is already taken.", path, "output.mp4")
    VideoEdit().add_text_to_vertical_video(path, 'Be yourself; everyone else is already taken!', "output.mp4")
