import os
from pippi import dsp

from .song import Note, Track

class Writer:

    def __init__(self, instrument: str, buffer):
        self.instrument = instrument
        self.instrument_path = f'{os.path.dirname(os.path.abspath(__file__))}/sounds/{instrument}'
        self.samples = dict()
        self.buffer = buffer

        for file in os.listdir(self.instrument_path):
            freq = os.path.splitext(file)[0]
            try:
                self.samples[float(freq)] = dsp.read(f'{self.instrument_path}/{file}')
                print(self.samples[float(freq)].samplerate)
            except ValueError:
                # Not a valid number
                continue



    def get_nearest_freq(self, target, freqs):
        '''Finds the nearest frequency to modulate'''
        dist = None
        nearest = None
        for f in freqs:
            d = abs(f - target)
            if d == 0:
                return f
            elif dist is None or d < dist:
                dist = d
                nearest = f
        return nearest

    def get_next_freq(self, target, freqs):
        '''Finds the next highest frequency to modulate lower'''
        dist = None
        nearest = None
        for f in freqs:
            if f < target:
                continue
            d = f - target
            if d == 0:
                return f
            elif dist is None or d < dist:
                dist = d
                nearest = f
        return nearest

    def compose(self, track: Track):
        i = 0
        total = len(track.notes)
        splits = 0.1
        split = 0

        for note in track.notes:
            if (i/total) >= split:
                split += splits
                print(f'{i/total*100:.2f}% {i} / {total}')

            nearest = self.get_nearest_freq(note.frequency, self.samples.keys())   # Find the best frequency to modulate from
            if nearest is None:
                continue
            clip = self.samples[nearest].speed(note.frequency/nearest)  # Modulate nearest sample to desired frequency.

            if note.length < clip.dur:
                clip = clip.cut(0, note.length*1.2)     # Chop to length
            clip.adsr(0, 0, 1, 10)                      # Apply adsr envelope
            clip *= note.volume                         # Apply amp envelope
            self.buffer.dub(clip, note.position)        # Write note to buffer
            i += 1

    def export(self, path):
        self.buffer.write(path)