#!/usr/bin/env python
# -*- coding: utf-8 -*-



# to the dictionary keys

import xml.etree.cElementTree as ET

osm_file = "Amsterdam61M.osm"



# functions to find the counts of contributed users the old center area

#set the users
def get_user(element):
    return element.get("user")

#find and count
def count_unique(filename):
    users = set()
    print(users)
    for _, element in ET.iterparse(filename):
        if "user" in element.attrib:
            users.add(get_user(element))
    print(users)
    print(len(users))




if __name__ == '__main__':
    
    users = count_unique(osm_file)
