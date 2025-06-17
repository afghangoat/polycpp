#PolyCPP

A C library which backports useful features from C++ to C.

##Features

-Namespace
-Classes
-Scopes (::)
-Try catch
-Iterators
-Exceptions
-Auto (Was removed, because it introduced too much complexity)

##Usage

Place all header files in your project and whenever you need to use it, include "POLYCPP.h" in you project.

You need to run the `POLYCPP_transpiler.py` if you want:
-templates
-::-s
-namespaces
-classes