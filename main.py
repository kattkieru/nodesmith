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

try:
	from implib import reload
except:
	from imp import reload

print(sys.argv[0])

basepath = os.path.dirname( os.path.abspath(os.path.dirname(sys.argv[0])) )
#basepath = os.sep.join( [basepath,'..'] )

if not basepath in sys.path:
	# print("Adding %s to path" % basepath)
	sys.path.insert( 0, basepath )


## ----------------------------------------------------------------------

from nodesmith import mpxnode
from nodesmith import plugin

for mod in mpxnode, plugin:
	reload(mod)

from nodesmith.plugin import Plugin


## ----------------------------------------------------------------------

print( "\n\nnodesmith.py" )

parser = argparse.ArgumentParser(
	description='Generate a Maya plugin from an input JSON description.'
)

parser.add_argument( 'filename', type=argparse.FileType('r') )
parser.add_argument( '-folder', metavar='folder', type=str,
				   help='Output location.', default='.' )
parser.add_argument( '-force', metavar='True | (False)', type=bool,
				   help='Overwrites existing files.', default=False )
parser.add_argument( '-debug', metavar='True | (False)', type=bool,
				   help='Enable debugging information.', default=False )

args = parser.parse_args()

if args.filename is None:
	parser.print_help()
	sys.exit(0)

with args.filename as fp:
	plugin_data = json.load( fp )

plugin = Plugin()
plugin.from_json( plugin_data )

print("Plugin: %s\n" % plugin.name )
print("+ Writing output to '%s'." % args.folder )


all_cpp_files = [ 'plugin_main.cpp' ]

with open(os.sep.join([args.folder, 'common.h']), 'w') as fp:
	print( "\t+ Writing common.h ..." )
	fp.write( plugin.generate_common_header() )

with open(os.sep.join([args.folder, 'plugin_main.cpp']), 'w') as fp:
	print( "\t+ Writing plugin_main.cpp ..." )
	fp.write( plugin.generate_plugin_cpp() )

for _, node in plugin.nodes.items():
	print( "\t+ Writing Node: %s" % node.class_name )

	header_name = '%s.h' % node.class_name
	class_name  = '%s.cpp' % node.class_name
	main_name   = '%s_main.cpp' % node.class_name

	with open(os.sep.join([args.folder, header_name]), 'w') as fp:
		print( "\t\t+ %s ..." % header_name )
		fp.write( node.generate_include() )

	with open(os.sep.join([args.folder, class_name]), 'w') as fp:
		print( "\t\t+ %s ..." % class_name )
		fp.write( node.generate_class() )
		all_cpp_files.append( class_name )

	with open(os.sep.join([args.folder, main_name]), 'w') as fp:
		print( "\t\t+ %s ..." % main_name )
		fp.write( node.generate_node_main() )
		all_cpp_files.append( main_name )

with open(os.sep.join([args.folder, 'CMakeList.txt']), 'w') as fp:
	print( "\t+ Writing CMake project ..." )
	fp.write( plugin.generate_common_header() )

print( "++ Project generation complete." )


