from pippi import dsp
import mml2music
import os

with open('input.mml', 'r') as file:
    mml = file.read().lower()

parser = mml2music.MMLParser()

track = parser.get_notes(mml, max_length = -1, max_notes = 200)

print(f'Parsed {len(track.notes)} notes.\nTotal length: {track.position}')

track.reverse()

out = dsp.buffer(channels=1, samplerate=48000)

writer = mml2music.Writer(f'{os.path.dirname(os.path.abspath(__file__))}/sounds/flute', out)

writer.compose(track)

writer.export('renders/output48_reversed.wav')

print('Done!')