from .errors import *

class Note:
    __slots__ = ('position', 'frequency', 'length', 'volume')

    def __init__(self, position: float, frequency: float, length: float, volume: float):
        self.position = position
        self.frequency = frequency
        self.length = length
        self.volume = volume

class Track:

    def __init__(self, *, max_length : int = None, max_notes : int = None):
        self.max_length = max_length if (max_length and max_length > 0) else None
        self.max_notes = max_notes if (max_notes and max_notes > 0) else None
        self.notes = list()
        self.position = 0
        print(self.max_length, self.max_notes)

    def check_length(self, new_length : int):
        """Returns True if new_length exceeds old length"""
        return (self.max_length and new_length > self.max_length) or new_length <= 0

    def add_note(self, note: Note):
        """Add a new note at the end of the track."""
        if self.check_length(self.position + note.length):
            raise ExceededLength("Adding note would exceed length limit.")
            pass
        elif self.max_notes and len(self.notes) >= self.max_notes:
            raise ExceededNotes("Adding note would exceed note limit.")
            pass
        else:
            self.notes.append(note)
            self.position += note.length



    def extend_last(self, length: float):
        """Extend the last note in the track."""
        if self.check_length(self.position + length):
            raise ExceededLength("Extending last note would exceed length limit.")
        else:
            self.notes[-1].length += length
            self.position += length

    def rest(self, length: float):
        """Add a rest of certain length to the current position of the track."""
        if self.check_length(self.position + length):
            raise ExceededLength("Adding rest would exceed length limit.")
            pass
        else:
            self.position += length

    def tempo(self, mult: float):
        """Modify the tempo of the track independant of the pitch."""
        if mult <= 0:
            # mult should not be negative or zero
            return
        elif self.check_length(self.position / mult):
            raise ExceededLength("Modifying tempo would exceed length limit.")
            pass
        else:
            for note in self.notes:
                note.position /= mult
                note.length /= mult
            self.position /= mult

    def pitch(self, mult: float):
        """Modify the pitch of the track independant of the tempo."""
        if mult <= 0:
            # mult should not be negative or zero
            return
        for note in self.notes:
            note.frequency *= mult

    def speed(self, mult: float):
        """Modify the tempo and pitch of the track at the same time."""
        if mult <= 0:
            # mult should not be negative or zero
            return
        elif self.check_length(self.position / mult):
            raise ExceededLength("Modifying speed would exceed length limit.")
            pass
        else:
            for note in self.notes:
                note.position /= mult
                note.length /= mult
                note.frequency *= mult
            self.position /= mult

    def constrain(self, *, low: float = 0, high: float = 44000):
        """Constrain the note frequencies of the track fo a certain range."""
        self.notes = [note for note in self.notes if low <= note.frequency <= high]

    def reverse(self):
        new_notes = []
        for note in self.notes[::-1]:
            note.position = self.position - note.position - note.length
            new_notes.append(note)
        del self.notes[:]
        self.notes = new_notes