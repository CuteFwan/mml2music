from pippi import dsp
import mml2music

with open('input.mml', 'r') as file:
    mml = file.read().lower()

parser = mml2music.MMLParser()

track = parser.get_notes(mml, max_length = 40, max_notes = 172)

print(f'Parsed {len(track.notes)} notes.\nTotal length: {track.position}')

track.speed(1.1)

out = dsp.buffer(channels=1, samplerate=48000)

writer = mml2music.Writer('flute', out)

writer.compose(track)

writer.export('renders/output48.wav')

print('Done!')