from pippi import dsp, tune
import re
from mmlparser import MMLParser

with open('input.mml', 'r') as file:
    mml = file.read().lower()

parser = MMLParser()

track = parser.get_notes(mml)


print(f'Parsed {len(track.notes)} notes.\nTotal length: {track.position}')

out = dsp.buffer(channels=1)

samples = {
    tune.ntf('A1') : dsp.read('sounds/flute/55.wav'),
    tune.ntf('A2') : dsp.read('sounds/flute/110.wav'),
    tune.ntf('A3') : dsp.read('sounds/flute/220.wav'),
    tune.ntf('A4') : dsp.read('sounds/flute/440.wav'),
    tune.ntf('A5') : dsp.read('sounds/flute/880.wav'),
    tune.ntf('A6') : dsp.read('sounds/flute/1760.wav'),
    tune.ntf('A7') : dsp.read('sounds/flute/3520.wav'),
}


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