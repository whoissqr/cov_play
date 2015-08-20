#include "Defects.hpp"
#include <iostream>

using namespace std;

int main()
{	
	cout << "my favorite bugs" << endl;

    Defects* myDefects = new Defects();

   	cout << myDefects->copyError(1,2,3,4) <<endl;

	vector<int> vec_1(3,1), vec_2(3,2);
	myDefects->misIter(vec_1,vec_2);

	return 0;
}
