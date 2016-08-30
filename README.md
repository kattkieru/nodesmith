Nodesmith: C++ Plugin generator for Autodesk Maya

Nodesmith takes in a JSON file and spits out node C++ and header files, as well as a
plugin_main.cpp that loads and registers the plugins.

The user can then go in and either hand-edit the node C++ file, or can use the
node_main.cpp file to add to the ::compute function while allowing for the node to
be re-generated (add or remove plugs, for example) after the fact.

This is proof of concept. It should not be used in production yet, and the CMakeLists.txt
that is generated may not yet work.
