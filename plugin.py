
## ----------------------------------------------------------------------
"""
NODESMITH

PLUGIN.PY

Generates the main plugin functions, as well as houses all work for 
the separate nodes and build system.

Created: 11 July 2016
Author: kiki
"""
## ----------------------------------------------------------------------

import json, os, re, string, sys
from collections import OrderedDict

from .mpxnode import MPxNodeCPP

## ----------------------------------------------------------------------

class PluginException(Exception):
	pass

## ----------------------------------------------------------------------

class Plugin(object):
	def __init__( self, filename=None, name=None, author=None, version=None,
			maya_lib_path=None, maya_include_path=None, constants=None ):
		self.name              = name
		self.author            = author
		self.version           = version
		self.maya_lib_path     = maya_lib_path
		self.maya_include_path = maya_include_path
		self.constants         = constants

		self.nodes = OrderedDict()

		if filename is not None:
			with open(filename, "r") as fp:
				data = json.load( fp )
				self.from_json( data )

	def from_json(self, data):
		p_typeID = re.compile( '0x([0-9A-Fa-f]{6})$' )

		base_attrs = [
			"name", "author",
			"version", "maya_lib_path",
			"maya_include_path"
		]

		for attr in base_attrs:
			if not attr in data:
				raise PluginException("Attribute %s missing in root plugin JSON object." % attr)
			self.__setattr__( attr, data[attr] )

		if 'constants' in data:
			constants = data['constants']
			if isinstance( constants, dict ):
				self.constants = constants
			else:
				raise PluginException( "Malformed JSON: 'constants' is not a dictionary." )
		else:
			self.constants = {}

		if 'nodes' in data:
			nodes = data['nodes']
			if not isinstance( nodes, dict ):
				raise PluginException( "Malformed JSON: 'constants' is not a dictionary." )

			for name, node_data in data['nodes'].items():
				node_name = node_data.pop( 'node_name', None )
				typeID = node_data.pop( 'id', None )

				if node_name is None:
					raise PluginException("Node %s: expected 'node_name' but found none." % name)

				if typeID is None:
					raise PluginException("Node %s: expected 'id' but found none." % name)
				else:
					## check for a malformed typeID-- should be in the format 0x123456
					if not p_typeID.match( typeID ):
						raise PluginException( "Malformed JSON: 'id' should be in format 0x123456 (found %s)" % typeID )
					else:
						typeID = eval( typeID )

				node = self.add_node( name, node_name, typeID, node_data )



	def to_json(self):
		result = {
			"name": self.name,
			"author": self.author,
			"version": self.version,
			"maya_lib_path": self.maya_lib_path,
			"maya_include_path": self.maya_include_path,
			"constants": self.constants,
			"nodes": {}
		}

	def add_node(self, class_name, node_name, typeID, data):
		print("\t+ Adding node %s..." % class_name)
		node = MPxNodeCPP( class_name, node_name, typeID )

		inputs  = data.pop( 'inputs',  None )
		outputs = data.pop( 'outputs', {} )

		if not isinstance(inputs, dict):
			raise PluginException( "Malformed JSON: node %s missing 'inputs'." % class_name )

		if not isinstance(outputs, dict):
			raise PluginException( "Malformed JSON: node %s missing 'outputs'." % class_name )

		for plug, inp_data in inputs.items():
			default = inp_data.pop('default', None)
			if default is None:
				raise PluginException( "Malformed JSON: input %s.%s has no 'default' value." % (class_name, plug) )
			node.add_input_plug( plug, default, **inp_data )

		for plug, outp_data in outputs.items():
			default = outp_data.pop('default', None)
			if default is None:
				raise PluginException( "Malformed JSON: output %s.%s has no 'default' value." % (class_name, plug) )
			node.add_output_plug( plug, default, **outp_data )

		self.nodes[class_name] = node

	def add_constant(self, name, value):
		self.constaints

	def generate_common_constants(self):
		result = ""

		for name, value in self.constants.items():
			result += "#define {name} {value}\n".format( name=name, value=value )

		return(result)

	def generate_common_header(self):
		result = ""

		with open( os.sep.join( [os.path.dirname( __file__ ), 'common_template.h'] ), 'r' ) as fp:
			template = fp.read()

		result = template.format(
			author=self.author,
			version=self.version,
			constants=self.generate_common_constants()
		)

		return(result)

	def generate_node_header_includes(self):
		result = ""
		for class_name in sorted(self.nodes.keys()):
			result += '#include "{class_name}.h";\n'.format( class_name=class_name )
		return( result )

	def generate_plugin_registration(self):
		result = ""
		for class_name in sorted( self.nodes.keys() ):
			node_inst = self.nodes[class_name]
			code = '\tstatus = plugin->registerNode( "{node_name}", {class_name}::id,\n' \
				'\t\t\t{class_name}::creator, {class_name}::initialize );\n' \
				'\tif (!stat) {{\n\t\tstat.perror("{class_name} registerNode");\n' \
				'\t\treturn stat;\n\t}}\n' \
				'\t{class_name}::aeTemplate();\n\n'

			## not doing data checks here since bad data
			## should be caught above on JSON load
			result += code.format(
				class_name=class_name,
				node_name=node_inst.node_name
			)

		return( result )

	def generate_plugin_deregistration(self):
		result = ""

		for class_name in sorted( self.nodes.keys() ):
			node_inst = self.nodes[class_name]
			code = '\tstatus = plugin->deregisterNode({class_name}::id);\n' \
				'\tif (!stat) {{\n\t\tstat.perror("{class_name} deregisterNode");\n' \
				'\t\treturn stat;\n\t}}\n\n'

			## not doing data checks here since bad data
			## should be caught above on JSON load
			result += code.format(
				class_name=class_name,
				node_name=node_inst.node_name
			)

		return( result )

	def generate_plugin_cpp(self):
		result = ""

		with open( os.sep.join( [os.path.dirname( __file__ ), 'plugin_main_template.cpp'] ), 'r' ) as fp:
			template = fp.read()

		result = template.format(
			author=self.author,
			version=self.version,
			node_header_includes=self.generate_node_header_includes(),
			plugin_registration=self.generate_plugin_registration(),
			plugin_deregistration=self.generate_plugin_deregistration()
		)

		return(result)

	def generate_plugin_cmake(self):
		result = ""
		return(result)
