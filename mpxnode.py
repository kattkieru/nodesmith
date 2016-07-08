
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
		self.typeID = '0x%6x' % typeID    ## converts to hex
		self.attributes = {}

	def add_plug( self, plug, default, is_input, type='float', min=None, max=None, 
					array=False, keyable=True, storable=True, readable=True, 
					writable=True, cached=False, hidden=False, short_name=None ):
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
					keyable=True, storable=True, cached=False,
					hidden=False, short_name=None ):

		return( self.add_plug(plug, default, True, type=type, min=min, max=max, array=array,
				keyable=keyable, storable=storable, readable=False, writable=True, 
				cached=cached, hidden=hidden, short_name=short_name ) )

	def add_output_plug( self, plug, default, type='float', min=None, max=None, array=False,
						keyable=True, storable=True, cached=False,
						hidden=False, short_name=None ):

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

	def generate_include(self):
		"""
		Generates the C++ header file for the class.
		:return: The string for the header file all constructed.
		"""

		with open( os.sep.join( [os.path.dirname( __file__ ), 'mpxnode_template.h'] ), 'r' ) as fp:
			template = fp.read( )

		## I was using .format but then it's harder to edit the templates
		## because you have to keep track more. So I'm replacing directly.
		# result = template.replace( '{class_name}', self.class_name )
		# result = result.replace( '{inputs}', self.generate_header_attributes( inputs=True ) )
		# result = result.replace( '{outputs}', self.generate_header_attributes( inputs=False ) )

		result = template.format(
			class_name=self.class_name,
			inputs=self.generate_header_attributes( inputs=True ),
			outputs=self.generate_header_attributes( inputs=False )
		)

		return( result )

	def generate_cpp_plug_check(self, inputs=False):
		result = None

		for name, data in self.attributes.items():
			if data['is_input'] is inputs:
				if result is None:
					result = "\t   "
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
		keyable    = data.get('keyable', None)
		storable   = data.get('storable', None)
		readable   = data.get('readable', None)
		writable   = data.get('writable', None)
		cached     = data.get('cached', None)
		hidden     = data.get('hidden', None)
		short_name = data.get('short_name', None)
		attr_name  = data.get('attr_name', None)

		return( default, aType, is_input, aMin, aMax, array, keyable, storable,
				readable, writable, cached, hidden, short_name, attr_name )

	def generate_cpp_input_collection(self):
		result = ""
		return (result)

	def generate_cpp_output_setting(self):
		result = ""
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

	def generate_attribute_creation_affects_inputs(self):
		result = ""
		return (result)

	def generate_attribute_creation_affects_outputs(self):
		result = ""
		return (result)

	def generate_class_main(self):
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
			static_input_attributes=self.generate_cpp_static_attributes( inputs=True ),
			static_output_attributes=self.generate_cpp_static_attributes( inputs=False ),
			constants=self.generate_cpp_constants(),
			plug_check=self.generate_cpp_plug_check(),
			input_collection=self.generate_cpp_input_collection(),
			output_setting=self.generate_cpp_output_setting(),
			attribute_creation="attribute_creation", # self.generate_cpp_attrib_creation(),
			attribute_creation_inputs=self.generate_cpp_attrib_creation(True),
			attribute_creation_outputs=self.generate_cpp_attrib_creation(False),
			attribute_creation_affects_inputs=self.generate_attribute_creation_affects_inputs(),
			attribute_creation_affects_outputs=self.generate_attribute_creation_affects_outputs()
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



