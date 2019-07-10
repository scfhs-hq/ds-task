#!/usr/bin/env python
# -*- coding: utf-8 -*-



import xml.etree.ElementTree as ET
import pprint


osm_file = "Amsterdam61M.osm"

def count_secondary_tag(filename):
        tag_keys={}
        # find the count of keys in tags
        for event, elem in ET.iterparse(filename):            
            if elem.tag == 'tag' and 'k' in elem.attrib:
                if elem.get('k') in tag_keys.keys():
                    tag_keys[elem.get('k')]=tag_keys[elem.get('k')]+1
                else:
                    tag_keys[elem.get('k')]=1  
        # sort the tag in reverse order
        import operator
        sorted_keys = sorted(tag_keys.items(), key=operator.itemgetter(1)) 
        sorted_keys.reverse()    
        return sorted_keys    



if __name__ == '__main__':
    
    
    # audit/count secondary tag
    secondary_tag = count_secondary_tag(osm_file)
    print("counts of secondary tags:")
    print (len(secondary_tag))
    