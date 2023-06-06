/*
* 遠隔手続きの宣言
* strdate_1() - 日時を書いた文字列を返す
*/
program DATE_PROG {
	version DATE_VERS {	
		string STRDATE(void) = 1; /* procedure number = 1 */
	} = 1; /* version number = 1 */
} = 0x41320020; /* program number = 0x41320020 */
