# -*- coding: utf-8 -*-
import sys
sys.path.append("../src/")

import tag
from rename import TagDictBuilder


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