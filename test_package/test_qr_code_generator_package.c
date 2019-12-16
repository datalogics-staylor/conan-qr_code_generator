#include <assert.h>
#include <stdio.h>
#include "qrcodegen.h"

int main(int argc, char **argv) {
  const char *number = "19";
  bool isNumeric = qrcodegen_isNumeric(number);
  printf("%s is numeric: %s\n", number, isNumeric ? "true" : "false");
  assert(isNumeric);
}
