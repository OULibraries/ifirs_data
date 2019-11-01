#!/usr/bin/env python

# A quick Python 2 script for making recipe files
# Because we're running it with the default CentOS 7 Python

import json 
import glob
import os
import uuid 

from pprint import pprint
from lxml import etree


#######################

# Set to base path for mp3s to load
mp3_path = ""

########################

script_path = os.path.dirname(os.path.abspath(__file__)) 
base = os.path.dirname(script_path)
metadata_path = "%s/metadata/" % base
tn_path = base
recipe_path = "%s/recipes" %base

# Calculate repository uuid namespace and make sure that 
# we're doing the math right.
repo_uuid = uuid.uuid5( uuid.NAMESPACE_DNS, 'repository.ou.edu')
assert( "eb0ecf41-a457-5220-893a-08b7604b7110" == str(repo_uuid))

# Make recipes for all of our metadata files
print('processing %s/*.xml' % metadata_path)
mods_files = glob.glob('%s/*.xml' % metadata_path)
for mf in mods_files:

  # Get Basename of tape and use to construct item uuid
  # For other collections, this would map to a bag name. 
  mf_filename = os.path.basename(mf)
  slug = mf_filename[0:-11]
  item_uuid = uuid.uuid5(repo_uuid, slug)
  
  # Get item title 
  tree = etree.parse(mf)
  title_tree = tree.xpath( '//mods:titleinfo/mods:title',
		       namespaces = {"mods":"http://www.loc.gov/mods/v3"})
  title = title_tree[0].text

  # Construct body of audio recipe
  recipe = {
    "import" : "audio",
    "update" : "true",
    "uuid"   : str(item_uuid),
    "label"  : title,
    "metadata" : { 
      "mods" : mf 
    },
    "files"  : {
      "obj": "%s/%s_Access.mp3" % (mp3_path, slug),
      "tn": "%s/recording-tn.jpg" % tn_path
    }
  }

  print(" writing to %s/%s.json" %(recipe_path, slug))

  with open('%s/%s.json' %(recipe_path, slug), 'w') as f:
    json.dump( { "recipe" : recipe }, f, indent=2,)
