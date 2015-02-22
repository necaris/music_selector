"""
Loader for track lists from an iTunes-format plist XML file.
"""
import datetime

import lxml.etree

from collection import Collection, Track


def plist_date_to_datetime(dt_string):
    '''
    Helper to parse a datetime in the iTunes library format (such as
    2012-01-12T00:54:32Z)
    '''
    return datetime.datetime.strptime(dt_string, "%Y-%m-%dT%H:%M:%SZ")


def plist_key_to_attribute(name):
    '''
    Helper function that transforms a key such as 'Track ID' into something
    appropriate for a Python attribute name, such as 'track_id'.
    '''
    return name.lower().replace(' ', '_')


# Certain attribute names need to be read as something other than
# strings, e.g. integers or datetimes -- provide a mapping from name to
# constructor function
_transformers = {
    'track_id': int,
    'size': int,
    'total_time': int,
    'date_modified': plist_date_to_datetime,
    'date_added': plist_date_to_datetime,
}

def plist_to_track(element):
    """
    Construct a `Track` instance from an appropriately formatted
    plist dictionary
    """
    track_info = {}
    for child_key in element[::2]:
        # Read through the child elements two at a time, since we know the
        # plist goes <key>k</key><value>v</value>, and set the attribute on
        # our track
        attr_name = plist_key_to_attribute(child_key.text)
        attr_val = child_key.getnext().text
        if attr_name in _transformers:
            attr_val = _transformers[attr_name](attr_val)
        track_info[attr_name] = attr_val
    return Track(**track_info)


def load_file(path="./music.xml"):
    '''
    Load a plist file and return the track list it contains as a Collection.
    '''

    tree = lxml.etree.parse(path)

    track_dictionary = None
    for element in tree.xpath("/plist/dict/key"):
        if element.text == "Tracks":
            track_dictionary = element.getnext()  # the value of the key
            break
    else:
        raise AssertionError("Could not find 'Tracks' dictionary!")

    tracks = Collection()
    for element in track_dictionary:
        if element.tag == "key":
            continue
        tracks.append(plist_to_track(element))

    return tracks
