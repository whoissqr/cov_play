#include <iostream>
#include <vector>

using namespace std;

int square(int x)
{
	return x*x;
}

int example(int a, int b, int x, int y)
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

void test(vector<int> &v1, vector<int> &v2)
{
	vector<int>::iterator i = v1.begin();
	// Defect: Uses "i" from "v1" in a method on "v2"
	v2.erase(i);
}

int main()
{	
	cout << "my favorite bugs" << endl;

    	cout << example(1,2,3,4) <<endl;

	vector<int> vec_1(3,1), vec_2(3,2);
	test(vec_1,vec_2);	

	return 0;
	
}
