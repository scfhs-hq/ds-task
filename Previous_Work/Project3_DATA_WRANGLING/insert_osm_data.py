#!/usr/bin/env python
import xml.etree.ElementTree as ET
import pprint
import re
import codecs
import json
from pymongo import MongoClient
import os



# source : http://napitupulu-jon.appspot.com/posts/wrangling-openstreetmap.html
lower = re.compile(r'^([a-z]|_)*$')
lower_colon = re.compile(r'^([a-z]|_)*:([a-z]|_)*$')
problemchars = re.compile(r'[=\+/&<>;\'"\?%#$@\,\. \t\r\n]')
addresschars = re.compile(r'addr:(\w+)')
CREATED = [ "version", "changeset", "timestamp", "user", "uid"]
osm_file = 'updatedAmst2.osm'

def shape_element(element):
    #node = defaultdict(set)
    node = {}
    if element.tag == "node" or element.tag == "way" :
        #create the dictionary based on exaclty the value in element attribute.
        node = {'created':{}, 'type':element.tag}
        for k in element.attrib:
            try:
                v = element.attrib[k]
            except KeyError:
                continue
            if k == 'lat' or k == 'lon':
                continue
            if k in CREATED:
                node['created'][k] = v
            else:
                node[k] = v
        try:
            node['pos']=[float(element.attrib['lat']),float(element.attrib['lon'])]
        except KeyError:
            pass
        
        if 'address' not in node.keys():
            node['address'] = {}
        #Iterate the content of the tag
        for stag in element.iter('tag'):
            #Init the dictionry

            k = stag.attrib['k']
            v = stag.attrib['v']
            #Checking if indeed prefix with 'addr' and no ':' afterwards
            if k.startswith('addr:'):
                if len(k.split(':')) == 2:
                    content = addresschars.search(k)
                    if content:
                        node['address'][content.group(1)] = v
            else:
                node[k]=v
        if not node['address']:
            node.pop('address',None)
        #Special case when the tag == way,  scrap all the nd key
        if element.tag == "way":
            node['node_refs'] = []
            for nd in element.iter('nd'):
                node['node_refs'].append(nd.attrib['ref'])
#         if  'address' in node.keys():
#             pprint.pprint(node['address'])
        return node
    else:
        return None


def process_map(file_in, pretty = False):
    """
    Process the osm file to json file to be prepared for input file to monggo
    """
    file_out = "{0}.json".format(file_in)
    data = []
    with codecs.open(file_out, "w") as fo:
        for _, element in ET.iterparse(file_in):
            el = shape_element(element)
            if el:
                data.append(el)
                if pretty:
                    fo.write(json.dumps(el, indent=2)+"\n")
                else:
                    fo.write(json.dumps(el) + "\n")
    return data

data = process_map(osm_file)
pprint.pprint(data[10])


db_name = 'AmsOSM'
# Connect to Mongo DB
client = MongoClient('localhost:27017')  
db = client[db_name]  
c = db.AmsMAP
c.insert(data)
pprint.pprint(c)





print('size of data',db.AmsMAP.count()) # of data
print ('number of ways',db.AmsMAP.find({'type':'way'}).count()) # of way 
print ('number of nodes',db.AmsMAP.find({'type':'node'}).count()) # of nodes
print ('number of bicycle parkings',db.AmsMAP.find({'amenity':'bicycle_parking'}).count()) # how many bicycle parkings in Amsterdam old center
print ('number of tourism attractions',db.AmsMAP.find({'tourism':'attraction'}).count())# how many tourism attractions in Amsterdam old center 


#Looking into the top 10 cusines in the old cental
cuisine = db.AmsMAP.aggregate([
        {"$match" : {"cuisine" : {"$exists" : 1}}},
        {"$group" : {"_id" : "$cuisine",
                     "count" : {"$sum" : 1}}},
        {"$sort" : {"count" : -1}},
        {"$limit" : 5}
    ])
print ('The top 10 cuisine:') 
pprint.pprint([doc for doc in cuisine])


#most common amenity top 5

amenity = db.AmsMAP.aggregate([ 
                { "$group" : { "_id" : "$amenity","count": {"$sum": 1 }}},
                { "$sort" : { "count" : -1 }},
                { "$skip" : 1 },
                { "$limit" : 5 }
               ])
print ('top 5 common amrity:') 
pprint.pprint([doc for doc in amenity])



#
shops = db.AmsMAP.aggregate([
        {"$match" : {"shop" : {"$exists" : 1}}},
        {"$group" : {"_id" : "$shop",
                     "count" : {"$sum" : 1}}},
        {"$sort" : {"count" : -1}},
        {"$limit" : 15}
    ])
print ('The top 15 common shops:') 
pprint.pprint([doc for doc in shops])

#University
Uni = db.AmsMAP.aggregate([{"$match":{"amenity":{"$exists":1}, "amenity": "university", "name":{"$exists":1}}},
            {"$group":{"_id":"$name", "count":{"$sum":1}}},
            {"$sort":{"count":-1}}])
print ('The Universities in Amsterdam:') 
pprint.pprint([doc for doc in Uni])






