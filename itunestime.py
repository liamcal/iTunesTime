#!/usr/bin/env python
import xml.etree.ElementTree as etree
import sys
#March 10 2014: 363 days, 1 hour, 46 minutes and 10.3 seconds
#BASE_TIME = 31369570.3
#XML_FILE = "Library2015.xml"

def group(lst, n):
    """
    Group a list into consecutive n-tuples. Incomplete tuples are
    discarded e.g.

    >>> group(range(10), 3)
    [(0, 1, 2), (3, 4, 5), (6, 7, 8)]
    """
    return zip(*[lst[i::n] for i in range(n)])

def seconds_to_timestring(total_seconds):
    """
    Converts an integer value of seconds to a string representation
    giving days, hours, minutes, seconds
    >>> seconds_to_timestring(150)
    0 days, 0 hours, 2 minutes and 30.00 seconds
    >>> seconds_to_timestring(97530)
    1 days, 3 hours, 5 minutes and 30.00 seconds
    """
    minutes, seconds = divmod(total_seconds,60)
    hours, minutes = divmod(minutes, 60)
    days, hours = divmod(hours, 24)

    return "{} days, {} hours, {} minutes and {:.2f} seconds".format(int(days),int(hours),int(minutes),seconds)

def build_song_list(songs):
    """"
    Builds a list of song data from the children in an xml ElementTree.
    Each list item is a dictionary of data for a song
    """
    data = []
    for song in songs:
        info = {}
        for key,value in group(song.getchildren(),2):
            info[key.text] = value.text
        data.append(info)
    return data

def calculate_music_time(library_xml, base_time = 0):

    #parse the tree and get the root.
    tree = etree.parse(library_xml)
    root = tree.getroot()
    songs = root.findall('dict')[0].findall('dict')[0].findall('dict') #don't blame me, blame the XML

    #Tally the playtime for each valid sond record
    time = 0
    for song in build_song_list(songs):
        if all(tag in song for tag in ("Name", "Play Count", "Total Time")):
            time += int(song["Play Count"]) * int(song["Total Time"])
    return seconds_to_timestring(time/1000 - base_time)

if __name__ == "__main__":
    print(calculate_music_time(sys.argv[1]))
