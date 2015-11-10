#include<stdio.h>

int g = 1;

int add() {
  return 1 + 1;
}

int main() {
   int n;
   int first = 0;
   int second = 1;
   int next;
   int c;

   add();
   printf("Enter the number of terms\n");
   scanf("%d",&n);
 
   printf("First %d terms of Fibonacci series are :-\n",n);
 
   for ( c = 0 ; c < n ; c++ )
   {
      int x = 7;
      if ( c <= 1 )
         next = c;
      else
      {
         next = first + second;
         first = second;
         second = next;
      }
      printf("%d\n",next);
   }
 
   return 0;
}
