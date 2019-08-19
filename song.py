class Note:
    __slots__ = ('position', 'frequency', 'length', 'volume')

    def __init__(self, position: float, frequency: float, length: float, volume: float):
        self.position = position
        self.frequency = frequency
        self.length = length
        self.volume = volume

class Track:

    def __init__(self):
        self.notes = list()
        self.position = 0

    def add_note(self, note: Note):
        self.notes.append(note)
        self.position += note.length

    def extend_last(self, length: float):
        self.notes[-1].length += length
        self.position += length

    def rest(self, length: float):
        self.position += length