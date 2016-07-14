
## ----------------------------------------------------------------------
"""
NODESMITH

MPXNODE.PY

Generates MPxNode C++ subclasses and related functions.

Created: 30 April 2016
Author: kiki
"""
## ----------------------------------------------------------------------

import os, string, sys

## ----------------------------------------------------------------------

try:
	StringTypes = ( str, unicode )
except:
	StringTypes = str

kShort = 1
kFloat = 2
kFloat3 = 3
kDouble = 4
kDouble3 = 5
kMatrix = 6
kPoint = 7
kRamp = 8
kBoolean = 9
kUnit = 10
kTyped = 11
kCompound = 12

types_mapping_table = {
	'short'    : 'short',
	'float'    : 'float',
	'float3'   : 'MFloatVector',
	'double'   : 'double',
	'double3'  : 'MVector',
	'matrix'   : 'MMatrix',
	'point'    : 'MPoint',
	'bool'     : 'bool',
	'unit'     : 'double',

	'angle'    : 'double',
	'angle3'   : 'MVector',

	'ramp'     : None,
	'typed'    : None,
	'compound' : None,
}

grab_mapping_table = {
	'short'    : 'asShort',
	'float'    : 'asFloat',
	'float3'   : 'asMFloatVector',
	'double'   : 'asDouble',
	'double3'  : 'asMVector',
	'matrix'   : 'asMMatrix',
	'point'    : 'asMVector',
	'bool'     : 'asShort',
	'unit'     : 'asDouble',

	'angle'    : 'asDouble',
	'angle3'   : 'asMVector',

	'ramp'     : None,
	'typed'    : None,
	'compound' : None,
}

set_mapping_table = {
	'short'    : 'setShort',
	'float'    : 'setFloat',
	'float3'   : 'setMFloatVector',
	'double'   : 'setDouble',
	'double3'  : 'setMVector',
	'matrix'   : 'setMMatrix',
	'point'    : 'setMVector',
	'bool'     : 'setShort',
	'unit'     : 'setDouble',

	'angle'    : 'setDouble',
	'angle3'   : 'setMVector',

	'ramp'     : None,
	'typed'    : None,
	'compound' : None,
}

## ----------------------------------------------------------------------
class MPxNodeCPPException(Exception):
	pass


