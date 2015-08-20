#include <vector>
using namespace std;

class Defects
{
    public:
        //Case 1: COPY_PASTE_ERROR
        int copyError(int a, int b, int x, int y);

        //Case 2: MISMATCHED_ITERATOR
        void misIter(vector<int>& v1, vector<int>& v2);

        //Case 3: FORWARD_NULL
        int forwardNull(int *p);

        //Case 4: OVERRUN
        void memberBoundaries();

    private:
        int square(int x){return x*x;};
};