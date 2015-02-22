import random

from collection import Collection


class ConstrainedPlaylist(Collection):
    '''
    Holds constraints (such as promoted, demoted, or must-match genres) as
    and can filter another Collection based on them.
    '''

    promote_factor = 0.3
    demote_factor = 0.3

    _default_threshold = 0.5

    def __init__(self, max_size=None, max_time=None, promote=None,
                 demote=None, must_match=None):

        self.max_size = max_size
        self.max_time = max_time
        # If tracks are promoted or demoted, they should be flagged as such,
        # but if no such criteria exist they shouldn't be flagged at all
        self.matchers = {
            'promoted': self.construct_matcher(promote, False),
            'demoted': self.construct_matcher(demote, False),
            # If there aren't any must-match criteria, the matcher should allow
            # tracks through, so default to True
            'must': self.construct_matcher(must_match, True)
        }

    def construct_matcher(self, elements, default=False):
        '''
        Returns a function that confirms whether a track matches the given
        criteria. If the criteria are empty, the function returns the default
        value.
        '''
        if not elements:
            # Nothing to match, so always return False
            return lambda self: default
        else:
            # Since what we currently expect is a list of genres, compile them
            # into a regular expression and return a function that, given a
            # track, returns True if the track has a matching genre.
            # NOTE that since the returned function is being attached to the
            # *instance*, it'll be looked up as a regular function and *not*
            # a bound method. So no need for the self argument.
            regex = re.compile("|".join(elements), re.IGNORECASE)
            return lambda t: t.genre and regex.match(t.genre)

    def _infinite_randomized_list(self, list_):
        '''
        Given a list, return an endless stream of random choices from it.
        '''
        while True:
            copy = list_[:]
            random.shuffle(copy)
            for element in copy:
                yield element

    def constraints_reached(self):
        '''
        Has the playlist reached its constraints?
        '''
        return ((self.max_size and self.total_size >= self.max_size) or
                (self.max_time and self.total_time >= self.max_time))

    def select(self, collection):
        infinite_list = self._infinite_randomized_list(collection)
        while not self.constraints_reached():
            track = next(infinite_list)
            if self.choose_track(track):
                self.append(track)

    def choose_track(self, track):
        '''
        Decide whether or not a track is selected by choosing a random number
        and checking it against the threshold. The default threshold is 0.5, so
        it's essentially a coin toss; however if the track is promoted or
        demoted the threshold changes, so certain types of track are more or
        less likely to make it through.
        '''
        if not self.matchers['must'](track):
            # Short-circuit if the must-match criteria aren't met
            return False

        threshold = self._default_threshold
        if self.matchers['promoted'](track):
            threshold -= self.promote_factor
        if self.matchers['demoted'](track):
            threshold += self.demote_factor

        choice = random.random()
        return (choice >= threshold)
