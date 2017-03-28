#!/usr/bin/env python
# -*- coding: utf-8 -*-
#script to download 101PPT resources
#anthor: zhang shixin
#email: tiger.zhag@gmail.com
#date: 2017.3.8

import requests
import json
import os
from contextlib import closing

hostConfig = 'http://esp-lifecycle.web.sdp.101.com'
hostDownload = 'http://cdncs.101.com/v0.1/download?path='
rootDir = '/home/tiger/101resources/101resources/'

normalSchool = 'K12'
proSchool = 'KPRO'
schoolLevel = proSchool
def getCourses(gradeCode):
    u1 = '/v0.6/categories/relations?patternPath=%s/%s' % (schoolLevel, gradeCode)
    url = hostConfig + u1
    rjson = requests.get(url).json()
    try:
        return rjson[0]['items']
    except:
        return {}

def getVersion(gradeCode, courseCode):
    u1 = '/v0.6/categories/relations?patternPath=%s/%s/%s' % (schoolLevel, gradeCode, courseCode)
    url = hostConfig + u1
    rjson = requests.get(url).json()
#    print url
    try:
        versions = rjson[0]['items']
    except:
        return []
    return versions


def getBookInfo(schoolCode, gradeCode, courseCode, versionCode, seasonCode):
    u1 = r'/v0.6/teachingmaterials/actions/query?&include=TI,EDU,CG&category=%s/%s/%s/%s/%s/%s&relation&coverage=Org/nd/&prop&words&limit=(0,20)' % (schoolLevel, schoolCode, gradeCode, courseCode, versionCode, seasonCode)
    url = hostConfig + u1;
    rjson = requests.get(url).json()
    try:
        return rjson['items'][0]
    except:
        return {}

def getChapter(bookUuid):
    u1 = '/v0.6/teachingmaterials/%s/chapters/none/subitems' % bookUuid
    url = hostConfig + u1;
    rjson = requests.get(url).json()
    return rjson['items']

def downloadPPT(identifier, start, total, dstDir):
    u1 = '/v0.6/coursewares/actions/query?words&limit=(%d,%d)&include=TI,LC&category&relation=chapters/%s/ASSOCIATE&coverage=Org/nd/' % (start, total+start,identifier)
    url = hostConfig + u1
    rjson = requests.get(url).json()
    ppts = rjson['items']
    totalCount = rjson['total']
    for ppt in ppts:
        #TODO download the PPT
        print '\r------------ download PPT:' + ppt['title'],
        pptSrc = ppt['tech_info']['source']['location'].replace('${ref-path}', hostDownload)
        pptDst = dstDir + ppt['title'] + '.ppt'
        downloadTo(pptSrc, pptDst)
    if(total + start < totalCount):
        downloadPPT(identifier,total+start, total)

def downloadMedia(identifier, dstDir):
    categories = ['$RA0101', "$RA0102", "$RA0103", '$RA0104']
    dict = {
        categories[0]:'image',
        categories[1]:'audio',
        categories[2]:'video',
        categories[3]:'gif',
    }
    def downloadCategoryMedia(category, start, total, detaildstDir):
        u1 = '/v0.6/assets/actions/query?words&limit=(%d,%d)&include=TI&category=%s&relation=chapters/%s/ASSOCIATE&coverage=Org/nd/' % (start, total+start, category, identifier)
        url = hostConfig + u1
        rjson = requests.get(url).json()
        totalCount = rjson['total']
        for media in rjson['items']:
            #TODO download the midia
            print '\r--------------' + media['title'],
            mediaSrc = media['tech_info']['source']['location'].replace('${ref-path}', hostDownload)
            mediaDst = detaildstDir + media['title'] + '.' + mediaSrc.split('.')[-1]
            downloadTo(mediaSrc, mediaDst)
        if(total + start < totalCount):
            downloadCategoryMedia(category, start + total, total, detaildstDir)
    for category in categories:
        downloadCategoryMedia(category, 0, 20, dstDir + '/' + dict[category] + '/')

