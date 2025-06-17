#ifndef POLYCPP_EXCEPTION
#define POLYCPP_EXCEPTION

typedef enum {
    no_error = 0,
    error_null_pointer,
    error_divide_by_zero
} ExceptionType;

#endif