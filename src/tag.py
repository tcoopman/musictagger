#!/bin/python
# -*- coding: utf-8 -*-

from mutagen.mp3 import MP3
from mutagen.easyid3 import EasyID3

import mutagen.id3


ARTIST = "Artist"
ALBUM = "Album"
TITLE = "Title"
TRACK = "Track"

class TagFile:
    def __init__(self):
        tags = {ARTIST:[self.artist, self.setArtist], ALBUM:[self.album, self.setAlbum], TRACK:[self.track, self.setTrack], TITLE:[self.title, self.setTitle]}
    
    def setTag(self, tag, value):
        TagFile.tags[tag][1](value)
        
    def getTag(self, tag):
        return TagFile.tags[tag][0]
    
    def artist(self):
        pass
    
    def setArtist(self, artist):
        pass
    
    def title(self):
        pass
    
    def setTitle(self, title):
        pass
    
    def album(self):
        pass
    
    def setAlbum(self, album):
        pass
    
    def track(self):
        pass
    
    def setTrack(self, track):
        pass
    
    def save(self):
        self.file.save()

class MyMp3(TagFile):
    _artist = "Artist"
    _album = "Album"
    _track = "tracknumber"
    _title = "Title"
    
    def __init__(self, fname):
        self.file = MP3(fname, ID3=EasyID3)
        try:
            self.file.add_tags(ID3=EasyID3)
        except mutagen.id3.error:
            pass
        
    def artist(self):
        try:
            return self.file[MyMp3._artist][0]
        except KeyError:
            return ""
        
    def setArtist(self, artist):
        self.file[MyMp3._artist] = artist
        
    def title(self):
        try:
            return self.file[MyMp3._title][0]
        except KeyError:
            return ""
        
    def setTitle(self, title):
        self.file[MyMp3._title] = title
    
    def album(self):
        try:
            return self.file[MyMp3._album][0]
        except KeyError:
            return ""
        
    def setAlbum(self, album):
        self.file[MyMp3._album] = album
    
    def track(self):
        try:
            return self.file[MyMp3._track][0]
        except KeyError:
            return 0
        
    def setTrack(self, track):
        self.file[MyMp3._track] = track