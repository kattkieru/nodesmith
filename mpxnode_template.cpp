
// ----------------------------------------------------------------------

#include "common.h"
#include "{header_name}.h"

// ----------------------------------------------------------------------

MTypeId {class_name}::id( {typeID} );

// static attribute memory allocation
{static_input_attributes}
{static_output_attributes}

const struct {{
	MMatrix identity {{}};
{constants}
}} SS {{}}; // need to force the initializer in gcc

// ----------------------------------------------------------------------
/*
	class method implementations
*/
// ----------------------------------------------------------------------

{class_name}::{class_name}()
{{
}}

{class_name}::~{class_name}()
{{
}}

// ----------------------------------------------------------------------
MStatus {class_name}::setDependentsDirty( const MPlug &plugBeingDirtied, MPlugArray &affectedPlugs )
{{
	/*
	// example usage
	MObject mob = plugBeingDirtied.attribute();
	if (mob == iOutputCount)
		should_resize_ = true;

	return(MStatus::kSuccess);
	*/
}}

// ----------------------------------------------------------------------
MStatus {class_name}::compute( const MPlug& plug, MDataBlock& data )
{{
	MStatus stat;
	MObject node = thisMObject();

	bool plug_check {{
{plug_check}    }};

	if( plug_check ) {{
		// collect all inputs
{input_collection}

		// call external compute function
		{class_name}__main();

		// set all outputs
{output_setting}

		set_all_clean();
		return MS::kSuccess;
	}}

	return MS::kUnknownParameter;
}}


// ----------------------------------------------------------------------
void* {class_name}::creator()
{{
	return new {class_name}();
}}


// ----------------------------------------------------------------------
MStatus {class_name}::initialize()
{{
	MStatus stat;
	char msg[1024];

// attribute function classes
{attribute_creation}

	MFnEnumAttribute     eAttr;
	MFnUnitAttribute     uAttr;
	MFnTypedAttribute    tAttr;
	MFnNumericAttribute  nAttr;
	MFnMatrixAttribute   mAttr;
	MRampAttribute       rAttr;
	MFnCompoundAttribute cAttr;

// input plugs
{attribute_creation_inputs}

// output plugs
{attribute_creation_outputs}

	// attributeAffects maps
	std::map<std::string, MObject *> all_inputs = {{
{attribute_creation_affects_inputs}
	}};

	std::map<std::string, MObject *> all_outputs = {{
{attribute_creation_affects_outputs}
	}};

	for (const auto &input_pair : all_inputs) {{
		for (const auto &output_pair : all_outputs) {{
			stat = attributeAffects(*input_pair.second, *output_pair.second);
			if (!stat) {{
				sprintf(msg, "attributeAffects: %s >> %s",
						(const char *)input_pair.first.c_str(),
						(const char *)output_pair.first.c_str());
				stat.perror(msg); 
				return stat;
			}}
		}}
	}}

	return MS::kSuccess;
}}

// ----------------------------------------------------------------------
void {class_name}::aeTemplate() {{
	const char *msg = R"(
		global proc AEsm_spineTemplate(string $nodeName) {{
			// AEswatchDisplay $nodeName;
			editorTemplate -beginScrollLayout;

				editorTemplate -beginLayout "Setup" -collapse 0;
					editorTemplate -addControl "curveFunction";
					editorTemplate -addControl "samples";
					editorTemplate -addControl "alpha";
					editorTemplate -addControl "inputCount";
					editorTemplate -addControl "outputCount";
					editorTemplate -addControl "restLength";

				editorTemplate -endLayout;

				// editorTemplate -beginLayout "Positioning" -collapse 0;
				// 	editorTemplate -addControl "compress";
				// 	editorTemplate -addControl "slide";
				// 	editorTemplate -addControl "stacking";
				// editorTemplate -endLayout;

				editorTemplate -beginLayout "Squash and Stretch" -collapse 0;
					editorTemplate -addControl "stretchBlend";
					editorTemplate -addControl "squetchMax";
					// editorTemplate -addControl "scaleClamp";
					// AEaddRampControl($nodeName + ".parametricScale");
					// AEaddRampControl($nodeName + ".lengthScale");
				editorTemplate -endLayout;

				// AEaddRampControl($nodeName + ".squetchShape");

				editorTemplate -beginLayout "Outputs" -collapse 0;
					editorTemplate -addControl "curveLength";
				editorTemplate -endLayout;

				// editorTemplate -endLayout;

				// AEdependNodeTemplate $nodeName;
				editorTemplate -addExtraControls -collapse 1;

			editorTemplate -endScrollLayout;
		}}
	)";

	MGlobal::executeCommand(msg);
}}

