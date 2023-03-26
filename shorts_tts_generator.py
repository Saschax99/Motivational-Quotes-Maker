from moviepy.editor import VideoFileClip, TextClip, CompositeVideoClip
from moviepy.video.tools.drawing import outline
font_size = 50
font_color = 'green'
outline_color = 'black'
outline_thickness = 2

text = TextClip("Your Text Here", fontsize=font_size, color=font_color, font='Arial', stroke_color=outline_color, stroke_width=outline_thickness)
text = outline(text, color=font_color, thickness=outline_thickness)

clip = VideoFileClip('path_to_video_file')
final_clip = CompositeVideoClip([clip, text.set_pos(('center', 'bottom'))])
final_clip.write_videofile('output_video.mp4')