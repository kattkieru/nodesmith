
#ifndef __COMMON_H
#define __COMMON_H
// ----------------------------------------------------------------------

#ifndef _CRT_SECURE_NO_WARNINGS
	// this stops Visual Studio from issuing the 
	// "blah blah is not secure" warnings
	#define _CRT_SECURE_NO_WARNINGS
#endif

#define _USE_MATH_DEFINES

#include <math.h>
#include <stdio.h>
#include <stdint.h>

#include <algorithm>
#include <cmath>
#include <cstdarg>
#include <iostream>
#include <map>
#include <numeric>
#include <set>
#include <string>
#include <vector>

#include <maya/MFnData.h>
#include <maya/MGlobal.h>
#include <maya/MPxNode.h>

#include <maya/MAngle.h>
#include <maya/MEulerRotation.h>
#include <maya/MFloatVector.h>
#include <maya/MFloatMatrix.h>
#include <maya/MMatrix.h>
#include <maya/MPoint.h>
#include <maya/MPointArray.h>
#include <maya/MQuaternion.h>
#include <maya/MString.h>
#include <maya/MTypeId.h>
#include <maya/MVector.h>
#include <maya/MVectorArray.h>

#include <maya/MArrayDataBuilder.h>
#include <maya/MArrayDataHandle.h>
#include <maya/MDataBlock.h>
#include <maya/MDataHandle.h>

#include <maya/MFnCompoundAttribute.h>
#include <maya/MFnEnumAttribute.h>
#include <maya/MFnUnitAttribute.h>
#include <maya/MFnMatrixAttribute.h>
#include <maya/MFnMatrixData.h>
#include <maya/MFnNumericAttribute.h>
#include <maya/MFnNumericData.h>
#include <maya/MFnNurbsSurfaceData.h>
#include <maya/MRampAttribute.h>
#include <maya/MFnTypedAttribute.h>

#include <maya/MFnNurbsSurface.h>

#include <maya/MThreadUtils.h>

#define PLG_AUTHOR  "{author}"
#define PLG_VERSION "{version}"

#define OUT

#define DEG2RAD(degrees)      (degrees * M_PI ) / 180
#define RAD2DEG(radians)      (radians * 180) / M_PI
#define LERP(a,b,t)           (a + (b-a) * t)

{constants}

#endif

