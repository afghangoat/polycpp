#ifndef POLYCPP_TRYCATCH
#define POLYCPP_TRYCATCH

#include <setjmp.h>
#include "POLYCPP_exception.h"

#define try if (!setjmp(ex_buf__))
#define catch(x) else if (current_exception == x)
#define finally else
#define throw(x) do { current_exception = x; longjmp(ex_buf__, 1); } while (0)

jmp_buf ex_buf__;
ExceptionType current_exception = no_error;

/*Example:
	try {
        printf("Inside TRY block\n");
        throw(error_divide_by_zero);
    }
    catch(error_null_pointer) {
        printf("Caught NULL POINTER exception!\n");
    }
    catch(error_divide_by_zero) {
        printf("Caught DIVIDE BY ZERO exception!\n");
    }
    finally {
        printf("Finally block executes\n");
    }
*/
#endif