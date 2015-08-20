#include "Defects.hpp"
#include <memory.h>

using namespace std;

//Demo Case 1
int Defects::copyError(int a, int b, int x, int y)
{
    int result = 0;
    if (a > 0)
    {
        result = square(a) + square(x);
    }
    if (b > 0)
    {
        // "square(a)" should read "square(b)"
        result = square(a) + square(y);
    }
    return result;
}

//Demo Case 2
void Defects::misIter(vector<int>& v1, vector<int>& v2)
{
    vector<int>::iterator i = v1.begin();
    // Defect: Uses "i" from "v1" in a method on "v2"
    v2.erase(i);
}

//Demo Case 3
int Defects::forwardNull(int *p) 
{
    int x = 1;
    if ( p == NULL )
    {
        x = 0;
    }
    else
    {
        x = *p;
    }
    *p = x;   // Defect: p is potentially NULL
    return 0;
}

//Demo Case 4
void Defects::memberBoundaries()
{
    struct S
    {
        int x[10];
        int y[20];
    };

    struct S s;
    // reported if 'strict_member_boundaries' is enabled
    memset(&s.x[0], 0, sizeof(int)*30); // access s.x[29]
}
