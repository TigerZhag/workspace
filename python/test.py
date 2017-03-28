#!/usr/bin/env python
# -*- coding: utf-8 -*-
import requests
import json
import download101

if __name__ == '__main__':
    # download101.downPPTtemp(0, 20, download101.rootDir + 'PPT_Template' + '/')
    # proSchool = 'KPRO'
    # download101.work('/v0.6/categories/relations?patternPath=%s' % proSchool)
    # rjson = requests.get('http://esp-lifecycle.web.sdp.101.com/v0.6/teachingmaterials/837fdaff-7d57-483e-bc06-acb74913f801/chapters/none/subitems').json()
    # topic = ''
    # for chapter in rjson['items']:
    #     if(chapter['parent'] == chapter['teaching_material']):
    #         topic = chapter['title']
    #         print '--' + topic
    #     else:
    #         print '----download ' + topic + '--' + chapter['title']
    with open(download101.rootDir + 'downloadrecord.log', 'w+') as handle:
        rjson = [
            {
                'school':"小学",
                'grades':[
                    {
                        'grade':"一年级",
                        'courses':[
                            {
                                'course':"语文",
                            }
                        ]
                    },
                    {
                        'grade':"二年级",
                        'courses':[
                            {
                                'course':"语文",
                            }
                        ]
                    },
                    {
                        'grade':"三年级",
                        'courses':[
                            {
                                'course':"语文",
                            }
                        ]
                    },
                ],
            },
            {
                'school':"初中"
            }
        ]
        json.dump(rjson, handle)
