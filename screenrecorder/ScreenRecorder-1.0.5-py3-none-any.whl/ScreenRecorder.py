# -*- coding: UTF-8 -*-
from datetime import datetime
from msvcrt import getch
from multiprocessing import Manager, Process
from ntpath import exists, join
from os import listdir, mkdir, remove
from shutil import rmtree
from threading import Lock, Thread, current_thread
from time import sleep
from wave import open

from keyboard import wait
from moviepy.editor import AudioFileClip, ImageSequenceClip, afx
from pyaudio import PyAudio, paInt8, paInt16, paInt24, paInt32
from pyautogui import screenshot
from pygame.time import Clock

image_cache = []
pic_files = []
saving_image_thread_lock = Lock()
img_index = 0
init_saving_image_threads_num = 1
processes = []
threads = []
saving_image_threads = []
saving_image_threads_dict = {}


def _recording_device(flag):
    temp = PyAudio()
    if flag:
        # 逐一查找声音设备
        get_info = temp.get_device_info_by_index
        for device_index in range(temp.get_device_count()):
            device_info = get_info(device_index)
            if device_info['name'].find('立体声混音') != -1 and not device_info['hostApi']:
                return device_info
        else:
            print("找不到内录设备，使用默认麦克风。")
            return temp.get_default_input_device_info()
    else:
        return temp.get_default_input_device_info()


def _record_audio(start_event, audio_filename,
                  audio_chunk_size, audio_format, interrecord):
    audio_stream = PyAudio()
    device_info = _recording_device(interrecord)
    # 创建输入流
    stream = audio_stream.open(input_device_index=device_info['index'],
                               format=audio_format,
                               channels=device_info['maxInputChannels'],
                               rate=int(device_info['defaultSampleRate']),
                               input=True, frames_per_buffer=audio_chunk_size,
                               )
    read_stream = stream.read
    audio_file = open(audio_filename, 'wb')
    audio_file.setnchannels(device_info['maxInputChannels'])
    audio_file.setsampwidth(audio_stream.get_sample_size(audio_format))
    audio_file.setframerate(int(device_info['defaultSampleRate']))
    write_frames = audio_file.writeframes
    start_event_setted = start_event.is_set
    start_event.wait()
    while start_event_setted():
        try:
            # 从录音设备读取数据，直接写入音频文件
            audio_data = read_stream(audio_chunk_size)
            write_frames(audio_data)
        except:
            start_event.clear()

    audio_file.close()
    stream.stop_stream()
    stream.close()
    audio_stream.terminate()


def _get_screenshot(start_event, image_cache, max_fps):
    fps_lock = Clock()
    image_cache_append = image_cache.append
    tick = fps_lock.tick
    start_event_setted = start_event.is_set
    start_event.wait()
    while start_event_setted():
        try:
            image = screenshot()
            image_cache_append(image)
            tick(max_fps)
        except:
            start_event.clear()


def _save_image(start_event, image_cache, img_temp_dir):
    global img_index

    saving_image_current_thread = current_thread()
    saving_image_threads.append(saving_image_current_thread)
    saving_image_threads_dict[saving_image_current_thread] = True
    acquire_lock = saving_image_thread_lock.acquire
    release_lock = saving_image_thread_lock.release
    start_event_setted = start_event.is_set
    while start_event_setted() or image_cache:
        if image_cache:
            acquire_lock()
            image = image_cache[0]
            del image_cache[0]
            local_index = img_index
            img_index += 1
            release_lock()

            image.save(f'{img_temp_dir}\{local_index:08x}.jpg', quality=95)

        if saving_image_current_thread not in saving_image_threads_dict:
            break


