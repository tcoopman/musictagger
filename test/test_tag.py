# -*- coding: utf-8 -*-

import sys
sys.path.append("../src/")

from tag import MyMp3
import time


class TestMyMp3:
    def setup_method(self, method):
        self.wfile1path = "mp3/test3.mp3"
        self.wfile2path = "mp3/test4.mp3"
        self.rfile1 = MyMp3("mp3/test1.mp3")
        self.rfile2 = MyMp3("mp3/test2.mp3")
        self.wfile1 = MyMp3(self.wfile1path)
        self.wfile2 = MyMp3(self.wfile2path)
        self.tag = str(time.time())
        
    def test_artist(self):
        assert "artist1" == self.rfile1.artist()
        assert "artist2" == self.rfile2.artist()
        
    def test_album(self):
        assert "album1" == self.rfile1.album()
        assert "album2" == self.rfile2.album()
        
    def test_track(self):
        assert "1" == self.rfile1.track()
        assert "2" == self.rfile2.track()
        
    def test_title(self):
        assert "title1" == self.rfile1.title()
        assert "title2" == self.rfile2.title()
        
    def test_setArtist(self):
        self.wfile1.setArtist(self.tag)
        assert self.tag == self.wfile1.artist()
        
        self.wfile2.setArtist(self.tag)
        assert self.tag == self.wfile2.artist()
        
    def test_setAlbum(self):
        self.wfile1.setAlbum(self.tag)
        assert self.tag == self.wfile1.album()
        
        self.wfile2.setAlbum(self.tag)
        assert self.tag == self.wfile2.album()
        
    def test_setTrack(self):
        self.wfile1.setTrack(self.tag)
        assert self.tag == self.wfile1.track()
        
        self.wfile2.setTrack(self.tag)
        assert self.tag == self.wfile2.track()
        
    def test_setTitle(self):
        self.wfile1.setTitle(self.tag)
        assert self.tag == self.wfile1.title()
        
        self.wfile2.setTitle(self.tag)
        assert self.tag == self.wfile2.title()
        
    def test_save1(self):
        self.wfile1.setTrack(self.tag)
        self.wfile1.setTitle(self.tag)
        self.wfile1.setAlbum(self.tag)
        self.wfile1.setArtist(self.tag)
        self.wfile1.save()
        file = MyMp3(self.wfile1path)
        assert self.tag == file.track()
        assert self.tag == file.title()
        assert self.tag == file.album()
    
    def test_save2(self):
        self.wfile2.setTrack(self.tag)
        self.wfile2.setTitle(self.tag)
        self.wfile2.setAlbum(self.tag)
        self.wfile2.setArtist(self.tag)
        self.wfile2.save()
        file = MyMp3(self.wfile2path)
        assert self.tag == file.track()
        assert self.tag == file.title()
        assert self.tag == file.album()
        assert self.tag == file.artist()