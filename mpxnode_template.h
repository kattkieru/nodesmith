#pragma once

// ----------------------------------------------------------------------

class {class_name} : public MPxNode
{{
public:

	{class_name}();
	virtual	~{class_name}();

	static  void* creator();
	static  MStatus initialize();
	static  void aeTemplate();

	static	MTypeId id;

	virtual MStatus setDependentsDirty( const MPlug &plugBeingDirtied,
		MPlugArray &affectedPlugs );

	virtual MStatus compute( const MPlug& plug, MDataBlock& data );

	virtual SchedulingType schedulingType() const {{ return kParallel }};

	void set_all_clean(void);

	// inputs
{inputs}

	// outputs
{outputs}
}};

