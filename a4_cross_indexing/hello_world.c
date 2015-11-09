#include<stdio.h>
int x = 1;
int foo() {
    return 0;
}
int main() {
    int y = 2;
    int z = x + y;
    x = 3;
    foo();
}
