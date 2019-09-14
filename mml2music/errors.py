class MmlError(Exception):
    """
    A generic MML2music error.
    """
    pass

class ExceededLength(MmlError):
    """
    Length has exceeded the limit
    """
    pass
class ExceededNotes(MmlError):
    """
    Number of notes has exceeded limit
    """
    pass