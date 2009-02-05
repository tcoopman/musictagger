#!/usr/bin/python
# -*- coding: utf-8 -*-

import glob
import tag

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

class TagDictBuilder:
    import re
    
    TRACK = "%track"
    TITLE = "%title"
    ALBUM = "%album"
    ARTIST = "%artist"
    ITEMS = [TRACK, TITLE, ALBUM, ARTIST]
    REGEX = re.compile("(" + TRACK + ")(" + TITLE + ")(" + ALBUM + ")(" + ARTIST  + ")")
    DICT = {TRACK:tag.TRACK, TITLE:tag.TITLE, ALBUM:tag.TITLE, ARTIST:tag.ARTIST}
    
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
                eaten = self._eat(line, match)
                line = eaten[1]
                if currentMatch != "":
                   result[TagDictBuilder[match]] = eaten[0] 
            filtered = filtered[1:]
                
            
    def _eat(self, line, token):
        result = re.split(token,line,1)
        return [result[0], result[-1]]
        
    def _buildRegex(self, regex):
        splitted = TagDictBuilder.REGEX.split(regex)
        return [k for k in splitted if k != None]
        

class TagWriter:
    def __init__(self, file, tagDict):
        self.file = file
        self.tagDict = tagDict
    
    def run(self):
        pass
    
    def _writeTags(self):
        for tag in self.tagDict:
            self.file.setTag(tag, self.tagDict[tag])
            
    def _save(self):
        self.file.save()
        
if __name__ == "__main__":
    print "ok"
    
