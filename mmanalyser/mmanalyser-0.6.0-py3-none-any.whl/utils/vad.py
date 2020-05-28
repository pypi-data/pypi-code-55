# -*- coding: utf-8 -*-
import collections
import contextlib
import sys
import wave
import webrtcvad
import os


def read_wave(path):
    """Reads a .wav file.

    Takes the path, and returns (PCM audio data, sample rate).
    """
    with contextlib.closing(wave.open(path, 'rb')) as wf:
        num_channels = wf.getnchannels()
        assert num_channels == 1
        sample_width = wf.getsampwidth()
        assert sample_width == 2
        sample_rate = wf.getframerate()
        assert sample_rate in (8000, 16000, 32000, 48000)
        pcm_data = wf.readframes(wf.getnframes())
        return pcm_data, sample_rate


def write_wave(path, audio, sample_rate, isSave=True):
    """Writes a .wav file.

    Takes path, PCM audio data, and sample rate.
    """
    if not isSave:
        return
    with contextlib.closing(wave.open(path, 'wb')) as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2)
        wf.setframerate(sample_rate)
        wf.writeframes(audio)


class Frame(object):
    """Represents a "frame" of audio data."""
    def __init__(self, bytes, timestamp, duration):
        self.bytes = bytes
        self.timestamp = timestamp
        self.duration = duration


def frame_generator(frame_duration_ms, audio, sample_rate):
    """Generates audio frames from PCM audio data.

    Takes the desired frame duration in milliseconds, the PCM data, and
    the sample rate.

    Yields Frames of the requested duration.
    """
    n = int(sample_rate * (frame_duration_ms / 1000.0) * 2)
    offset = 0
    timestamp = 0.0
    duration = (float(n) / sample_rate) / 2.0
    while offset+n < len(audio):
        yield Frame(audio[offset:offset + n], timestamp, duration)
        timestamp += duration
        offset += n


def vad_collector(sample_rate, frame_duration_ms, padding_duration_ms, vad,
                  frames):
    """Filters out non-voiced audio frames.

    Given a webrtcvad.Vad and a source of audio frames, yields only
    the voiced audio.

    Uses a padded, sliding window algorithm over the audio frames.
    When more than 90% of the frames in the window are voiced (as
    reported by the VAD), the collector triggers and begins yielding
    audio frames. Then the collector waits until 90% of the frames in
    the window are unvoiced to detrigger.

    The window is padded at the front and back to provide a small
    amount of silence or the beginnings/endings of speech around the
    voiced frames.

    Arguments:

    sample_rate - The audio sample rate, in Hz.
    frame_duration_ms - The frame duration in milliseconds.
    padding_duration_ms - The amount to pad the window, in milliseconds.
    vad - An instance of webrtcvad.Vad.
    frames - a source of audio frames (sequence or generator).

    Returns: A generator that yields PCM audio data.
    """
    num_padding_frames = int(padding_duration_ms / frame_duration_ms)
    # We use a deque for our sliding window/ring buffer.
    ring_buffer = collections.deque(maxlen=num_padding_frames)
    # We have two states: TRIGGERED and NOTTRIGGERED. We start in the
    # NOTTRIGGERED state.
    triggered = False

    voiced_frames = []
    for frame in frames:
        is_speech = vad.is_speech(frame.bytes, sample_rate)

        #         sys.stdout.write('1' if is_speech else '0')
        if not triggered:
            ring_buffer.append((frame, is_speech))
            num_voiced = len([f for f, speech in ring_buffer if speech])
            # If we're NOTTRIGGERED and more than 90% of the frames in
            # the ring buffer are voiced frames, then enter the
            # TRIGGERED state.
            if num_voiced > 0.9 * ring_buffer.maxlen:
                triggered = True
                triggered_time = ring_buffer[0][0].timestamp
                #                 sys.stdout.write('+(%s)' % (ring_buffer[0][0].timestamp,))
                # We want to yield all the audio we see from now until
                # we are NOTTRIGGERED, but we have to start with the
                # audio that's already in the ring buffer.
                for f, s in ring_buffer:
                    voiced_frames.append(f)
                ring_buffer.clear()
        else:
            # We're in the TRIGGERED state, so collect the audio data
            # and add it to the ring buffer.
            voiced_frames.append(frame)
            ring_buffer.append((frame, is_speech))
            num_unvoiced = len([f for f, speech in ring_buffer if not speech])
            # If more than 90% of the frames in the ring buffer are
            # unvoiced, then enter NOTTRIGGERED and yield whatever
            # audio we've collected.
            if num_unvoiced > 0.9 * ring_buffer.maxlen:
                #                 sys.stdout.write('-(%s)' % (frame.timestamp + frame.duration))
                triggered = False
                yield b''.join([f.bytes
                                for f in voiced_frames]), triggered_time
                triggered_time = 0
                ring_buffer.clear()
                voiced_frames = []


