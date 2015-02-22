"""
Loader for a track list from a Clementine SQLite database
"""
from datetime import datetime
import sqlite3

from collection import Collection, Track

def load_file(path):
    '''
    Connect to an SQLite3 database and retrieve a track list as a Collection.
    '''
    conn = sqlite3.connect("./music.db")
    conn.row_factory = sqlite3.Row

    cur = conn.cursor()
    cur.execute('''SELECT 0 AS "track_id", title AS name, artist, album, genre,
        filetype AS kind, filesize AS size, length AS total_time, track, year,
        mtime AS date_modified, ctime AS date_created, bitrate, samplerate,
        comment AS comments, NULL AS "persistent_id", filename AS location
        FROM songs''')

    rows = cur.fetchall()

    tracks = Collection()
    counter = 0
    for sqlite_row in rows:
        counter += 1
        row = dict(sqlite_row)
        row['track_id'] = counter
        row['total_time'] = int(row['total_time'] / 1000000)  # stored in ns
        row['date_modified'] = datetime.fromtimestamp(row['date_modified'])
        row['date_created'] = datetime.datetime.fromtimestamp(row['date_created'])
        tracks.append(Track(**row))

    return tracks
