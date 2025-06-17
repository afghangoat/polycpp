#ifndef POLYCPP_ITERATOR
#define POLYCPP_ITERATOR

//Important naming convention: the next linked list nodes should be named "next"
#define ITERATE_LIST(type,iterator, head,end) \
    for (type* iterator = (head); iterator != end; iterator = iterator->next)
/*
Example:
ITERATE_LIST(Node,it, head,NULL) {
    printf("%d\n", it->data);
}
*/

#define ITERATE_ARRAY(type, array, size, iterator) \
    for (type* iterator = (array); iterator < (array) + (size); ++iterator)
/*
Example:
ITERATE_ARRAY(int, arr, size, it) {
    printf("%d\n", *it);
}
*/

#endif