#    if triggered:
#         sys.stdout.write('-(%s)' % (frame.timestamp + frame.duration))
#     sys.stdout.write('\n')
# If we have any leftover voiced audio when we run out of input,
# yield it.
    if voiced_frames:
        yield b''.join([f.bytes for f in voiced_frames]), triggered_time


def vad(filename, mode=2, span=None, stride=None, chunk_dir=None):
    if chunk_dir:
        chunk_dir = os.path.join(chunk_dir, os.path.basename(filename)[:-4])
        if not os.path.exists(chunk_dir):
            os.makedirs(chunk_dir)
    chunk_path = os.path.join(chunk_dir if chunk_dir else '.',
                              'chunk-%01d.wav' % (mode, ))
    paths = [chunk_path]
    voiced_range = []
    voiced_duration = 0.0
    voiced_segment = b''
    audio, sample_rate = read_wave(filename)
    vad = webrtcvad.Vad(mode)
    # a frame is 30ms
    frames = list(frame_generator(30, audio, sample_rate))
    duration = len(frames) * 30 / 1000
    # a frame is 30ms & the queue is 200ms
    segments = vad_collector(sample_rate, 30, 200, vad, frames)
    for i, (segment, start_time) in enumerate(segments):
        path = os.path.join(chunk_dir if chunk_dir else '.',
                            'chunk-%002d-%01d.wav' % (i, mode))
        duration_ = len(segment) / sample_rate / 2
        paths.append(path)
        voiced_range.append([start_time, start_time + duration_])
        voiced_duration += duration_
        voiced_segment += segment
        if not span:
            write_wave(path, segment, sample_rate, bool(chunk_dir))

    if chunk_dir and len(paths) > 0:
        write_wave(chunk_path, voiced_segment, sample_rate, bool(chunk_dir))
        if span:
            if not stride:
                stride = span
            stride = max(stride, 1)
            span = max(span, 3)
            num = int((voiced_duration - span) / stride) + 1
            span = sample_rate * 2 * span
            stride = sample_rate * 2 * stride
            paths = [chunk_path]
            for i in range(num):
                path = os.path.join(chunk_dir, 'chunk-%002d-%01d.wav' % (
                    i,
                    mode,
                ))
                paths.append(path)
                write_wave(path, voiced_segment[i * stride:i * stride + span],
                           sample_rate)
    return paths if chunk_dir else [], voiced_range, voiced_duration, duration


def vad_robust(path, span=None, stride=None, chunk_dir=None):
    result = vad(path, span=span, stride=stride, mode=2, chunk_dir=chunk_dir)
    for x in [1, 0]:
        mid = vad(path, span=span, stride=stride, mode=x, chunk_dir=chunk_dir)
        if len(mid[1]) > len(result[1]):
            for tmp in result[0]:
                os.remove(tmp)
            result = mid
        else:
            if len(mid[1]) == len(result[1]):
                for tmp in result[0]:
                    os.remove(tmp)
                result = mid
            else:
                for tmp in mid[0]:
                    os.remove(tmp)
            break
    return result
