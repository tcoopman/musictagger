#!/usr/bin/python
# -*- coding: utf-8 -*-

import glob
import tag
import re
import shutil
import os

from tag import MyMp3

#musicFolder = "test/wereldkinderen"
#tagFile = "test/test_tags"

#lines = open(tagFile, "r").readlines()

#files = glob.glob(musicFolder + "/*.mp3")

#def writeFiles(lines):
    #for i in range(0, len(lines)):
        #file = readFile(i)
        #writeFile(file, makeDict(lines[i]))

#def readFile(number):
    #return MyMp3(files[number])
    
#def makeDict(line):
    #splitted = line.strip().split("-")
    #result = {}
    #result["Track"] = splitted[0]
    #result["Album"] = splitted[1]
    #result["Artist"] = splitted[2]
    #result["Title"] = splitted[3]
    #return result
    
#def writeFile(file, tags):
    #file.setTrack(tags["Track"])
    #file.setTitle(tags["Title"])
    #file.setAlbum(tags["Album"])
    #file.setArtist(tags["Artist"])
    #file.save()
    
#writeFiles(lines)

TRACK = "%track"
TITLE = "%title"
ALBUM = "%album"
ARTIST = "%artist"
TAGDICT = {TRACK:tag.TRACK, TITLE:tag.TITLE, ALBUM:tag.ALBUM, ARTIST:tag.ARTIST}

class TagDictBuilder:    
    ITEMS = [TRACK, TITLE, ALBUM, ARTIST]
    REGEX = re.compile("(" + TRACK + ")|(" + TITLE + ")|(" + ALBUM + ")|(" + ARTIST  + ")")
    
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
                    result[TAGDICT[currentMatch]] = eaten[0]
            filtered = filtered[1:]
        return result
                
            
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
    
    def copy(self, file):
        self.copy(file,False)
    
    def copy(self, file, overwrite):
        src = self._getSource(file)
        dst = self._getDestination(file)
        self.fh.copy(src,dst, overwrite)
        
    def _getSource(self, file):
        return file.fname
        
    def _getDestination(self, file):
        return os.path.join(self.path,self._translateSchema(file)) + "." + self.file.extension
        
    def _translateSchema(self, file):
        location = self.schema
        for tag in TAGDICT:
            location = location.replace(tag, file.getTag(TAGDICT[tag]))
        return location
            
class FileHandler:
    def copy(self, src, dst, overwrite):
        if overwrite == False and self._exists(dst):
            raise IOError(dst + ": exists")
        shutil.copy2(src,dst)
    
    def move(self, src, dst, overwrite):
        if overwrite == False and self._exists(dst):
            raise IOError(dst + ": exists")
        shutil.move(src,dst)
        
    def _exists(self, path):
        return os.path.exists(path)