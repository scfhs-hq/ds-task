#!/usr/bin/env python
# -*- coding: utf-8 -*-


# load libraries
import xml.etree.cElementTree as ET

osm_file = "Amsterdam61M.osm"
count = 0


def find_gay(osmfile):
	count = 0
	#parse the file
	for event, elem in ET.iterparse(osm_file, events=("start",)):
		#check both ways and node tags
		if elem.tag == "node" or elem.tag == "way":
			#check the key at the tag
			for tag in elem.iter("tag"):
				#check the condition
				if tag.attrib['k'] == "gay" and  tag.attrib['v'] == "yes":
					#print(tag.attrib['k'] + " friendly place number: " + str(count))
					count += 1
	print ("There are " + str(count) + " gay friendly place at the old center of Amsterdam")
					
					

find_gay(osm_file)

