#!/usr/bin/env python
# -*- coding: utf-8 -*-

import xml.etree.cElementTree as ET
from collections import defaultdict
import re
import pprint


fname = "sample61M.osm"


# Define a function to count all types of tags in the xml file
def count_tags(filename):
    tags_dict = defaultdict(int)
    for event, elem in ET.iterparse(filename, events=("start",)):
        tags_dict[elem.tag] += 1
    return tags_dict



if __name__ == '__main__':
    
    # audit/count tag
    tags = count_tags(fname)
    print("counts of primary tags:")
    pprint.pprint(tags)
    