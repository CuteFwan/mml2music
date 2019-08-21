from pippi import dsp
from mml2music.mmlparser import MMLParser
from mml2music.writer import Writer

with open('input.mml', 'r') as file:
    mml = file.read().lower()

parser = MMLParser()

track = parser.get_notes(mml)

print(f'Parsed {len(track.notes)} notes.\nTotal length: {track.position}')


out = dsp.buffer(channels=1)

writer = Writer('flute', out)

writer.compose(track)

writer.export('renders/output44.wav')

print('Done!')