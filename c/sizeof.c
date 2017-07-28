#include<stdio.h>
#include<string.h>
#include<unistd.h>

char* subStr(char* s, int start, int size){
  if(start < 0 || size < 0 || start + size > strlen(s)){
    return "";
  }else {
    char buffer[size + 1];
    memcpy(buffer, &s[start], size);
    buffer[size] = '\0';
    return buffer;
  }
}

int kmpSearch(char* s, char* child){
  int m, i;
  while(*s != '\0'){
    
    s++;
  }
  return 0;
}

char* longestPalindrome(char* s){
  char *buffer;
  puts(s);
  if(strlen(s) < 2){
    return "";
  }else {
    char *begin = s;
    int maxLen = 0,tempLen = 0;
    char *start, *tempStart;
    while(*s != '\0'){
      if(*s == *(s - 1)){
        tempLen = 2;
        tempStart = s - 1;
        int n = 0;
        while(*(s + n++) != '\0'){
          if(*(s + n) == *(s - n - 1)){
            tempLen++;
            tempStart = s - n - 1;
          }
          if(s - n - 1 == begin) break;
        }
      }else if(begin != s-1 && *s == *(s - 2)){
        tempLen = 3;
        tempStart = s - 2;
        int n = 0;
        while(*(s + n++) != '\0'){
          if(*(s + n) == *(s - n - 2)){
            tempLen++;
            tempStart = s - n - 2;
          }
          if(s - n - 1 == begin) break;
        }
      }
      if(tempLen > maxLen){
        maxLen = tempLen;
        start = tempStart;
      }
      s++;
    }
    printf("%d %d\n", maxLen, (start - begin));
    if(maxLen == 0) return "";
    else {
      return subStr(s, start - begin, maxLen);
    }
  }
}

int main() {
  /* printf("xxx\n"); */
  /* int child = fork(); */
  /* if(child == 0){ */
  /*   printf("this is child process\n"); */
  /*   printf("uid: %d", getuid()); */
  /*   printf("self: %d\n father: %d\n group: %d\n", getpid(), getppid(), getgid()); */
  /* }else { */
  /*   printf("this is father process\n"); */
  /*   printf("uid: %d", getuid()); */
  /*   printf("self: %d\n father: %d\n group: %d\n", getpid(), getppid(), getgid()); */
  /* } */
  printf("%d\n", kmpSearch("ababababcabcabcdefg", "abcd"));
  return 0;
}
