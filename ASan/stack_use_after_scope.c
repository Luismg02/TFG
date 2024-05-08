#include <stdlib.h>

volatile int *p = NULL;

int main() {
  {
    int x = 0;
    p = &x;
  }
  *p = 5;
  return 0;
}
