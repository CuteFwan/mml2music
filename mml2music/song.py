class Note:
    __slots__ = ('position', 'frequency', 'length', 'volume')

    def __init__(self, position: float, frequency: float, length: float, volume: float):
        self.position = position
        self.frequency = frequency
        self.length = length
        self.volume = volume

class Track:

    def __init__(self, max_length : int = None, max_notes : int = None):
        self.max_length = max_length
        self.max_notes = max_notes
        self.notes = list()
        self.position = 0

    def add_note(self, note: Note):
        """Add a new note at the end of the track."""
        if self.max_length and self.position + note.length > self.max_length:
            # raise length error
            pass
        elif self.max_notes and self.max_notes > len(self.notes):
            # raise note count error
            pass
        else:
            self.notes.append(note)
            self.position += note.length



    def extend_last(self, length: float):
        """Extend the last note in the track."""
        if self.max_length and self.position + length > self.max_length:
            # raise length error
            pass
        else:
            self.notes[-1].length += length
            self.position += length

    def rest(self, length: float):
        """Add a rest of certain length to the current position of the track."""
        if self.max_length and self.position + length > self.max_length:
            # raise length error
            pass
        else:
            self.position += length

    def tempo(self, mult: float):
        """Modify the tempo of the track independant of the pitch."""
        for note in self.notes:
            note.position /= mult
            note.length /= mult
        self.position /= mult

    def pitch(self, mult: float):
        """Modify the pitch of the track independant of the tempo."""
        for note in self.notes:
            note.frequency *= mult

    def speed(self, mult: float):
        """Modify the tempo and pitch of the track at the same time."""
        for note in self.notes:
            note.position /= mult
            note.length /= mult
            note.frequency *= mult
        self.position /= mult

    def constrain(self, *, low: float = 0, high: float = 44000):
        """Constrain the note frequencies of the track fo a certain range."""
        self.notes = [note for note in self.notes if low <= note.frequency <= high]