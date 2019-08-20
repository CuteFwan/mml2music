from pippi import dsp, tune
import re
import os
from mmlparser import MMLParser

with open('input.mml', 'r') as file:
    mml = file.read().lower()

parser = MMLParser()

track = parser.get_notes(mml)


print(f'Parsed {len(track.notes)} notes.\nTotal length: {track.position}')

out = dsp.buffer(channels=1)


instrument = 'flute'

samples = dict()

instrument_path = f'sounds/{instrument}'

for file in os.listdir(instrument_path):
    freq = os.path.splitext(file)[0]
    try:
        samples[float(freq)] = dsp.read(f'{instrument_path}/{file}')
    except ValueError:
        # Not a valid number
        continue



def get_nearest_freq(target, freqs):
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

def get_next_freq(target, freqs):
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


i = 0
total = len(track.notes)
splits = 0.1
split = 0

for note in track.notes:
    if (i/total) >= split:
        split += splits
        print(f'{i/total*100:.2f}% {i} / {total}')

    nearest = get_nearest_freq(note.frequency, samples.keys())   # Find the best frequency to modulate from
    if nearest is None:
        continue
    clip = samples[nearest].speed(note.frequency/nearest)  # Modulate nearest sample to desired frequency.

    if note.length < clip.dur:
        clip = clip.cut(0, note.length*1.2)   # Chop to length
    clip.adsr(0, 0, 1, 10)  # Apply adsr envelope
    clip *= note.volume               # Apply amp envelope
    out.dub(clip, note.position)       # Write note
    i += 1

out.write(f'renders/output56.wav')
print('Done!')