def _scan(start_event, init_threads_num, image_cache, max_fps, img_temp_dir):
    threads_num = init_threads_num
    cache_length = 0
    screen_thread = Thread(target=_get_screenshot,
                           args=[start_event, image_cache, max_fps],
                           name='screen_thread')
    screen_thread.start()
    start_event_setted = start_event.is_set
    start_event.wait()
    while start_event_setted():
        sleep(1)
        if cache_length + max_fps >= len(image_cache) >= cache_length - max_fps:
            continue

        elif len(image_cache) > cache_length + max_fps:

            saving_image_thread = Thread(target=_save_image,
                                         args=[start_event,
                                               image_cache, img_temp_dir],
                                         name=f'saving_image_thread{threads_num}')
            saving_image_thread.start()
            cache_length = len(image_cache)
            threads_num += 1

        elif len(image_cache) < cache_length - max_fps:
            if threads_num > 1:
                threads_num -= 1
                saving_image_threads_dict.popitem()
                cache_length = len(image_cache)

    screen_thread.join()
    [thread.join() for thread in saving_image_threads]


def _cue(start_event):
    print_rate_lock = Clock()
    tick = print_rate_lock.tick
    num_of_dots = 0
    start_event_setted = start_event.is_set
    start_event.wait()
    while start_event_setted():
        if num_of_dots == 4:
            num_of_dots = 0
        print("\x1b[2J", end='')
        print('(按"q"键结束录制)Recording' + num_of_dots * '.', end='')
        num_of_dots += 1
        tick(1)

    print("\n录制结束。")


def start_screen_recording(record_audio: bool = True,
                           audio_chunk_size: int = 800,
                           audio_format: any = paInt16,
                           max_fps: float = 15,
                           delay: float = 3,
                           interrecord: bool = False,
                           crf: int = 23,
                           video_compression_speed: str = 'ultrafast',
                           codec: str = 'libx264') -> None:

    audio_filename = str(datetime.now())[:19].replace(':', '_') + '.mp3'
    img_temp_dir = f'.{audio_filename[:-4]}_temp'
    video_filename = audio_filename[:-3] + 'mp4'

    if exists(img_temp_dir):
        rmtree(img_temp_dir)
    mkdir(img_temp_dir)

    start_event = Manager().Event()

    # 分别录音和录屏
    audio_process = Process(target=_record_audio,
                            args=[start_event, audio_filename,
                                  audio_chunk_size, audio_format, interrecord],
                            name='audio_process')
    processes.append(audio_process)

    scan_process = Process(target=_scan,
                           args=[start_event, init_saving_image_threads_num,
                                 image_cache, max_fps, img_temp_dir],
                           name='scan_process')
    processes.append(scan_process)

    cue_process = Process(target=_cue, args=[start_event], name='cue_process ')
    processes.append(cue_process)

    strat_process = Process.start
    join_process = Process.join
    [strat_process(process) for process in processes]

    print(f'{delay}秒后开始录制，按"q"键结束录制。')

    sleep(delay)
    start_event.set()

    while True:
        sleep(.1)
        if getch() == b'q':
            [remove(join(img_temp_dir, fn))
             for fn in listdir(img_temp_dir) if not fn.endswith('.jpg')]
            if listdir(img_temp_dir):
                break
    # wait(hotkey='q')
    # sleep(12000)
    start_event.clear()

    [join_process(process) for process in processes if process != scan_process]

    # 把录制的音频和屏幕截图合成为视频文件
    audio = AudioFileClip(audio_filename)
    audio = audio.fx(afx.audio_normalize)

    scan_process.join()

    video_fps = len([fn for fn in listdir(img_temp_dir)]) / audio.duration

    image_clip = ImageSequenceClip(img_temp_dir, fps=video_fps)
    video = image_clip.set_audio(audio)

    video.write_videofile(video_filename, fps=None, codec=codec,
                          bitrate=None, audio=record_audio,
                          audio_fps=int(_recording_device(interrecord)[
                              'defaultSampleRate']),
                          preset=video_compression_speed, audio_codec=None,
                          audio_bufsize=2000, threads=None,
                          ffmpeg_params=['-crf', str(crf)])

    # 删除临时音频文件和截图
    remove(audio_filename)
    rmtree(img_temp_dir)


if __name__ == "__main__":
    start_screen_recording()
