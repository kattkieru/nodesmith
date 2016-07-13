#pragma once

// ----------------------------------------------------------------------

class {class_name} : public MPxNode
{{
private:
{private_variables}
public:

	{class_name}();
	virtual	~{class_name}();

	static  void* creator();
	static  MStatus initialize();
	static  void aeTemplate();

	static  MTypeId id;

	virtual MStatus setDependentsDirty( const MPlug &plugBeingDirtied,
		MPlugArray &affectedPlugs );

	virtual MStatus compute( const MPlug& plug, MDataBlock& data );

	virtual SchedulingType schedulingType() const {{ return kParallel }};

	inline void set_all_clean(void);

	// this is the real compute function
	inline void node_main(void);

	// inputs
{inputs}
	// outputs
{outputs}
}};

