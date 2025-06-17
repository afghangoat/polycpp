#include "POLYCPP.h"

//Run the POLYCPP_transpiler.py on this to see that it works.
int Math_add(int a, int b) { return a + b; }

namespace(Math){
    int (*add)(int, int);
};end_namespace(Math)

template<typename POLY_T,typename POLY_U>
POLY_T add(POLY_T x1, POLY_U x2){
	return x1+x2;
}
end_template

int main() {
    Math.add=Math_add;

    printf("Example for namespace:\n");
    printf("%d",Math::add(1,2));

    return 0;
}