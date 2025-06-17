#ifndef POLYCPP_NAMESCPACE
#define POLYCPP_NAMESCPACE

#define namespace(name) typedef struct name##POLYCPP_ns name##POLYCPP_ns; struct name##POLYCPP_ns
#define end_namespace(name) struct name##POLYCPP_ns name={};

//Example usage: you need to also define functions outside namespaces:

/*int Math_add(int a, int b) { return a + b; }

namespace(Math){
    int (*add)(int, int);
};end_namespace(Math)*/

#endif