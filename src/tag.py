#!/bin/python
# -*- coding: utf-8 -*-

from mutagen.mp3 import MP3
from mutagen.easyid3 import EasyID3

from mutagen.flac import FLAC
from mutagen.id3 import ID3, TIT2, TPE1, TALB, TRCK, TPOS

import mutagen.id3

#FIXME add year, disc, comment,..
#FIXME add flac, oggvorbis, oggflac,...
#FIXME add TagFileBuilder

ARTIST = "Artist"
ALBUM = "Album"
TITLE = "Title"
TRACK = "Track"
YEAR = "Year"
DISC = "Disc"
KNOWN_TAGS = [ARTIST, ALBUM, TITLE, TRACK, YEAR, DISC]

class TagFile:
        
    def tags(self):
        return {ARTIST:[self.artist, self.setArtist], ALBUM:[self.album, self.setAlbum], TRACK:[self.track, self.setTrack], TITLE:[self.title, self.setTitle], DISC:[self.disc, self.setDisc]}
    
    def setTag(self, tag, value):
        self.tags()[tag][1](value)
        
    def getTag(self, tag):
        return self.tags()[tag][0]()
    
    def artist(self):
        self._read(ARTIST)
    
    def setArtist(self, artist):
        self._write(ARTIST, artist)
    
    def title(self):
        self._read(TITLE)
    
    def setTitle(self, title):
        self._write(TITLE, title)
    
    def album(self):
        self._read(ALBUM)
    
    def setAlbum(self, album):
        self._write(ALBUM, album)
    
    def track(self):
        self._read(TRACK)
    
    def setTrack(self, track):
        self._write(TRACK, track)
    
    def disc(self):
        self._read(DISC)
    
    def setDisc(self, disc):
        self._write(DISC, disc)
    
    def save(self):
        self.file.save()

        
class MyMp3(TagFile):    
    writeDict = {ARTIST:TPE1, ALBUM:TALB, TRACK:TRCK, TITLE:TIT2, DISC:TPOS}
    readDict = {ARTIST:"TPE1", ALBUM:"TALB", TRACK:"TRCK", TITLE:"TIT2", DISC:"TPOS"}
    
    def __init__(self, fname):
        self.extension = "mp3"
        self.fname = fname
        self.file = ID3(fname)
        
    def _read(self, tag):
        try:
            return self.file.get(MyMp3.readDict[tag]).text[0]
        except AttributeError:
            return ""
            
    def _write(self, tag, value):
        self.file.add(MyMp3.writeDict[tag](encoding=0, text=unicode(value)))
        
        
class MyFlac(TagFile):
    def __init__(self, fname):
        self.extension = "flac"
        self.fname = fname
        self.file = FLAC(fname)