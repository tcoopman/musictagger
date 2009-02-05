# -*- coding: utf-8 -*-
import sys
import time
sys.path.append("../src/")

import tag
from rename import *


class TestTagDictBuilder:
    def setup_method(self,method):
        self.a = "1-KidsWorld MiniDisco-Ko en Kiki-Ko en Kiki lied"
        self.b = "2-KidsWorld MiniDisco-Ko en Kiki-Beginnen"
        self.c = "3-KidsWorld MiniDisco-Ko en Kiki-Hallo"
        self.tdb1 = TagDictBuilder("%track-%album-%artist-%title")
        
    def test_init1(self):
        tdb = TagDictBuilder("%track-%album-%artist-%title")
        assert ['', '%track', '-', '%album', '-', '%artist', '-', '%title', '']==tdb.regex
        
    def test_init2(self):
        tdb = TagDictBuilder("%album-%artist-%title")
        assert ['', '%album', '-', '%artist', '-', '%title', '']==tdb.regex
        
    def test_init3(self):
        tdb = TagDictBuilder("%albumxx-xx%artist - %title")
        assert ['', '%album', 'xx-xx', '%artist', ' - ', '%title', '']==tdb.regex
        
    def test_init4(self):
        tdb = TagDictBuilder("/%album/%artist/ %track -*- %title.mp3")
        assert ['/', '%album', '/', '%artist', '/ ', '%track', ' -*- ', '%title', '.mp3'] ==tdb.regex
        
    def test__eat1(self):
        result = self.tdb1._eat(self.a, '')
        assert self.a == result[0]
        assert self.a == result[1]
        
    def test__eat2(self):
        a = "xxxNext"
        result = self.tdb1._eat(a, "xxx")
        print result
        assert "xxx" == result[0]
        assert "Next" == result[1]
        
    def test_eat3(self):
        a = "xxx Next"
        result = self.tdb1._eat(a, "xxx")
        print result
        assert "xxx" == result[0]
        assert " Next" == result[1]
        
    def test_eat4(self):
        a = "xxx * Next"
        result = self.tdb1._eat(a, "xxx")
        print result
        assert "xxx" == result[0]
        assert " * Next" == result[1]
        
    def test_build1(self):
        result = self.tdb1.build(self.a)
        assert result[tag.TRACK] == "1"
        assert result[tag.TITLE] == "Ko en Kiki lied"
        assert result[tag.ALBUM] == "KidsWorld MiniDisco"
        assert result[tag.ARTIST] == "Ko en Kiki"
        
    def test_build2(self):
        result = self.tdb1.build(self.b)
        assert result[tag.TRACK] == "2"
        assert result[tag.TITLE] == "Beginnen"
        assert result[tag.ALBUM] == "KidsWorld MiniDisco"
        assert result[tag.ARTIST] == "Ko en Kiki"
        
    def test_build3(self):
        result = self.tdb1.build(self.c)
        assert result[tag.TRACK] == "3"
        assert result[tag.TITLE] == "Hallo"
        assert result[tag.ALBUM] == "KidsWorld MiniDisco"
        assert result[tag.ARTIST] == "Ko en Kiki"
        
    def test_build4(self):
        line = "/album/artist/ 111 -x- title with spaces.mp3"
        tdb = TagDictBuilder("/%album/%artist/ %track -x- %title.mp3")
        result = tdb.build(line)
        print result
        assert result[tag.TRACK] == "111"
        assert result[tag.TITLE] == "title with spaces"
        assert result[tag.ALBUM] == "album"
        assert result[tag.ARTIST] == "artist"
        
    def test_build5(self):
        line = "/album/artist/ 111 -*- title with spaces.mp3"
        tdb = TagDictBuilder("/%album/%artist/ %track -*- %title.mp3")
        result = tdb.build(line)
        print result
        assert result[tag.TRACK] == "111"
        assert result[tag.TITLE] == "title with spaces"
        assert result[tag.ALBUM] == "album"
        assert result[tag.ARTIST] == "artist"
        
        
class TestTagWriter:
    def setup_method(self, method):
        self.wfile1path = "mp3/test3.mp3"
        self.wfile2path = "mp3/test4.mp3"
        self.wfile1 = MyMp3(self.wfile1path)
        self.wfile2 = MyMp3(self.wfile2path)
        self.tagTrack = str(time.time() + 0)
        self.tagTitle = str(time.time() + 1)
        self.tagAlbum = str(time.time() + 2)
        self.tagArtist = str(time.time() + 3)
        self.tagDict = {tag.TRACK:self.tagTrack, tag.TITLE:self.tagTitle, tag.ALBUM:self.tagAlbum, tag.ARTIST:self.tagArtist}
        
    def test_writeTags1(self):
        tw = TagWriter(self.wfile1)
        tw.writeTags(self.tagDict)
        assert self.tagTrack == self.wfile1.track()
        assert self.tagTitle == self.wfile1.title()
        assert self.tagArtist == self.wfile1.artist()
        assert self.tagAlbum == self.wfile1.album()
        
    def test_writeTags2(self):
        tw = TagWriter(self.wfile2)
        tw.writeTags(self.tagDict)
        assert self.tagTrack == self.wfile2.track()
        assert self.tagTitle == self.wfile2.title()
        assert self.tagArtist == self.wfile2.artist()
        assert self.tagAlbum == self.wfile2.album()
        
    def test_saveTags1(self):
        tw = TagWriter(self.wfile1)
        tw.writeTags(self.tagDict)
        tw.save()
        wfile1 = MyMp3(self.wfile1path)
        assert self.tagTrack == wfile1.track()
        assert self.tagTitle == wfile1.title()
        assert self.tagArtist == wfile1.artist()
        assert self.tagAlbum == wfile1.album()
        
    def test_saveTags2(self):
        tw = TagWriter(self.wfile2)
        tw.writeTags(self.tagDict)
        tw.save()
        wfile2 = MyMp3(self.wfile2path)
        assert self.tagTrack == wfile2.track()
        assert self.tagTitle == wfile2.title()
        assert self.tagArtist == wfile2.artist()
        assert self.tagAlbum == wfile2.album()
        
class TestFileWriter:
    def setup_method(self, method):
        self.fw = FileWriter("","%artist/%album/%track - %title")
        self.rfile1 = MyMp3("mp3/test1.mp3")
        self.rfile2 = MyMp3("mp3/test2.mp3")
        
    def test__translateSchema1(self):
        schema = self.fw._translateSchema(self.rfile1)
        assert self.rfile1.artist() + "/" + self.rfile1.album() + "/" + self.rfile1.track() + " - " + self.rfile1.title() == schema
        
    def test__translateSchema2(self):
        schema = self.fw._translateSchema(self.rfile2)
        assert self.rfile2.artist() + "/" + self.rfile2.album() + "/" + self.rfile2.track() + " - " + self.rfile2.title() == schema
        
        