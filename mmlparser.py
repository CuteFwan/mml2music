from pippi import tune
import re


class MMLParser:
    def __init__(self, regex = None):
        self.pattern = regex or r"\/\*[\s\S]*?\*\/|\/\/.*\n|([tlvornabcdefg])([+\-#]?)(\d*)(\.?)|[<>]|&"

    def get_notes(self, mml):
        matches = re.finditer(self.pattern, mml)

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
                    if note == 'n':
                        # Handle midi notes
                        freq = tune.mtof(note+m[3])
                    else:
                        freq = tune.ntf(note, o)
                    notes.append([pos, freq, length*1.2, [V/8]*2])
                    pos += length
        return notes, pos