def downPPTtemp(start, total, dstDir):
    u1 = '/v0.6/assets/actions/query?words&limit=(%d,%d)&include=TI,LC&category=$RA0501 and $F050003&category&coverage=Org/nd/' % (start, start + total)
    url = hostConfig + u1
    rjson = requests.get(url).json()
    totalCount = rjson['total']
    for temp in rjson['items']:
        print '\r--------------Download PPT template ' + temp['title'],
        tempSrc = temp['tech_info']['source']['location'].replace('${ref-path}', hostDownload)
        tempDst = dstDir + temp['title'] +'.' + tempSrc.split('.')[-1]
        downloadTo(tempSrc, tempDst)
    if(total + start < totalCount):
        downPPTtemp(total + start, total, dstDir)

def downloadTo(url, dst):
    try:
        r = requests.get(url, stream=True)
        ensureDir(dst)
        if not os.path.exists(dst):
            print '----download file--'
            with open(dst, "wb") as handle:
                for chunk in r.iter_content(chunk_size = 1024):
                    if(chunk):
                        handle.write(chunk)
                handle.flush()
                handle.close()
    except:
        with open(rootDir + 'download_error.log', 'w+') as handle:
            handle.write(url + '////')
            handle.flush()
            handle.close()

def ensureDir(file_path):
    directory = os.path.dirname(file_path)
    if not os.path.exists(directory):
        os.makedirs(directory)

def work(getGradeUrl):
    # get and parse the grade list
    rjson = requests.get(hostConfig + getGradeUrl).json()
    schools = rjson[0]['items']
    for school in schools[0:1]:
        print school['target']['title'] + '-----------------------------------------'
        grades = school['level_items']
        for grade in grades[2:3]:
            print '--' + grade['target']['title']
            gradeCode = grade['target']['nd_code']
            for course in getCourses(gradeCode)[4:]:
                courseDst = rootDir + school['target']['title'] + '/' + \
                                  grade['target']['title'] + '/' + \
                                  course['target']['title'] + '/'
                ensureDir(courseDst)
                print '----', course['target']['title']
                courseCode = course['target']['nd_code']
                for version in getVersion(gradeCode, courseCode):
                    print '------' + version['target']['title']
                    versionCode = version['target']['nd_code']
                    for season in version['level_items']:
                        seasonCode = season['target']['nd_code']
                        bookUuid = getBookInfo(school['target']['nd_code'],gradeCode, courseCode, versionCode, seasonCode)
                        if(bool(bookUuid)):
                            #download book coverage
                            bookDst = courseDst + \
                                  version['target']['title'] + '/' + \
                                  season['target']['title'] + '/'
                            try:
                                downloadTo(bookUuid['preview']['fm'].replace('${ref-path}', hostDownload), bookDst + '/fm.jpg')
                            except:
                                print('this book has no preview')
                            chapters = getChapter(bookUuid['identifier'])
                            topics = {}
                            for chapter in chapters:
                                if(chapter['parent'] == chapter['teaching_material']):
                                    topics.update(chapter['parent']=bookDst + chapter['title'] + '/')
                                    ensureDir(bookDst + '/' + topic + '/')
                                    print '\n--------' + topic
                                else:
                                    sectionDst = topics.get(chapter['parent'], '') + chapter['title'] + '/'
                                    print '----------' + chapter['title']
                                    chapterIdentifier = chapter['identifier'] + '/'
                                    topics.update(chapterIdentifier=sectionDst)
                                    ensureDir(sectionDst)
                                    #sectionDst = bookDst + topic + '/' + chapter['title'] + '/'
                                    PPTDst = sectionDst + 'PPT/'
                                    downloadPPT(chapterIdentifier, 0, 20, PPTDst)
                                    downloadMedia(chapterIdentifier, sectionDst + 'Media/')
    # downPPTtemp(0, 20, rootDir + 'PPT_Template' + '/')

if __name__ == '__main__':
    print 'start download 101 resources\n'
    normalSchool = 'K12'
    schoolLevel = normalSchool
    work('/v0.6/categories/relations?patternPath=%s' % normalSchool)
    # proSchool = 'KPRO'
    # work('/v0.6/categories/relations?patternPath=%s' % proSchool)
