## ----------------------------------------------------------------------
"""
NODESMITH

NODESMITH.PY

Command-line launcher for the nodesmith api. Can be used to generate
an entire plugin structure from an input JSON file.

Created: 12 July 2016
Author: kiki
"""
## ----------------------------------------------------------------------

import argparse
import json
import os
import re
import string
import sys

print(sys.argv[0])

basepath = os.path.dirname( os.path.abspath(os.path.dirname(sys.argv[0])) )
#basepath = os.sep.join( [basepath,'..'] )

if not basepath in sys.path:
	print("Adding %s to path" % basepath)
	sys.path.insert( 0, basepath )


## ----------------------------------------------------------------------

from nodesmith import mpxnode
from nodesmith import plugin

for mod in mpxnode, plugin:
	reload(mod)

from nodesmith.plugin import Plugin


## ----------------------------------------------------------------------

print( "nodesmith.py" )

parser = argparse.ArgumentParser(
	description='Generate a Maya plugin from an input JSON description.'
)

parser.add_argument( 'filename', type=argparse.FileType('r') )
parser.add_argument( '-force', metavar='True | (False)', type=bool,
                   help='Overwrites existing files.', default=False )
parser.add_argument( '-debug', metavar='True | (False)', type=bool,
                   help='Enable debugging information.', default=False )

result = parser.parse_args()

if result.filename is None:
	parser.print_help()
	sys.exit(0)

with result.filename as fp:
	plugin_data = json.load( fp )

plugin = Plugin()
plugin.from_json( plugin_data )

print("Plugin: %s" % plugin.name )

print("Writing source files...")

filename = "common.cpp"
with open(filename, "w") as fp:
	print("\t+ %s..." % filename)
	fp.write( plugin.generate_common_header() )

filename = "plugin_main.cpp"
with open(filename, "w") as fp:
	print("\t+ %s..." % filename)
	fp.write( plugin.generate_plugin_cpp() )

for filename, node in plugin.nodes.items():
	with open("%s.h" % filename, "w") as fp:
		print("\t+ %s.h..." % filename)
		fp.write( node.generate_include() )
	with open("%s.cpp" % filename, "w") as fp:
		print("\t+ %s.cpp..." % filename)
		fp.write( node.generate_class() )

print("++ Generation complete.")






