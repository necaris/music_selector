"""
Classes related to individual tracks and the music collection(s) built up
out of them.
"""

class Track:
    '''
    Container for track information, such as name, artist, genre, size, and
    play time.
    '''

    def __init__(self, track_id=None, name=None, artist=None, album=None,
                 genre=None, size=0, total_time=0, location=None, **kw):
        self.track_id = track_id
        self.name = name
        self.artist = artist
        self.album = album
        self.genre = genre
        self.size = size
        self.total_time = total_time
        self.location = location
        # Just take any other properties
        for k, v in kw.items():
            setattr(self, k, v)

    @property
    def time_in_seconds(self):
        '''
        self.total_time is in milliseconds, return it conveniently in seconds
        '''
        return self.total_time / 1000

    def __repr__(self):
        return "{0}({1}, artist={2}, album={3}, genre={4})".format(
            self.__class__.__name__, self.name, self.artist, self.album,
            self.genre)


class Collection(list):
    @property
    def total_time(self):
        '''
        The sum total time of all tracks in the current collection, in seconds.
        '''
        # NOTE: each track holds its total time in milliseconds
        return sum([t.total_time / 1000 for t in self])

    @property
    def total_size(self):
        '''
        The sum total size of all tracks in the current collection, in bytes.
        '''
        return sum([t.size for t in self])
