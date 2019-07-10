#!/usr/bin/env python
# -*- coding: utf-8 -*-


# load libraries
import xml.etree.cElementTree as ET
import os


# refer to the link for medhods used
# https://docs.python.org/2/library/xml.etree.elementtree.html

def update_way(oldfile, newfile):
    tree = ET.parse(oldfile)
    root = tree.getroot()


    for tag in root.iter('tag'):
        #bike_frindly = False
        #here we have all the tag elements
        # check for the key = shop and v contaings drug
        if tag.attrib['k'] == "maxspeed" and tag.attrib['v'] == "30" and tag.attrib['v'] == "unclassified":
            tag.set('v', 'Bicycle Friendly')
                
    tree.write(newfile,encoding="UTF-8", xml_declaration=True, default_namespace=None, method="xml")

update_way('updatedAmst.osm','updatedAmst2.osm')