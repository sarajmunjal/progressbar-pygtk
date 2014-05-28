#include <iostream>
#include <cstdio>

using namespace std;

int main(int argc,char **argv)
{
	int i,j;
	cout<<"number 100\n";
	for(i=1;i<=100;i++)
	{
		for(j=1;j<100000000;j++);
		cout<<"frame "<<i<<endl;
	}	
	return 0;
}