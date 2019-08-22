from pippi import dsp
import mml2music

with open('input.mml', 'r') as file:
    mml = file.read().lower()

parser = mml2music.MMLParser()

track = parser.get_notes(mml)

print(f'Parsed {len(track.notes)} notes.\nTotal length: {track.position}')

track.tempo(0.75)
track.pitch(1.1)

out = dsp.buffer(channels=1)

writer = mml2music.Writer('flute', out)

writer.compose(track)

writer.export('renders/output22.wav')

print('Done!')