#include <stdio.h>
#include <string.h>
#include <malloc.h>
#include <sys/types.h>
#include <sys/socket.h>
#include <netinet/in.h>
//並行処理
#include <pthread.h>
#include <time.h>

#define PORT 9876 //クライアントプログラムとポート番号を合わせてください
int i;
int srcSocket; //自分
int dstSocket; //相手
// sockaddr_in 構造体
struct sockaddr_in srcAddr;
struct sockaddr_in dstAddr;
int dstAddrSize = sizeof(dstAddr);
// 各種パラメータ
int status;
int numrcv;
char buf[1024];


int *my_func(void *arg){
  int i,j;
  char tmp;
//パケットの受信
  numrcv = read(dstSocket, buf, 1024);
  if(numrcv ==0 || numrcv ==-1 ){
    close(dstSocket);
    return 1;
  }
  printf("変換前 %s",buf);
  
  for (i=0; i< numrcv; i++){ // bufの中の小文字を大文字に変換
    if(isalpha(buf[i])) buf[i] = toupper(buf[i]);
  }
  for (i = 0, j = strlen(buf) - 1; i < j; i++, j--) {
        tmp = buf[i];
        buf[i] = buf[j];
        buf[j] = tmp;
    }
  // パケットの送信
  write(dstSocket, buf, 1024);
  fprintf(stdout,"→ 変換後 %s \n",buf);

  return NULL;
}

int main(){
  pthread_t pthread;
  clock_t start_clock, end_clock;

   /* 処理開始前後のクロックを取得 */
  start_clock = clock();
  end_clock = clock();


  while(1){//ループで回すことによって何度でもクライアントからつなぐことができる
    // sockaddr_in 構造体のセット
    bzero((char *)&srcAddr, sizeof(srcAddr));
    srcAddr.sin_port = htons(PORT);
    srcAddr.sin_family = AF_INET;
    srcAddr.sin_addr.s_addr = INADDR_ANY;
    
    // ソケットの生成（ストリーム型）
    srcSocket = socket(AF_INET, SOCK_STREAM, 0);
    // ソケットのバインド
    bind(srcSocket, (struct sockaddr *)&srcAddr, sizeof(srcAddr));
    // 接続の許可
    listen(srcSocket, 1);
    
    // 接続の受付け
    printf("接続を待っています\nクライアントプログラムを動かして下さい\n");
    dstSocket = accept(srcSocket, (struct sockaddr *)&dstAddr, &dstAddrSize);
    printf("接続を受けました\n");
    close(srcSocket);

    /* スレッド作成 */
    //pthread_create(&pthread, NULL, my_func, NULL);
    while(1){
      pthread_create(&pthread, NULL, my_func, NULL);

      printf(
      "clock:%f\n", 
      (double)(end_clock - start_clock) / CLOCKS_PER_SEC
      );
      end_clock = clock();
      sleep(1);
      }
      pthread_join(pthread, NULL);
  }
  return(0);
}
