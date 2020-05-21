from typing import List
from os import path

from kcu import sh, kpath

from . import ffprobe

def reencode_mp3(path_in: str, path_out: str) -> bool:
    sh.sh(
        'ffmpeg -y -i ' + path_in + ' -codec:a libmp3lame -qscale:a 2 ' + path_out
    )

    return path.exists(path_out)

def create_video_from_images(
    input_folder: str,
    output_file_path: str,
    seconds_per_image: float = 3.0,
    file_base_name: str = 'image',
    file_extension: str = '.jpg'
) -> bool:
    sh.sh(
        'ffmpeg -y -framerate ' + str(1.0/seconds_per_image) + ' -start_number 001 -i ' + path.join(input_folder, file_base_name + '%03d' + file_extension) + ' -pix_fmt yuv420p ' + output_file_path
    )

    return path.exists(output_file_path)

def remove_audio(input: str, output: str) -> bool:
    sh.sh(
        'ffmpeg -y -i ' + sh.path(input) + ' -c copy -an ' + sh.path(output)
    )

    return path.exists(output)

def add_silence_to_video(input: str, output: str) -> bool:
    sh.sh(
        'ffmpeg -f lavfi -y -i anullsrc=channel_layout=stereo:sample_rate=48000 -i ' + sh.path(input) + ' -c:v copy -c:a aac -shortest ' + sh.path(output)
    )

    return path.exists(output)

def add_audio_to_video(input_a: str, input_v: str, output: str, reencode: bool = False) -> bool:
    cmd = 'ffmpeg -y -i ' + sh.path(input_v)+ ' -i ' + sh.path(input_a)

    if not reencode:
        cmd += ' -c:v copy -map 0:v:0 -map 1:a:0'
    
    cmd += ' -shortest ' + sh.path(output)

    sh.sh(cmd)

    return path.exists(output)

def loop_audio_to_video(in_a: str, in_v: str, out: str, reencode: bool = False) -> bool:
    return __loop_together(in_v, in_a, out, reencode=reencode)

def loop_video_to_audio(in_a: str, in_v: str, out: str, reencode: bool = False) -> bool:
    return __loop_together(in_a, in_v, out, reencode=reencode)

def loop(in_path: str, out_path: str, length_seconds: float):
    sh.sh('ffmpeg -y -stream_loop -1 -i ' + sh.path(in_path) + ' -t ' + str(length_seconds) + ' ' + sh.path(out_path))

    return path.exists(out_path)

def convert_video_to_16_9(in_path: str, out_path: str) -> bool:
    w, h = ffprobe.video_resolution(in_path)

    if h is None or w is None:
        return False
    
    if h == 1080 and w == 1920:
        sh.cp(in_path, out_path)

        return True
    
    if w/h < 16/9:
        sh.sh(
            'ffmpeg -y -i ' + sh.path(in_path) + " -vf 'split[original][copy];[copy]scale=1920:-1,setsar=1:1,crop=h=1080,gblur=sigma=75[blurred];[original]scale=-1:1080[original_resized];[blurred][original_resized]overlay=(main_w-overlay_w)/2:(main_h-overlay_h)/2' " + sh.path(out_path)
        )
    else:
        sh.sh(
            'ffmpeg -y -i ' + sh.path(in_path) + " -vf 'split[original][copy];[copy]scale=-1:1080,setsar=1:1,crop=w=1920,gblur=sigma=75[blurred];[original]scale=1920:-1[original_resized];[blurred][original_resized]overlay=(main_w-overlay_w)/2:(main_h-overlay_h)/2' " + sh.path(out_path)
        )

    return path.exists(out_path)

def concat_videos(in_paths: List[str], out_path: str) -> bool:
    if len(in_paths) == 0:
        return False
    elif len(in_paths) == 1:
        sh.cp(in_paths[0], out_path)

        return True

    temp_txt_path = path.join(kpath.folder_path_of_file(out_path), '.__temp_list.txt')
    temp_txt_content = ''

    for in_path in in_paths:
        if len(temp_txt_content) > 0:
            temp_txt_content += '\n'
        
        temp_txt_content += 'file \'' + in_path + '\''
    
    with open(temp_txt_path, 'w') as f:
        f.write(temp_txt_content)
    
    sh.sh('ffmpeg -y -f concat -safe 0 -i ' + sh.path(temp_txt_path) + ' -c copy ' + sh.path(out_path))
    kpath.remove(temp_txt_path)
    
    return path.exists(out_path)

# Private

# both in_reference_path and in_follower_path can be audio or video
# 1 needs to be video, the otheer needs to be audio
def __loop_together(in_reference_path: str, in_follower_path: str, out: str, reencode: bool = False) -> bool:
    reference_dur = ffprobe.get_duration(in_reference_path)
    follower_dur = ffprobe.get_duration(in_follower_path)

    looped_follower_path = kpath.temp_path_for_path(in_follower_path)

    if reference_dur > follower_dur:
        if not loop(in_follower_path, looped_follower_path, reference_dur):
            return False
    else:
        looped_follower_path = None

    in_video_path = in_reference_path
    in_audio_path = looped_follower_path or in_follower_path

    if ffprobe.has_video(in_audio_path):
        in_video_path = in_audio_path
        in_audio_path = in_reference_path

    return add_audio_to_video(in_audio_path, in_video_path, out, reencode=reencode)