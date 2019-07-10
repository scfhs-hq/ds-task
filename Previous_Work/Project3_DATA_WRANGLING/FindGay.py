#!/usr/bin/env python
# -*- coding: utf-8 -*-


# load libraries
import xml.etree.cElementTree as ET
import os


osm_file = "Amsterdam61M.osm"
count = 1


def find_gay(osmfile):
	count = 1
	for event, elem in ET.iterparse(osm_file, events=("start",)):
		if elem.tag == "node" or elem.tag == "way":
			found_gay = False
			for tag in elem.iter("tag"):
				if tag.attrib['k'] == "gay" and  tag.attrib['v'] == "yes":
					count += 1
					found_gay = True
					break
			
			if found_gay == True:

				# we have found the node containing gay tag, so lets print the name
				for tag in elem.iter("tag"):
					if tag.attrib['k'] == "name":
						print(tag.attrib['v'])
						break
				
				# also lets print the lat and long values present in the node 
				# remember that we don't have lat, lon in way nodes
				if elem.tag == 'node':
					print("lat: " + elem.attrib['lat'] + ", lon: " + elem.attrib['lon'])
				

find_gay(osm_file)