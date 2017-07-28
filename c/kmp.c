#include <stdio.h>
#include <stdlib.h>
#include <string.h>

void printArray(int* p, int psize){
  int i = 0;
  for(; i < psize; i++){
    printf("%d ", *(p+i));
  }
  printf("\n");
}

int *compute_prefix_function(char *pattern, int psize)
{
	int k = -1;
	int i = 1;
	int *pi = malloc(sizeof(int)*psize);
	if (!pi)
		return NULL;

	pi[0] = k;
	for (i = 1; i < psize; i++) {
		while (k > -1 && pattern[k+1] != pattern[i])
			k = pi[k];
		if (pattern[i] == pattern[k+1])
			k++;
		pi[i] = k;
	}
  printArray(pi, psize);
	return pi;
}

int kmp(char *target, int tsize, char *pattern, int psize)
{
	int i;
	int *pi = compute_prefix_function(pattern, psize);
	int k = -1;
	if (!pi)
		return -1;
	for (i = 0; i < tsize; i++) {
		while (k > -1 && pattern[k+1] != target[i])
			k = pi[k];
		if (target[i] == pattern[k+1])
			k++;
		if (k == psize - 1) {
			free(pi);
			return i-k;
		}
	}
	free(pi);
	return -1;
}

int fibonacci(int n){
  int i = 2;
  int result = 0;
  int prev = 0;
  int forw = 1;
  if(n <= 2){
    return n;
  }
  printf("%d %d ", prev, forw);
  while(i < n){
    result = prev + forw;
    prev = forw;
    forw = result;
    i++;
    printf("%d ", result);
  }
  printf("\n");
  return result;
}

int fibonacci2(int n){
  if(n == 1 || n == 2){
    return n - 1;
  }else {
    return fibonacci2(n - 1) + fibonacci2(n - 2);
  }
}

int main(int argc, const char *argv[])
{
	/* char target[] = "ABC ABCDAB ABCDABCDABDE"; */
	/* char *ch = target; */
	/* char pattern[] = "ABCDABCD"; */
	/* int i; */

	/* i = kmp(target, strlen(target), pattern, strlen(pattern)); */
	/* if (i >= 0) */
	/* 	printf("matched @: %s\n", ch + i); */
  printf("%d ", fibonacci(60));
  printf("%d ", fibonacci2(60));
	return 0;
}
