'''
Possible ways of outputting the selected track list.
'''

def write_m3u(tracks, output_file):
    '''
    Outputs the given track list to a file in 'Extended M3U' format.
    '''
    m3u_line = "#EXTINF:{length}, {artist} - {title}\n{path}\n\n"
    o.write("#EXTM3U\n\n")
    for t in tracks:
        data = {
            'length': t.time_in_seconds,
            'artist': t.artist, 'title': t.name,
            'path': t.unix_path
        }
        o.write(m3u_line.format(**data))


def write_stdout(tracks):
    '''
    Pretty-prints the whole list to stdout.
    '''
    for t in tracks:
        print(t)
