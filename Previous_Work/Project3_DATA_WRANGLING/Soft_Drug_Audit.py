#!/usr/bin/env python
# -*- coding: utf-8 -*-

# load libraries
import xml.etree.cElementTree as ET

# refer to the link for medhods used
# https://docs.python.org/2/library/xml.etree.elementtree.html

def update_save(oldfile, newfile):
    tree = ET.parse(oldfile)
    root = tree.getroot()


    for tag in root.iter('tag'):
        #here we have all the tag elements
        # check for the key = shop and v contaings drug
        if tag.attrib['k'] == 'shop' and tag.attrib['v'] == "soft_drugs":
            # update the value to drug store
            tag.set('v', 'drug store')
        # if the v == coffee_shop and k = cuisine
        elif tag.attrib['v'] == 'soft_drugs' and tag.attrib['k'] == 'cuisine':
            # update the value to drug store
            tag.set('v', 'drug store')
    
    tree.write(newfile,encoding="UTF-8", xml_declaration=True, default_namespace=None, method="xml")

update_save('updatedAmst.osm', 'updatedAmst2.osm')