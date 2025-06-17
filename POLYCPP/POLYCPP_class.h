#ifndef POLYCPP_CLASS
#define POLYCPP_CLASS

#define class(name) typedef struct name name; struct name

#define new(typename) malloc(sizeof(typename))
#define delete(d) free(d)

//Example:
/*
// Base class
class(Animal){
    char name[50];

    void (*introduce)(struct Animal* self);
};

// Animal method
void Animal_introduce(Animal* self) {
    printf("I'm an animal named %s.\n", self->name);
}
*/
#endif