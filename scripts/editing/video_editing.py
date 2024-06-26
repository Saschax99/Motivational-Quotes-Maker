from moviepy.editor import VideoFileClip, AudioFileClip, CompositeAudioClip, concatenate_videoclips, CompositeVideoClip
import cv2
import os


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
        self.text_writing_speed = 2  # higher = slower

    @staticmethod
    def cut_video(start, end, file, output, intro=None, outro=None):
        """Set the start and end times of the subclip you want to cut

        Args:
            start (float): start time of the video
            end (float): end time of the video
            file (str): file name 
            output (str): output path
            intro (str, optional): path of intro. Defaults to None.
            outro (str, optional): path of outro. Defaults to None.
        """
        start_time = start  # seconds
        end_time = end  # seconds
        # Load the original video into a VideoFileClip object
        video = VideoFileClip(file)
        # Use the subclip method to cut the video
        subclip = video.subclip(start_time, end_time)

        if intro is not None:
            intro_video = VideoFileClip(intro)
            final_video = concatenate_videoclips([intro_video, subclip])
        if outro is not None:
            outro_video = VideoFileClip(outro)
            final_video = CompositeVideoClip([final_video, outro_video.set_start(final_video.duration)])
        if intro is not None or outro is not None:
            final_video.write_videofile(output, fps=60)

        else:
            # Write the subclip to a new video file with a frame rate of 60fps
            subclip.write_videofile(output, fps=60)

    @staticmethod
    def get_audio_length(audio_file_path):
        """cutting video with offset to be not useless long"""
        audio = AudioFileClip(audio_file_path)
        # Get the duration of the audio clip
        duration = audio.duration
        return duration

    @staticmethod
    def __combine_strings(string):
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

    def add_text_to_vertical_video(self, abs_video_path, text, author=None, output_path="output.mp4", font_scale=2,
                                   thickness=3):
        """add text with optional author to an vertical video

        Args:
            video_path (str): path of video to get edited
            text (str): text to write on video
            author (str, optional): author name. Defaults to None.
            output_path (str, optional): output path for mp4 file. Defaults to "output.mp4".
            font_scale (int, optional): text fontscale. Defaults to 2.
            thickness (int, optional): text thickness. Defaults to 3.
        """

        def draw_text_with_outline_on_frame(frame, text, x, y):
            cv2.putText(frame, text, (x, y), self.font, font_scale, self.background_color, self.thickness_outer,
                        self.linetype)  # outline
            cv2.putText(frame, text, (x, y), self.font, font_scale, self.text_loading_color, thickness,
                        self.linetype)  # text

        self.font_scale = font_scale
        self.thickness = thickness

        cap = cv2.VideoCapture(abs_video_path)
        width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        fps = int(cap.get(cv2.CAP_PROP_FPS))
        frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

        fourcc = cv2.VideoWriter_fourcc(*"mp4v")
        out = cv2.VideoWriter(output_path, fourcc, fps, (width, height))

        # set text bundles
        text = self.__combine_strings(text)

        if author is not None:
            # text.append("")  # append empty element to separate author text
            text.append(f"- {author}")
        print(f"writing '{text}' into video..")

        for index, bundle in enumerate(text):
            text_size = cv2.getTextSize(bundle, self.font, self.font_scale, self.thickness_outer)[0]
            x = int((width - text_size[0]) / 2)
            y = int((height / 6 - text_size[1] / 2) + 25)
            y_offset = int(index * (text_size[1] + self.border * 2))  # need to be smaller
            y += y_offset

            for i in range(0, (len(bundle) + 1) * self.text_writing_speed):  # for 1 bundle/row
                i = i / self.text_writing_speed

                ret, frame = cap.read()
                if not ret:
                    break
                overlay = frame.copy()

                pt1 = (0, y - text_size[1] - self.border)
                pt2 = (width, y + self.border)
                if self.saved_bundles:  # add background if bundle exists
                    for save_bundle in self.saved_bundles:
                        rect = cv2.rectangle(overlay, save_bundle.get("pt1"), save_bundle.get("pt2"),
                                             self.background_color, cv2.FILLED)
                rect = cv2.rectangle(overlay, pt1, pt2, self.background_color, cv2.FILLED)
                cv2.addWeighted(rect, self.background_transparency, frame, 1 - self.background_transparency, 0, frame)

                if self.saved_bundles:
                    for save_bundle in self.saved_bundles:
                        draw_text_with_outline_on_frame(frame, save_bundle.get("bundle"), save_bundle.get("x"),
                                                        save_bundle.get("y"))

                if not i.is_integer():  # slowing down the speed of the texts
                    i = int(i)
                    draw_text_with_outline_on_frame(frame, bundle[:i], x, y)
                    out.write(frame)
                    continue
                else:
                    i = int(i)
                    draw_text_with_outline_on_frame(frame, bundle[:i], x, y)

                out.write(frame)

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
                    rect = cv2.rectangle(overlay, save_bundle.get("pt1"), save_bundle.get("pt2"), self.background_color,
                                         cv2.FILLED)
                cv2.addWeighted(rect, self.background_transparency, frame, 1 - self.background_transparency, 0, frame)

                for save_bundle in self.saved_bundles:
                    draw_text_with_outline_on_frame(frame, save_bundle.get("bundle"), save_bundle.get("x"),
                                                    save_bundle.get("y"))
            out.write(frame)

        cap.release()
        out.release()
        print(f"Text '{text}' added to {abs_video_path}. Output saved to {output_path}.")

    @staticmethod
    def add_audio_clips_to_video(video_path, tts_audio_path, background_music_path, output_path):
        """add audio clips to a video

        Args:
            video_path (str): path
            tts_audio_path (str): path
            background_music_path (str): path
            output_path (str): path
        """
        with VideoFileClip(video_path) as video:
            video_duration = video.duration
            with AudioFileClip(background_music_path).set_duration(video_duration).audio_fadeout(
                    .33) as background_audio:
                reduced_background_audio = background_audio.volumex(0.1)
                with AudioFileClip(tts_audio_path).set_start(
                        1.2) as tts_audio:  # hardcoded wait 1 second to start audio should be changed in longterm
                    combined_audio = CompositeAudioClip([tts_audio, reduced_background_audio])
                    video_with_music = video.set_audio(combined_audio)
                    video_with_music.write_videofile(output_path, fps=60, codec="libx264")
