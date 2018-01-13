
#include "common.h"
{node_header_includes}
#include <maya/MFnPlugin.h>

// ----------------------------------------------------------------------
PLUGIN_EXPORT MStatus initializePlugin( MObject obj )
{{
	MStatus stat;
	MFnPlugin plugin( obj, "{author}", "{version}", "Any");

{plugin_registration}
	return stat;
}}


// ----------------------------------------------------------------------
PLUGIN_EXPORT MStatus uninitializePlugin( MObject obj)
{{
	MStatus stat;
	MFnPlugin plugin(obj);

{plugin_deregistration}
	return stat;
}}

