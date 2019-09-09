from pippi import tune
import re
from .song import Note, Track


class MMLParser:
    def __init__(self, tempo : int = 120, length : int = 4, volume : int = 8, octave : int = 4, regex = None):
        self.tempo = tempo
        self.length = length
        self.volume = volume
        self.octave = octave

        self.pattern = regex or r"\/\*[\s\S]*?\*\/|\/\/.*\n|([tlvornabcdefg])([+\-#]?)(\d*)(\.?)|[<>]|&"

    def get_notes(self, mml):
        matches = re.finditer(self.pattern, mml)

        T = self.tempo or 120
        L = self.length or 4
        dotted = False
        V = self.volume or 8
        O = self.octave or 4
        tie = False

        notes = []
        pos = 0
        track = Track()


        for m in matches:
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

            elif m[1] in 'abcdefgrn':
                if m[1] == 'n':
                    length = 240 / (L * T)
                else:
                    length = 240 / ((int(m[3]) if m[3] else L) * T)
                if dotted or m[4]:
                    length *= 1.5
                if tie:
                    #tie
                    track.extend_last(length)
                    tie = False
                elif m[1] == 'r':
                    #do nothing, advence position
                    track.rest(length)
                else:
                    #every other note
                    note = m[1]
                    if m[2] in {'+', '#'}:
                        note += '#'
                    elif m[2] == '-':
                        note += 'b'

                    if note == 'cb':
                        o = O-1
                    elif note == 'b#':
                        o = O+1
                    else:
                        o = O
                    if note == 'n':
                        # Handle midi notes
                        freq = tune.mtof(note+m[3])
                    else:
                        freq = tune.ntf(note, o)
                    track.add_note(Note(track.position, freq, length, [V/8]*2))
        return track
