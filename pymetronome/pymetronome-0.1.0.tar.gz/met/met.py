import argparse
import sys
import winsound
from itertools import cycle
from types import SimpleNamespace
import time


class Meter(SimpleNamespace):
    def __init__(self, beats: int, unit: int):
        super().__init__(unit=unit, beats=beats)

    @classmethod
    def from_string(cls, s):
        return cls(*(int(i) for i in s.split('/')))

    def __iter__(self):
        return iter([self.unit, self.beats])

    def cycle(self):
        beats = [(880, 100)]
        if beats == 1:
            return cycle(beats)
        else:
            for _ in range(1, self.beats):
                beats.append((440, 100))
            return cycle(beats)

    def __str__(self):
        return '{}/{}'.format(self.beats, self.unit)


def bpm_to_interval(bpm: float) -> float:
    per_second = 60 / bpm
    return per_second


class Metronome:
    def __init__(self, bpm, meter: Meter):
        self.meter = meter
        self.running = False
        self.bpm = bpm

    def start(self):
        interval = bpm_to_interval(self.bpm)
        now = time.time()
        next_click = now + interval
        beats = self.meter.cycle()
        while True:
            now = time.time()
            if now >= next_click:
                next_click = now + interval
                next_sound = next(beats)
                winsound.Beep(*next_sound)


def main():
    parser = argparse.ArgumentParser('met')
    parser.add_argument('--bpm', default=120, type=int, help="Beats per minute (default is 120)")
    parser.add_argument('--meter', default='4/4', help='The time signature to use (default is "4/4")')
    args = parser.parse_args()
    meter = Meter.from_string(args.meter)
    met = Metronome(args.bpm, meter)
    try:
        met.start()
    except KeyboardInterrupt:
        sys.exit(0)
