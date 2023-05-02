#include <stdio.h>
#include <string.h>
#include <sys/types.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <netdb.h>
#include <pthread.h>
#define PORT 9876 //サーバープログラムとポート番号を合わせてください

int main(){
  // IP アドレス，ソケット，sockaddr_in 構造体
  char destination[32];
  int dstSocket;
  struct sockaddr_in dstAddr;

  //struct sockaddr_in addr;
  struct hostent *hp;
  char   buf[1024];
  int    numrcv;

  // 相手先アドレスの入力と送る文字の入力
  printf("サーバーマシンのIPは？:");
  scanf("%s", destination);
  
  //sockaddr_in 構造体のセット
  bzero((char *)&dstAddr, sizeof(dstAddr));
  dstAddr.sin_family = AF_INET;
  dstAddr.sin_port = htons(PORT);
  
  hp = gethostbyname(destination);
  bcopy(hp->h_addr, &dstAddr.sin_addr, hp->h_length);

  //ソケットの生成
  dstSocket = socket(AF_INET, SOCK_STREAM, 0);
  
  //接続
  if (connect(dstSocket, (struct sockaddr *)&dstAddr, sizeof(dstAddr)) < 0){
    printf("%s に接続できませんでした\n",destination);
    return(-1);
  }
  printf("%s に接続しました\n",destination);
  printf("適当な文字列を入力：");
  
  while (1){
    scanf("%s",buf);
    //パケットの送信
    write(dstSocket, buf, 1024);
    //パケットの受信
    numrcv = read(dstSocket, buf, 1024);
    printf("→ %s\n\n",buf);
  }
  close(dstSocket);
  return(0);
}
