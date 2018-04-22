Nodesmith: C++ Plugin generator for Autodesk Maya
=================================================

Nodesmith takes in a JSON file and spits out node C++ and header 
files, as well as a plugin_main.cpp that loads and registers the 
plugins.

The user can then go in and either hand-edit the node C++ file, or 
can use the node_main.cpp file to add to the ::compute function 
while allowing for the node to be re-generated (add or remove plugs,
for example) after the fact.

I've also added expression support (please see the example).  You can
specify the code to put into the compute for simple nodes directly in
the plugin JSON.  This means that after generation, you have a runnable,
testable suite of nodes for nodes performing simple operations.

Please note that the CMakeLists.txt that is created has only been tested
on Mac.  Windows support is coming.


