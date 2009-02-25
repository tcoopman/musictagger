#!/usr/bin/python
# -*- coding: utf-8 -*-

import glob

from rename import TagDictBuilder
from rename import FileHandler
from rename import FileWriter
from rename import BatchRename
from tag import MyMp3


def buildTags(tagFile, builder, album, disc):
    lines = open(tagFile, "r").readlines()

    tags = []
    for line in lines:
        result = builder.build(line)
        result.setAlbum(album)
        result.setDisc(disc)
        tags.append(result)
    return tags
    
def buildFiles(musicFolder):
    files = glob.glob(musicFolder + "/*.mp3")
    mp3s = []
    for file in files:
        mp3s.append(MyMp3(file))
    return mp3s
    
def proces(tags, mp3, baseDir, schema):
    batch = BatchRename(tags, mp3s)
    batch.tagAll()
    fh = FileHandler()
    fileCollectionWriter = FileWriter(baseDir,schema, fh)
    for mp3 in mp3s:
        fileCollectionWriter.copy(mp3, True)

builder = TagDictBuilder("%track. %title - %artist")

tagFile1 = "/home/thomas/Workspace/musictagger/test/disco01"
tagFile2 = "/home/thomas/Workspace/musictagger/test/disco02"
tagFile3 = "/home/thomas/Workspace/musictagger/test/disco03"
tagFile4 = "/home/thomas/Workspace/musictagger/test/disco04"
tagFile5 = "/home/thomas/Workspace/musictagger/test/disco05"

musicFolder1 = "/home/thomas/Music/Unsorted/100 HITS DISCO (5CD)/CD1"
musicFolder2 = "/home/thomas/Music/Unsorted/100 HITS DISCO (5CD)/CD2"
musicFolder3 = "/home/thomas/Music/Unsorted/100 HITS DISCO (5CD)/CD3"
musicFolder4 = "/home/thomas/Music/Unsorted/100 HITS DISCO (5CD)/CD4"
musicFolder5 = "/home/thomas/Music/Unsorted/100 HITS DISCO (5CD)/CD5"

baseDir = "/home/thomas/Music/DJ/Disco/Various Artists/"
schema = "%album (disc %disc)/%track - %artist - %title"

tags = buildTags(tagFile1, builder, "100 Hits Disco", "1")
mp3s = buildFiles(musicFolder1)
proces(tags,mp3s, baseDir,schema)

tags = buildTags(tagFile2, builder, "100 Hits Disco", "2")
mp3s = buildFiles(musicFolder2)
proces(tags,mp3s, baseDir,schema)

tags = buildTags(tagFile3, builder, "100 Hits Disco", "3")
mp3s = buildFiles(musicFolder3)
proces(tags,mp3s, baseDir,schema)

tags = buildTags(tagFile4, builder, "100 Hits Disco", "4")
mp3s = buildFiles(musicFolder4)
proces(tags,mp3s, baseDir,schema)

tags = buildTags(tagFile5, builder, "100 Hits Disco", "5")
mp3s = buildFiles(musicFolder5)
proces(tags,mp3s, baseDir,schema)
