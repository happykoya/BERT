#include <time.h>
#include <rpc/rpc.h>
#include "date.h"
char ** strdate_1_svc(void *arg, struct svc_req *req) {

  static char *result; 
  struct timeval theTime; 
  gettimeofday(&theTime, NULL);

  result = ctime((const time_t *)&theTime.tv_sec);
  return(&result);
}
