from pippi import dsp, tune
import re

with open('input.mml', 'r') as file:
    mml = file.read()


pattern = r"\/\*[\s\S]*?\*\/|\/\/.*\n|([tlvornabcdefg])([+\-#]?)(\d*)(\.?)|[<>]|&"

matches = re.finditer(pattern, mml)

T = 120
L = 4
dotted = False
V = 8
O = 4
tie = False


notes = []
pos = 0

b = ''


for m in matches:
    #print(''.join(f"{f'm[{i}] = {b if not m[i] else m[i]}':15}" for i in range(5)))
    if m[0].startswith('/'):
        #comment, ignore
        continue

    if m[0] == '<':
        O -= 1
    elif m[0] == '>':
        O += 1
    elif m[0] == '&':
        tie = True
    elif m[1] == 't':
        T = int(m[3])
    elif m[1] == 'l':
        L = int(m[3])
        dotted = bool(m[4])
    elif m[1] == 'v':
        V = int(m[3])
    elif m[1] == 'o':
        O = int(m[3])

    elif m[1] in 'abcdefgr':
        length = 240 / ((int(m[3]) if m[3] else L) * T)
        if dotted or m[4]:
            length *= 1.5
        if tie:
            #tie
            notes[-1][2] += length
            tie = False
            pos += length
        elif m[1] == 'r':
            #do nothing, advence position
            pos += length
        else:
            #every other note
            note = m[1]
            if m[2] in ['+', '#']:
                note += '#'
            elif m[2] == '-':
                note += 'b'

            if note == 'cb':
                o = O-1
            elif note == 'b#':
                o = O+1
            else:
                o = O
            freq = tune.ntf(note, o)
            notes.append([pos, freq, length*1.2, [V/8]*2])
            pos += length

print(f'Parsed {len(notes)} notes')

out = dsp.buffer(channels=1)

samples = {
    tune.ntf('A1') : dsp.read('sounds/flute55.wav'),
    tune.ntf('A2') : dsp.read('sounds/flute110.wav'),
    tune.ntf('A3') : dsp.read('sounds/flute220.wav'),
    tune.ntf('A4') : dsp.read('sounds/flute440.wav'),
    tune.ntf('A5') : dsp.read('sounds/flute880.wav'),
    tune.ntf('A6') : dsp.read('sounds/flute1760.wav'),
    tune.ntf('A7') : dsp.read('sounds/flute3520.wav'),
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
total = len(notes)
splits = 0.1
split = 0

for pos, F, L, V in notes:
    if (i/total) >= split:
        split += splits
        print(f'{i/total*100:.2f}% {i} / {total}')

    nearest = get_nearest_freq(F, samples.keys())   # Find the best frequency to modulate from
    if nearest is None:
        continue
    note = samples[nearest].speed(F/nearest)  # Modulate nearest sample to desired frequency.

    if L < note.dur:
        note = note.cut(0, L)   # Chop to length
    note.adsr(0, 0, 1, 10)  # Apply adsr envelope
    note *= V               # Apply amp envelope
    out.dub(note,pos)       # Write note
    i += 1

out.write(f'renders/output.wav')
print('Done!')