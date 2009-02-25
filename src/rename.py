#!/usr/bin/python
# -*- coding: utf-8 -*-

import glob
import tag
import re
import shutil
import os

from tag import MyMp3
from tag import KNOWN_TAGS

TRACK = "%track"
TITLE = "%title"
ALBUM = "%album"
DISC = "%disc"
ARTIST = "%artist"
TAGDICT = {TRACK:tag.TRACK, TITLE:tag.TITLE, ALBUM:tag.ALBUM, ARTIST:tag.ARTIST, DISC:tag.DISC}

class TagDict:
    def __init__(self, dict):
        self.dict = dict
        
    def keys(self): return self.dict.keys() 
    def items(self): return self.dict.items()  
    def values(self): return self.dict.values()

        
    def __getitem__(self,key):
        return self.dict[key]
        
    def __setitem__(self, key, item):
        if key not in KNOWN_TAGS:
            raise KeyError
        else:
            self.dict[key] = item
            
    def __contains__(self, key):
        return self.dict.__contains__(key)
        
    def __iter__(self):
        return self.dict.__iter__()
        
    def setAlbum(self, album):
        self[TAGDICT[ALBUM]] = album
        
    def setTitle(self, title):
        self[TAGDICT[TITLE]] = title
    
    def setTrack(self, track):
        self[TAGDICT[TRACK]] = track
    
    def setDisc(self, disc):
        self[TAGDICT[DISC]] = disc
        
    def setArtist(self, artist):
        self[TAGDICT[ARTIST]] = artist

class TagDictBuilder:    
    ITEMS = [TRACK, TITLE, ALBUM, ARTIST]
    REGEX = re.compile("(" + TRACK + ")|(" + TITLE + ")|(" + ALBUM + ")|(" + ARTIST  + ")|(" + DISC + ")")
    
    def __init__(self, regex):
        self.regex = self._buildRegex(regex)
        
    def build(self, line):
        filtered = self.regex
        currentMatch = ""
        result = {}
        for match in filtered:
            if match in TagDictBuilder.ITEMS:
                currentMatch = match
            else:
                print line
                print "eat: " + match
                eaten = self._eat(line, match)
                line = eaten[1]
                if currentMatch != "":
                    print currentMatch
                    print eaten
                    result[TAGDICT[currentMatch]] = eaten[0].strip()
            filtered = filtered[1:]
        return TagDict(result)
                
            
    def _eat(self, line, token):
        token = re.escape(token)
        result = re.split("(" + token + ")",line,1)
        result = [k for k in result if k != ""]
        return [result[0], result[-1]]
        
    def _buildRegex(self, regex):
        splitted = TagDictBuilder.REGEX.split(regex)
        return [k for k in splitted if k != None]
        

class TagWriter:
    def __init__(self, file):
        self.file = file
        
    def writeTags(self, tagDict):
        for tag in tagDict:
            self.file.setTag(tag, tagDict[tag])
            
    def save(self):
        self.file.save()
        
class FileWriter:
    def __init__(self, path, schema, fileHandler):
        self.schema = schema
        self.path = path
        self.fh = fileHandler
    
    def move(self, file):
        self.move(file, False)
        
    def move(self, file, overwrite):
        src = self._getSource()
        dst = self._getDestination()
        self.fh.move(src,dst,overwrite)
    
    def copy(self, file, overwrite=False):
        src = self._getSource(file)
        dst = self._getDestination(file)
        self.fh.copy(src,dst, overwrite)
        
    def _getSource(self, file):
        return file.fname
        
    def _getDestination(self, file):
        return os.path.join(self.path,self._translateSchema(file)) + "." + file.extension
        
    def _translateSchema(self, file):
        location = self.schema
        for tag in TAGDICT:
            print tag
            print TAGDICT[tag]
            print file.getTag(TAGDICT[tag])
            location = location.replace(tag, file.getTag(TAGDICT[tag]))
        return location
            
class FileHandler:
    def copy(self, src, dst, overwrite):
        if overwrite == False and self._exists(dst):
            raise IOError(dst + ": exists")
        self.ensure_dir(dst)
        shutil.copy2(src,dst)
    
    def move(self, src, dst, overwrite):
        if overwrite == False and self._exists(dst):
            raise IOError(dst + ": exists")
        self.ensure_dir(dst)
        shutil.move(src,dst)
        
    def _exists(self, path):
        return os.path.exists(path)
        
    def ensure_dir(self,f):
        d = os.path.dirname(f)
        if not os.path.exists(d):
            os.makedirs(d)

        
class BatchRename:
    def __init__(self, tagDicts, musicFiles):
        self.tagDicts = tagDicts
        self.musicFiles = musicFiles
        
    def tagAll(self):
        for (file,tagDict) in zip(self.musicFiles,self.tagDicts):
            tw = TagWriter(file)
            tw.writeTags(tagDict)
            tw.save()