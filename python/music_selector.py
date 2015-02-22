#!/usr/bin/env python3
#-*-coding: utf-8-*-
"""
Toy application to select random music from my iTunes library with which to
fill a limited space on devices such as my iPod, phone or tablet.
"""
import sys
import os

from errors import CommandLineError
from playlist import ConstrainedPlaylist
from cli import handle_args
from output import write_m3u, write_stdout
from loaders.plist import load_file


def main():
    try:
        args = handle_args()
    except CommandLineError as e:
        print("Uh-oh!", e)
        sys.exit(1)

    # TODO: Implement flexible loading
    all_tracks = load_file("../music.xml")
    playlist = ConstrainedPlaylist(
        args.max_size, args.max_time, args.promote, args.demote,
        args.must_match)

    playlist.select(all_tracks)
    # TODO: implement choice of how to sort
    playlist.sort(key=lambda t: (t.artist or "", t.album or "", t.name))

    if args.output:
        _, ext = os.path.splitext(args.output)
        if ext != '.m3u':
            raise CommandLineError("Don't know how to write '{}'!".format(ext))
        with open(args.output, 'w') as out:
            write_m3u(playlist, out)
    else:
        # Just print it to stdout, don't know what else to do
        write_stdout(playlist)

    print("Total length: {} tracks".format(len(playlist)))
    print("Total size: {:.2f}MB".format(playlist.total_size / (1024 * 1024)))
    print("Total time: {}h{}m{}s".format(
        int(playlist.total_time / 3600),
        int((playlist.total_time % 3600) / 60),
        int(playlist.total_time % 60)))


if __name__ == '__main__':
    main()
