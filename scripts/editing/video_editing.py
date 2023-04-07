from moviepy.editor import VideoFileClip, AudioFileClip, CompositeAudioClip
import cv2
import os
from ..utils.omp_tools import OsTools
import random

class VideoEdit:
    def __init__(self):
        self.background_color = (0, 0, 0)
        self.background_transparency = .45
        self.text_loading_color = (250, 250, 250)
        self.text_color = (255, 255, 255)
        self.font = cv2.FONT_HERSHEY_SIMPLEX
        self.linetype = cv2.LINE_AA
        self.font_scale = 2
        self.thickness = 3
        self.thickness_outer = int(self.thickness * 4)
        self.border = 20
        self.saved_bundles = []
    
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

    def __combine_strings(self, string):
        """combine strings into a list with bundles of max. 25 characters

        Args:
            string (str): string text
        """
        # if len(string) >= 250:
        #     return None
        
        combined_strings = []
        current_string = ''
        for string in string.split():
            if len(current_string + ' ' + string) <= 25:
                if current_string != '':
                    current_string += ' '
                current_string += string
            else:
                combined_strings.append(current_string)
                current_string = string
        combined_strings.append(current_string)
        return combined_strings

    def add_text_to_vertical_video(self, abs_video_path, text, author=None, output_path="output.mp4", font_scale=2, thickness=3):
        """add text with optional author to an vertical video

        Args:
            video_path (str): path of video to get edited
            text (str): text to write on video
            author (str, optional): author name. Defaults to None.
            output_path (str, optional): output path for mp4 file. Defaults to "output.mp4".
            font_scale (int, optional): text fontscale. Defaults to 2.
            thickness (int, optional): text thickness. Defaults to 3.
        """
        #text = OsTools.delete_unreadable_characters(text, [";", "”", "“"])
        if len(text) >= 250 or text is None:
            print(f"skipped '{text}' because its too long or is None")
            return None
        
        # cutting video with offset to be not useless long
        tts = output_path.split(".")[-2] + ".wav"
        bg_music_path = os.path.join("assets", "background_music")
        temp_output_path = os.path.join("temp", os.path.basename(output_path))
        background_music = random.choice(os.listdir(bg_music_path)) 
        print(background_music)
        print(tts)
        print(temp_output_path)
        audio = AudioFileClip(os.path.join("temp", os.path.basename(output_path).split(".")[-2] + ".wav"))
        audio_offset = 5
        # Get the duration of the audio clip
        duration = audio.duration
        print(f"cutting video with {duration}s audio+ {audio_offset}s offset to make video shorter..")
        
        self.cut_video(0, duration + audio_offset, abs_video_path, temp_output_path)
        #self.add_audio_clips_to_video(temp_output_path, tts, background_music)
        
        self.font_scale = font_scale
        self.thickness = thickness
        
        cap = cv2.VideoCapture(temp_output_path)
        width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        fps = int(cap.get(cv2.CAP_PROP_FPS))
        frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        
        fourcc = cv2.VideoWriter_fourcc(*"mp4v")
        out = cv2.VideoWriter(output_path, fourcc, fps, (width, height))
                        
        # set text bundles
        text = self.__combine_strings(text)
        
        if author is not None:
            text.append("")  # append empty element to separate author text
            text.append(f"- {author}")
        print(f"writing '{text}' into video..")
        
        for index, bundle in enumerate(text):
            text_size = cv2.getTextSize(bundle, self.font, self.font_scale, self.thickness_outer)[0]
            x = int((width - text_size[0]) / 2)
            y = int((height / 6 - text_size[1] / 2) + 10)
            y_offset = int(index * (text_size[1] + self.border * 2))  # need to be smaller
            y += y_offset
            alpha = 0

            for i in range(1, len(bundle) + 1):
                ret, frame = cap.read()
                if not ret:
                    break
                overlay = frame.copy()
                
                increment = (i / len(bundle)) / 1.5
                pt1 = (x - (text_size[0] * 2), y - text_size[1] - self.border)
                pt2 = (width, y + self.border)
                                
                rect = cv2.rectangle(overlay, pt1, pt2, self.background_color, cv2.FILLED)
                if self.saved_bundles:  # add background if bundle exists
                    for save_bundle in self.saved_bundles:
                        rect = cv2.rectangle(overlay, save_bundle.get("pt1"), save_bundle.get("pt2"), self.background_color, cv2.FILLED)
                cv2.addWeighted(rect, self.background_transparency, frame, 1 - self.background_transparency, 0, frame)
                
                cv2.putText(frame, bundle[:i], (x, y), self.font, font_scale, self.background_color, self.thickness_outer, self.linetype)  # outline
                cv2.putText(frame, bundle[:i], (x, y), self.font, font_scale, self.text_loading_color, self.thickness, self.linetype)  # text
                
                if self.saved_bundles:
                    for save_bundle in self.saved_bundles:
                        cv2.putText(frame, save_bundle.get("bundle"), (save_bundle.get("x"), save_bundle.get("y")), self.font, font_scale, self.background_color, self.thickness_outer, self.linetype)
                        cv2.putText(frame, save_bundle.get("bundle"), (save_bundle.get("x"), save_bundle.get("y")), self.font, font_scale, self.text_color, self.thickness, self.linetype)
                out.write(frame)
                alpha += increment
                
                if i == len(bundle):  # last element
                    d_bundle = {
                        "pt1": pt1,
                        "pt2": pt2,
                        "bundle": bundle,
                        "x": x,
                        "y": y,
                     }
                    self.saved_bundles.append(d_bundle)

        while True:  # after writing elements to video continue video with elements displayed
            ret, frame = cap.read()
            if not ret:
                break
            overlay = frame.copy()
            if self.saved_bundles:
                for save_bundle in self.saved_bundles:  # write firstly the background
                    rect = cv2.rectangle(overlay, save_bundle.get("pt1"), save_bundle.get("pt2"), self.background_color, cv2.FILLED)
                cv2.addWeighted(rect, self.background_transparency, frame, 1 - self.background_transparency, 0, frame)
                
                for save_bundle in self.saved_bundles:
                    cv2.putText(frame, save_bundle.get("bundle"), (save_bundle.get("x"), save_bundle.get("y")), self.font, font_scale, self.background_color, self.thickness_outer, self.linetype)
                    cv2.putText(frame, save_bundle.get("bundle"), (save_bundle.get("x"), save_bundle.get("y")), self.font, font_scale, self.text_color, self.thickness, self.linetype)
            out.write(frame)
             
        cap.release()
        out.release()
        print(f"Text '{text}' added to {temp_output_path}. Output saved to {output_path}.")

    def add_audio_clips_to_video(self, abs_video_path, tts_audio_path, background_music_path):
        # Load the video clip
        video = VideoFileClip(abs_video_path)

        # Load the two audio clips
        tts = AudioFileClip(tts_audio_path)
        background_music = AudioFileClip(background_music_path)

        # Combine the two audio clips
        combined_audio = CompositeAudioClip([tts, background_music])

        # Add the combined audio to the video clip
        video = video.set_audio(combined_audio)

        # Write the output video file
        video.write_videofile(abs_video_path)

if __name__ == '__main__':
    path = os.path.abspath(os.path.join("..", "..", "assets", "background_videos", "0-2.mp4"))
    #path2 = os.path.abspath(os.path.join("..", "assets", "default.mp4"))
    #VideoEdit().cut_video(0, 2, path2, path)
    VideoEdit().add_text_to_vertical_video(path, 'Be yourself; everyone else is already taken! asdasdasd asdasdasd asdasdasdasd asdasdasd', output_path="output.mp4")