## ----------------------------------------------------------------------
class MPxNodeCPP(object):

	def __init__( self, class_name, node_name, typeID ):
		"""
		Standard initializer.
		:param class_name: Name of subclass.
		:param typeID: MTypeID value. Should be from a registered node block.
		"""
		self.class_name = class_name
		self.node_name = node_name
		if not isinstance(typeID, StringTypes):
			self.typeID = '0x%6x' % typeID    ## converts to hex
		else:
			self.typeID = typeID
		self.attributes = {}

	@property
	def sorted_attributes(self):
		"""
		Sometimes it's useful to have the attribute names
		in sorted order, so this sorts and re-pairs for
		quick looping.

		:return: zip() of alpabetically-sorted name:data pairs
		"""
		names = sorted( self.attributes.keys() )
		all_data = [ self.attributes[x] for x in names ]
		return( zip(names, all_data) )

	def add_plug( self, plug, default, is_input, type='float', min=None, max=None, 
					array=None, keyable=None, storable=None, readable=None, 
					writable=None, cached=None, hidden=None, short_name=None ):
		"""
		Adds a definition for a node plug.
		:param plug: The name of the plug.
		:param default: Default value for the plug.
		:param is_input: If True, the attribute will be created as an input attribute
			and its data will be collected at the top of the generated compute. If False,
			the attribute will be treated as an output attribute and its value will be set
			through the data block at the end of the compute.
		:param type: The type of plug. Must be an integer constant.
		:param min: If not None, the minimum value.
		:param max: If not None, the maximum value.
		:param array: bool: Is this an array attribute?
		:param keyable: bool: Can this plug accept keys?
		:param storable: bool: Does this get saved with the file?
		:param readable: bool: Can this be a source for plug connections?
		:param writable: bool: Can this be a target for plug connections?
		:param cached: bool: Plug caches values (good for outputs for rigs)
		:param hidden: bool: Plug is hidden and does not show up in the channel
			box or in the AE.
		:param short_name: If not None, specifies the short name of the plug.
			If None, the long name will also be used as the short name.
		:return: No return value
		"""

		if not type in types_mapping_table:
			raise MPxNodeCPPException( "Invalid plug type %s." % type )

		attr_name = 'i' if is_input else 'o'
		attr_name += plug[0].upper() + plug[1:]

		attribute_data = {
			"default":    default,
			"type":       type,
			"is_input":   True if is_input else False,
			"min":        min,
			"max":        max,
			"array":      array,
			"keyable":    keyable,
			"storable":   storable,
			"readable":   readable,
			"writable":   writable,
			"cached":     cached,
			"hidden":     hidden,
			"short_name": short_name,
			"attr_name":  attr_name,
		}

		self.attributes[plug] = attribute_data

	def add_input_plug(self, plug, default, type='float', min=None, max=None, array=False,
					keyable=True, storable=None, cached=None,
					hidden=None, short_name=None ):

		return( self.add_plug(plug, default, True, type=type, min=min, max=max, array=array,
				keyable=keyable, storable=storable, readable=False, writable=True, 
				cached=cached, hidden=hidden, short_name=short_name ) )

	def add_output_plug( self, plug, default, type='float', min=None, max=None, array=False,
						keyable=False, storable=None, cached=None,
						hidden=None, short_name=None ):

		return (self.add_plug( plug, default, False, type=type, min=min, max=max, array=array,
			   storable=storable, readable=True, writable=False, cached=cached,
			   hidden=hidden, short_name=short_name ))

	def generate_header_attributes(self, inputs=False ):
		result = ""
		for name, data in self.attributes.items():
			if data['is_input'] is inputs:
				result += "\tstatic MObject %s;\n" % (data['attr_name'])
		return(result)

	def generate_cpp_static_attributes(self, inputs=False ):
		result = ""

		for name, data in self.attributes.items():
			if data['is_input'] is inputs:
				result += "MObject %s::%s;\n" % (self.class_name, data['attr_name'])

		return(result)

	def generate_cpp_constants(self):
		result = ""

		return (result)

	def generate_private_variables(self):
		result = ""

		for name, data in self.attributes.items():
			default, aType, is_input, aMin, aMax, array, keyable, storable, readable, \
				writable, cached, hidden, short_name, attr_name = self.extract_attribute_data( data )

			if not array:
				result += '\t{variable_type} {name};\n'.format( 
					variable_type=types_mapping_table[data['type']], name=name
				)

		return(result)

	def generate_include(self):
		"""
		Generates the C++ header file for the class.
		:return: The string for the header file all constructed.
		"""

		with open( os.sep.join( [os.path.dirname( __file__ ), 'mpxnode_template.h'] ), 'r' ) as fp:
			template = fp.read()

		result = template.format(
			class_name=self.class_name,
			inputs=self.generate_header_attributes( inputs=True ),
			outputs=self.generate_header_attributes( inputs=False ),
			private_variables=self.generate_private_variables()
		)

		return( result )

	def generate_cpp_plug_check(self, inputs=False):
		result = None

		for name, data in self.attributes.items():
			if data['is_input'] is inputs:
				if result is None:
					result = "\t\t   "
				else:
					result += "\t\t|| "
				result += "plug == {attr_name} || plug.parent() == {attr_name}\n".format( attr_name=data['attr_name'] )

		return(result)

	def extract_attribute_data(self, data):
		default    = data.get('default', None)
		aType      = data.get('type', None)
		is_input   = data.get('is_input', None)
		aMin       = data.get('min', None)
		aMax       = data.get('max', None)
		array      = data.get('array', None)
		keyable    = data.get('keyable', True if is_input else False)
		storable   = data.get('storable', True if is_input else False)
		readable   = data.get('readable', False if is_input else True)
		writable   = data.get('writable', True if is_input else False)
		cached     = data.get('cached', True if is_input else False)
		hidden     = data.get('hidden', None)
		short_name = data.get('short_name', None)
		attr_name  = data.get('attr_name', None)

		return( default, aType, is_input, aMin, aMax, array, keyable, storable,
				readable, writable, cached, hidden, short_name, attr_name )

	def generate_cpp_collect_inputs(self):
		result = ""

		for name, data in self.sorted_attributes:

			default, aType, is_input, aMin, aMax, array, keyable, storable, \
				readable, writable, cached, hidden, short_name, attr_name = self.extract_attribute_data( data )

			if is_input is True:
				if not array:
					result += "\t\t{name} = data.inputValue({attr_name}).{grab_type}();\n".format(
						name=name,
						attr_name=attr_name,
						grab_type = grab_mapping_table[aType]
					)
				else:
					raise NotImplementedError( "array plugs not implemented for value collection yet." )

		return (result)

	def generate_cpp_set_outputs(self):
		result = ""

		for name, data in self.sorted_attributes:

			default, aType, is_input, aMin, aMax, array, keyable, storable, \
				readable, writable, cached, hidden, short_name, attr_name = self.extract_attribute_data( data )

			if is_input is not True:
				if not array:
					code  = "\t\tMDataHandle h_{name} = data.outputValue({attr_name});\n"
					code += "\t\th_{name}.{set_type}({name});\n\n"
					code  = code.format(
						name=name,
						attr_name=attr_name,
						set_type = set_mapping_table[aType]
					)

					result += code
				else:
					raise NotImplementedError( "array plugs not implemented for setting yet." )

		return (result)

	def generate_set_all_clean(self):
		result = ""

		for name, data in self.sorted_attributes:

			default, aType, is_input, aMin, aMax, array, keyable, storable, \
				readable, writable, cached, hidden, short_name, attr_name = self.extract_attribute_data( data )

			if is_input is not True:
				if not array:
					result += "\tdata.outputValue({attr_name}).setClean();\n".format( attr_name=attr_name )
				else:
					raise NotImplementedError( "array plugs not implemented for all clean." )

		return (result)

	def generate_cpp_attrib_creation(self, is_input):
		result = ""

		keys = sorted( self.attributes.keys() )
		data = [ self.attributes[x] for x in keys ]

		for name, data in zip( keys, data ):
			if data['is_input'] is is_input:

				## for ease of use I'm extracting everything here
				default, aType, is_input, aMin, aMax, array, keyable, storable, readable, \
					writable, cached, hidden, short_name, attr_name = self.extract_attribute_data( data )

				mfn = 'nAttr'

				if aType == 'float':
					create = '\t{attr_name} = {mfn}.create( "{name}", "{short_name}", MFnNumericData::kFloat, {default} );\n'
					create = create.format(
						attr_name=attr_name,
						mfn=mfn,
						name=name,
						short_name=short_name if short_name else name,
						default=default
					)

					result += create

				elif aType == 'matrix':
					mfn = 'mAttr'
					create = '\t{attr_name} = {mfn}.create( "{name}", "{short_name}" );\n'
					create = create.format(
						attr_name=attr_name,
						mfn=mfn,
						name=name,
						short_name=short_name if short_name else name,
					)

					create += '\t\t{mfn}.setDefault( identity );\n'.format(mfn=mfn)

					result += create

				else:
					raise NotImplementedError( "Plugs of %s type are not yet implemented." % aType )

				

				result += '\t\t{mfn}.setStorable({value});\n'.format( mfn=mfn, value='true' if storable else 'false' )
				result += '\t\t{mfn}.setKeyable({value});\n'.format(  mfn=mfn, value='true' if keyable else 'false' )
				result += '\t\t{mfn}.setReadable({value});\n'.format( mfn=mfn, value='true' if readable else 'false' )
				result += '\t\t{mfn}.setWritable({value});\n'.format( mfn=mfn, value='true' if writable else 'false' )

				if array:
					result += '\t\t{mfn}.setArray( true );\n'.format( mfn=mfn )
					if is_input:
						result += '\t\t{mfn}.setUsesArrayDataBuilder( true );\n'.format( mfn=mfn )

				if aMin is not None:
					result += '\t\t{mfn}.setMin( {min} );\n'.format( mfn=mfn, min=aMin )

				if aMax is not None:
					result += '\t\t{mfn}.setMax( {max} );\n'.format( mfn=mfn, max=aMax )

				if cached is True:
					result += '\t\t{mfn}.setCached( true );\n'.format( mfn=mfn )

				if hidden is True:
					result += '\t\t{mfn}.setHidden( true );\n'.format( mfn=mfn )

				## final check
				result += '\tCHECK_MSTATUS_AND_RETURN_IT( addAttribute({attr_name}) );\n\n'.format( attr_name=attr_name )

		return (result)

	def generate_attribute_creation_affects(self, inputs):
		result = ""

		## shouldn't matter if this is sorted or not
		for name, data in self.attributes.items():
			is_input = data.get('is_input', None)
			if is_input == inputs:
				result += '\t\t{{ "{name}", & {attr_name} }},\n'.format( name=name, attr_name=data['attr_name'] )

		## eat the last comma
		result = result.rpartition(",\n")[0]

		return (result)

	def generate_ae_parameters(self):
		result = ""
		ae_types = { 'float' }

		for name, data in self.attributes.items():
			is_input = data.get('is_input', None)
			if is_input:
				if data['type'] in ae_types:
					result += ('\t' * 5) + 'editorTemplate -addControl "{name}";\n'.format( name=name )

		return(result)

	def generate_class(self):
		"""
		Generates the C++ file for the class with method implementations.
		:return: The string for the C++ class file all constructed.
		"""

		with open( os.sep.join( [os.path.dirname( __file__ ), 'mpxnode_template.cpp'] ), 'r' ) as fp:
			template = fp.read( )

		result = template.format(
			typeID=self.typeID,
			header_name=self.class_name,
			class_name=self.class_name,
			node_name=self.node_name,
			static_input_attributes=self.generate_cpp_static_attributes( inputs=True ),
			static_output_attributes=self.generate_cpp_static_attributes( inputs=False ),
			constants=self.generate_cpp_constants(),
			plug_check=self.generate_cpp_plug_check(),
			input_collection=self.generate_cpp_collect_inputs(),
			output_setting=self.generate_cpp_set_outputs(),
			attribute_creation="attribute_creation", # self.generate_cpp_attrib_creation(),
			attribute_creation_inputs=self.generate_cpp_attrib_creation(True),
			attribute_creation_outputs=self.generate_cpp_attrib_creation(False),
			attribute_creation_affects_inputs=self.generate_attribute_creation_affects(True),
			attribute_creation_affects_outputs=self.generate_attribute_creation_affects(False),
			attribute_editor_parameters=self.generate_ae_parameters(),
			set_all_clean=self.generate_set_all_clean()
		)

		return(result)

	def generate_node_main(self):
		"""
		Generates the C++ file for the actual compute function. This is left
		separate because the class can be regenerated.
		:return: The string for the C++ class file all constructed.
		"""

		with open( os.sep.join( [os.path.dirname( __file__ ), 'mpxnode_template_main.cpp'] ), 'r' ) as fp:
			template = fp.read( )

		result = template.format(
			header_name=self.class_name,
			class_name=self.class_name,
			node_name=self.node_name
		)

		return(result)

## ----------------------------------------------------------------------
if __name__ == "__main__":
	inst = MPxNodeCPP( 'SomaticVIK', 'sm_vik', 0x123456 )

	inst.add_input_plug( 'inputMatrix', None, type='matrix' )
	inst.add_input_plug( 'blender_one', 1.0, min=0.0, max=1.0 )
	inst.add_input_plug( 'blender_two', 0.0, min=0.0, max=1.0 )
	inst.add_output_plug( 'outMatrix', None, type='matrix' )

	print( inst.generate_include() )
	print( inst.generate_class_main() )



