"""
Handle the command-line inputs to the music selector
"""
import argparse

from errors import CommandLineError


# Definition of byte multipliers for various units, e.g. KB = 1024 bytes
_SIZE_MULTIPLIERS = {
    'gb': 1024 * 1024 * 1024,
    'mb': 1024 * 1024,
    'kb': 1024
}


def _parse_size(size_string):
    '''
    Parse a size specification (e.g. 10MB or 5GB) into a number in bytes. A
    raw number is assumed to be just bytes.
    '''
    size_string = size_string.lower()
    # Assume the last two characters are the units, e.g. MB
    if size_string[-2:].isalpha():
        units = size_string[-2:]
        size_string = size_string[:-2]
        multiplier = _SIZE_MULTIPLIERS.get(units, 1)  # default to raw bytes

    try:
        size = float(size_string) * multiplier
        return size
    except ValueError:
        raise CommandLineError("Invalid size specification!")


# Definition of second multipliers for various units, e.g. m = 60s
_TIME_MULTIPLIERS = {
    'h': 3600,
    'm': 60,
    's': 1,
    'ms': 0.001
}


def _parse_time(time_string):
    '''
    Parse a time specification (e.g. 10m or 1.5h) into a number in seconds -
    a raw number is assumed to already be in seconds.
    '''
    multiplier = 1
    if time_string[-1].isalpha():
        units = time_string[-1]
        time_string = time_string[:-1]
        multiplier = _TIME_MULTIPLIERS.get(units, 1)  # default to seconds

    try:
        time = float(time_string) * multiplier
        return time
    except ValueError:
        raise CommandLineError("Invalid time specification!")


def handle_args():
    '''
    Deal with the command-line.
    '''
    description = '''
Randomly choose some music from the iTunes library, given certain criteria
for what should be chosen, e.g. certain genres should be promoted, others
avoided, and / or some genres must be matched, and matching certain constraints
e.g. maximum size or playing time.'''
    epilog = '''
Note that the maximum size and time constraints will be loosely met and may
"overflow" by at most one track (usually ~5 minutes / 5 MB), so they should not
be considered hard limits.'''

    parser = argparse.ArgumentParser(description=description.strip(),
                                     epilog=epilog.strip())
    parser.add_argument("-s", "--max-size", default=None)
    parser.add_argument("-t", "--max-time", default=None)
    parser.add_argument("-p", "--promote", action="append", required=False)
    parser.add_argument("-d", "--demote", action="append", required=False)
    parser.add_argument("-m", "--must-match", action="append", required=False)
    parser.add_argument("-o", "--output", required=False)
    parser.add_argument("-l", "--load-from", required=False)  # TODO
    args = parser.parse_args()

    if not args.max_size and not args.max_time:
        raise CommandLineError("Either maximum size or time must be given!")

    if args.max_size:
        args.max_size = _parse_size(args.max_size)
    if args.max_time:
        args.max_time = _parse_time(args.max_time)

    return args
