#include <stdlib.h>
#include <stdio.h>
#include <time.h>
#include <conio.h>s
#include <GL/glut.h>
#include <Windows.h>
#pragma comment (lib, "winmm.lib")

#define STB_IMAGE_IMPLEMENTATION
#include "stb_image.h"

//#define	imageWidth 1024
//#define	imageHeight 1024

//unsigned char texImage[imageHeight][imageWidth][4];
//unsigned char texImage2[imageHeight][imageWidth][4];

char bgmfilename[] = "sound.wav";

int numRectangles = 30;
float positionsX[30];
float posX = -0.90f;
float posX_s = 0.0f;

int pos_return = 0;
int i = -1;

float mouseX = 0.0f; // マウスのX座標
float mouseY = -0.2f; // マウスのY座標

static int time_cnt = 1;
int move_cnt = 0;
static int flag = 0;
static int attack_flag = 0;
static int sans_attack = 0;
static int char_attack = 0;
static int char_act = 0;
static int char_act2 = 0;

static int avoidance = 0;

char str1[] = "char   ";
char str2[] = "LV  3         ";
char str3[] = "HP ";
char space[] = "               ";
int hp = 28;
char hp_int[40];
char* p;
char str4[100];

GLuint textureID1, textureID2;
GLuint textureID3, textureID4, textureID5, textureID6;

static void msleep(unsigned int milliseconds) {
	Sleep(milliseconds);
}

GLuint loadTexture(const char* filename) {
	GLuint textureID;
	glGenTextures(1, &textureID);  // テクスチャIDを生成

	int width, height, channels;
	unsigned char* image = stbi_load(filename, &width, &height, &channels, 0);  // 画像を読み込む

	GLenum format_image;
	if (channels == 3)
		format_image = GL_RGB;
	else if (channels == 4)
		format_image = GL_RGBA;

	glBindTexture(GL_TEXTURE_2D, textureID);  // テクスチャをバインド
	glTexImage2D(GL_TEXTURE_2D, 0, format_image, width, height, 0, format_image, GL_UNSIGNED_BYTE, image);  // テクスチャをOpenGLにアップロード
	glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR);  // テクスチャの拡大/縮小方法を指定
	glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR);
	glBindTexture(GL_TEXTURE_2D, 0);  // テクスチャをアンバインド

	stbi_image_free(image);  // メモリを解放

	return textureID;
}

void loadTextures() {
	textureID1 = loadTexture("Sans2.jpg");  // テクスチャ1を読み込み

	textureID2 = loadTexture("Fight.png");  // テクスチャ2を読み込み
	textureID3 = loadTexture("Act2.png");
	  
	textureID4 = loadTexture("Item.png");  // テクスチャ3を読み込み
	textureID5 = loadTexture("Mercy.png");  // テクスチャ4を読み込み

	textureID6 = loadTexture("Attack.png");
}

void drawObjects() {
	glEnable(GL_TEXTURE_2D);
	if (avoidance == 0) {
		// テクスチャ1をバインドしてオブジェクトを描画
		glBindTexture(GL_TEXTURE_2D, textureID1);
		glBegin(GL_QUADS);
		glTexCoord2f(0.0f, 0.0f); glVertex2f(-0.20f, 0.05f);
		glTexCoord2f(1.0f, 0.0f); glVertex2f(0.20f, 0.05f);
		glTexCoord2f(1.0f, 1.0f); glVertex2f(0.20f, 0.45f);
		glTexCoord2f(0.0f, 1.0f); glVertex2f(-0.20f, 0.45f);
		glEnd();
	}
	
	// テクスチャ2をバインドしてオブジェクトを描画
	glBindTexture(GL_TEXTURE_2D, textureID2);
	glBegin(GL_QUADS);
	glTexCoord2f(0.0f, 0.0f); glVertex2f(-0.90f, -0.70f);
	glTexCoord2f(1.0f, 0.0f); glVertex2f(-0.54f, -0.70f);
	glTexCoord2f(1.0f, 1.0f); glVertex2f(-0.54f, -0.58f);
	glTexCoord2f(0.0f, 1.0f); glVertex2f(-0.90f, -0.58f);
	glEnd();

	// テクスチャ3をバインドしてオブジェクトを描画
	glBindTexture(GL_TEXTURE_2D, textureID3);
	glBegin(GL_QUADS);
	glTexCoord2f(0.0f, 0.0f); glVertex2f(-0.43f, -0.70f);
	glTexCoord2f(1.0f, 0.0f); glVertex2f(-0.07f, -0.70f);
	glTexCoord2f(1.0f, 1.0f); glVertex2f(-0.07f, -0.58f);
	glTexCoord2f(0.0f, 1.0f); glVertex2f(-0.43f, -0.58f);
	glEnd();

	glBindTexture(GL_TEXTURE_2D, textureID4);
	glBegin(GL_QUADS);
	glTexCoord2f(0.0f, 0.0f); glVertex2f(0.07f, -0.70f);
	glTexCoord2f(1.0f, 0.0f); glVertex2f(0.43f, -0.70f);
	glTexCoord2f(1.0f, 1.0f); glVertex2f(0.43f, -0.58f);
	glTexCoord2f(0.0f, 1.0f); glVertex2f(0.07f, -0.58f);
	glEnd();

	glBindTexture(GL_TEXTURE_2D, textureID5);
	glBegin(GL_QUADS);
	glTexCoord2f(0.0f, 0.0f); glVertex2f(0.54f, -0.70f);
	glTexCoord2f(1.0f, 0.0f); glVertex2f(0.90f, -0.70f);
	glTexCoord2f(1.0f, 1.0f); glVertex2f(0.90f, -0.58f);
	glTexCoord2f(0.0f, 1.0f); glVertex2f(0.54f, -0.58f);
	glEnd();

	glDisable(GL_TEXTURE_2D);
}

void updateMouse(int x, int y) {

	// ウィンドウ座標を正規化デバイス座標に変換
	mouseX = (float)x / glutGet(GLUT_WINDOW_WIDTH) * 2 - 1;
	mouseY = (float)y / glutGet(GLUT_WINDOW_HEIGHT) * -2 + 1;

	if (mouseX >= 0.2){
		mouseX = 0.19f;
	}

	if (mouseX <= -0.2) {
		mouseX = -0.19f;
	}

	if (mouseY >= 0.0) {
		mouseY = -0.01f;
	}

	if (mouseY <= -0.4) {
		mouseY = -0.39f;
	}

	glutPostRedisplay(); // 再描画を要求
}

void middle_text() {
	char text1[50] = "* You  feel  like  you' re  going  to";
	char text2[50] = "   have  a  bad  time.";

	char text3[40] = "* Keep up the attack.";

	char text4[30] = "* It should hit eventually.";
	char text5[30] = "   Keep up the attack.";
	glColor3f(1.0, 1.0, 1.0);
	glBegin(GL_LINE_LOOP);					// middle_text
	glVertex2d(0.9, 0.0);
	glVertex2d(0.9, -0.4);
	glVertex2d(-0.9, -0.4);
	glVertex2d(-0.9, 0.0);
	glEnd();

	glColor3f(1.0f, 1.0f, 1.0f); // 

	glRasterPos2f(-0.8f, -0.10f);
	for (int i = 0; i < strlen(text1); i++) {
		glutBitmapCharacter(GLUT_BITMAP_TIMES_ROMAN_24, text1[i]);
	}
	glRasterPos2f(-0.8f, -0.25f);
	for (int i = 0; i < strlen(text2); i++) {
		glutBitmapCharacter(GLUT_BITMAP_TIMES_ROMAN_24, text2[i]);
	}
}

void SansAttack()
{
	time_cnt++;
	//glPointSize(100.0f);
	glColor3d(1.0, 0.0, 0.0);
	double x = 0.0;
	double y = -0.3;
	
	if (attack_flag == 0) {
		glPointSize(10.0);
		glEnable(GL_POINT_SMOOTH);
		glBegin(GL_POINTS); // 点の描画を開始
			glVertex2d(mouseX, mouseY); // 点の座標を指定
		glEnd();
	}
	else {
		glPointSize(10.0);
		glEnable(GL_POINT_SMOOTH);
		glBegin(GL_POINTS); // 点の描画を開始
			glVertex2d(x, y); // 点の座標を指定
		glEnd();
	}
	//y += -0.02;

	glColor3d(1.0, 1.0, 1.0);
	glBegin(GL_LINE_LOOP);					// heart_range
		glVertex2d(0.2, 0.0);
		glVertex2d(0.2, -0.4);
		glVertex2d(-0.2, -0.4);
		glVertex2d(-0.2, 0.0);
	glEnd();
	
	attack_flag=1;   //on_attack
	/*
	for (int i = 0; i < numRectangles; i++) {
		//glLoadIdentity();
		if ((positionsX[i] <= -0.2) || (positionsX[i] >= 0.2)) {
			glColor3d(0.0, 0.0, 0.0);
		}
		else {
			glColor3d(1.0, 1.0, 1.0);
		}
		glPushMatrix();
			glTranslatef(positionsX[i], 0.0f, 0.0f);

		glBegin(GL_QUADS);
			glVertex2f(-0.02f, -0.2f);
			glVertex2f(-0.04f, -0.2f);
			glVertex2f(-0.04f, -0.4f);
			glVertex2f(-0.02f, -0.4f);
		glEnd();
		glPopMatrix();
	}
	*/
	//bone_attack
	if (time_cnt <= 30) {
		for (int i = 0; i < numRectangles; i++) {
			positionsX[i] = -0.5 + 0.05f * i;
		}
	}
	/*
	//increase_x-axis
	else{
		for (int i = 0; i < numRectangles; i++) {
			positionsX[i] += 0.001f;
		}
	}

	for (int i = 0; i < numRectangles; i++) {
		//glLoadIdentity();
		if ((positionsX[i] <= -0.2) || (positionsX[i] >= 0.2)) {
			glColor3d(0.0, 0.0, 0.0);
		}
		else {
			glColor3d(1.0, 1.0, 1.0);
		}
		glPushMatrix();
			glTranslatef(positionsX[i], 0.0f, 0.0f); 

			glBegin(GL_QUADS);
				glVertex2f(-0.02f, -0.2f);
				glVertex2f(-0.04f, -0.2f);
				glVertex2f(-0.04f, -0.4f);
				glVertex2f(-0.02f, -0.4f);
			glEnd();
		glPopMatrix();
	}
		glColor3d(1.0, 1.0, 1.0);
	*/
	
}

void CharAttack() {

	glColor3f(1.0, 1.0, 1.0);
	
	glPushMatrix();
	glTranslatef(posX, 0.0f, 0.0f);
	glBegin(GL_QUADS);
	glVertex2f(0.0f, -0.4f);
	glVertex2f(0.05f, -0.4f);
	glVertex2f(0.05f, 0.0f);
	glVertex2f(0.0f, 0.0f);
	glEnd();
	glPopMatrix();

	glEnable(GL_TEXTURE_2D);

	glBindTexture(GL_TEXTURE_2D, textureID6);
	glBegin(GL_QUADS);
	glTexCoord2f(0.0f, 0.0f); glVertex2f(-0.90f, -0.40f);
	glTexCoord2f(1.0f, 0.0f); glVertex2f(0.90f, -0.40f);
	glTexCoord2f(1.0f, 1.0f); glVertex2f(0.90f, 0.00f);
	glTexCoord2f(0.0f, 1.0f); glVertex2f(-0.90f, 0.00f);
	glEnd();

	glDisable(GL_TEXTURE_2D);
}

void Char_Act(){
	char text1[50] = "* Sans";

	char text2[40] = "* SANS  1 ATK  1 DEF";
	char text3[30] = "* The easiest enemy.";
	char text4[30] = "* Can only deal 1 damage.";

	glColor3f(1.0, 1.0, 1.0);
	glBegin(GL_LINE_LOOP);					// middle_text
	glVertex2d(0.9, 0.0);
	glVertex2d(0.9, -0.4);
	glVertex2d(-0.9, -0.4);
	glVertex2d(-0.9, 0.0);
	glEnd();

	glColor3f(1.0f, 1.0f, 1.0f); // 

	if ((char_act2 == 0) &&(sans_attack == 0)){
		glRasterPos2f(-0.8f, -0.10f);
		for (int i = 0; i < strlen(text1); i++) {
			glutBitmapCharacter(GLUT_BITMAP_TIMES_ROMAN_24, text1[i]);
		}
	}
	else {
		glRasterPos2f(-0.8f, -0.10f);
		for (int i = 0; i < strlen(text2); i++) {
			glutBitmapCharacter(GLUT_BITMAP_TIMES_ROMAN_24, text2[i]);
		}

		glRasterPos2f(-0.8f, -0.20f);
		for (int i = 0; i < strlen(text3); i++) {
			glutBitmapCharacter(GLUT_BITMAP_TIMES_ROMAN_24, text3[i]);
		}

		glRasterPos2f(-0.8f, -0.30f);
		for (int i = 0; i < strlen(text4); i++) {
			glutBitmapCharacter(GLUT_BITMAP_TIMES_ROMAN_24, text4[i]);
		}
	}
	


}

void Sans_avoidance() {


	move_cnt++;
	if ((move_cnt >= 20) && (move_cnt <= 40)){
		i = 1;
	}
	else if (move_cnt >= 40) {
		avoidance = 0;
		return 0;
	}
	posX_s += i * 0.01f;
	glColor3d(1.0, 1.0, 1.0);
	glEnable(GL_TEXTURE_2D);
	// テクスチャ1をバインドしてオブジェクトを描画
	
	
	glPushMatrix();
	msleep(10);
		glTranslatef(posX_s, 0.0f, 0.0f);
		glBindTexture(GL_TEXTURE_2D, textureID1);
		glBegin(GL_QUADS);
		glTexCoord2f(0.0f, 0.0f); glVertex2f(-0.20f, 0.05f);
		glTexCoord2f(1.0f, 0.0f); glVertex2f(0.20f, 0.05f);
		glTexCoord2f(1.0f, 1.0f); glVertex2f(0.20f, 0.45f);
		glTexCoord2f(0.0f, 1.0f); glVertex2f(-0.20f, 0.45f);
		glEnd();
	glPopMatrix();
	
	glDisable(GL_TEXTURE_2D);
}

void myKeyboard(unsigned char key, int x, int y)
{
	textureID2 = loadTexture("Fight.png");
	textureID3 = loadTexture("Act2.png");
	textureID4 = loadTexture("Item.png");
	textureID5 = loadTexture("Mercy.png");
	switch (key){
	case '1':
		flag = 1;
		textureID2 = loadTexture("Fight2.png");
		break;

	case '2':
		flag = 2;
		textureID3 = loadTexture("Act3.png");
		break;
	
	case '3':
		flag = 3;
		textureID4 = loadTexture("Item2.png");
		break;

	case '4':
		flag = 4;
		textureID5 = loadTexture("Mercy2.png");
		break;

	case 27:
		exit(0);
		break;

	default:
		break;
	}
	
	if (key == 13){
		if (flag == 1) {
			char_attack = 1;
		}
		else if (flag == 2) {
			char_act = 1;
		}
	}
	else if (key == 32) {
		if (char_attack == 1) {
			avoidance =  1;
		}
		else if (char_act == 1) {
			char_act2 = 1;
		}
		if (char_act2 == 1) {
			sans_attack = 1;
		}
	}

}

void myDisplay()
{
	char text1[40] = "* You  feel  like  you' re  going  to";
	char text2[30] = "   have  a  bad  time.";
	double	p0[] = { 0.25, 0.9 }, p1[] = { -0.25, 0.9 },
		p2[] = { -0.25, 0.05 }, p3[] = { -0.25, 0.05 };


	//glClear(GL_COLOR_BUFFER_BIT);
	glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT);
	//glColor3d(1.0, 1.0, 1.0);			// red
	//glPolygonMode(GL_BACK, GL_LINE);	// draw line  if back
	//glPolygonMode(GL_FRONT, GL_FILL);
	
	
	//glPolygonMode(GL_BACK, GL_LINE);
	
	
	glColor3d(1.0, 1.0, 0.0);      //hp_yellow
	glBegin(GL_QUADS);
	glVertex2d(-0.20, -0.45);
	glVertex2d(0.0, -0.45);
	glVertex2d(0.0, -0.51);
	glVertex2d(-0.20, -0.51);
	glEnd();


	glColor3d(1.0, 0.0, 0.0);       //hp_red
	glBegin(GL_QUADS);
	glVertex2d(-0.25, -0.45);
	glVertex2d(0.0, -0.45);
	glVertex2d(0.0, -0.51);
	glVertex2d(-0.25, -0.51);
	glEnd();

	//glTranslated(0.1, 0.03, 0);

	if ((char_attack == 0)&&(sans_attack == 0)&&(char_act == 0)) {
		middle_text();
		posX = -0.90f;
	}
	else if (char_attack == 1) {
		posX += 0.01f;
		if ((posX >= 0.90)||(avoidance == 1)){
			char_attack = 0;
		}
		else {
			CharAttack();
		}
		
	}
	if (avoidance == 1) {
		Sans_avoidance();
		sans_attack = 1;
	}

	else if(char_act == 1){
		Char_Act();
	}

	
	glColor3f(1.0f, 1.0f, 1.0f);
	glRasterPos2f(-0.9f, -0.50f);

	strcpy_s(str4, sizeof(str4), str1); // str
	strcat_s(str4, sizeof(str4), str2); // str
	strcat_s(str4, sizeof(str4), str3);

	for (int i = 0; i < strlen(str4); i++) {
		glutBitmapCharacter(GLUT_BITMAP_TIMES_ROMAN_24, str4[i]); //	
	}

	//glRasterPos3d(1.0, 1.0, 0.0);

	sprintf_s(hp_int, 40, "                   %4d/28", hp);
	for (p = hp_int; *p; p++) {
		glutBitmapCharacter(GLUT_BITMAP_TIMES_ROMAN_24, *p);
	}

	if (sans_attack == 1) {
		SansAttack();
		//sans_attack = 0;
	}
	drawObjects();
	
	

	//glFlush();
	glutSwapBuffers();
	//glDisable(GL_TEXTURE_2D);
}

void myReshape(int width, int height)
{
	glViewport(0, 0, width, height);
	glMatrixMode(GL_PROJECTION);
	glLoadIdentity();
	gluPerspective(23.0, (double)width / (double)height, 0.1, 20.0);
	//gluPerspective(60.0, (double)width / (double)height, 0.1, 20.0);
	glMatrixMode(GL_MODELVIEW);
	glLoadIdentity();
	glTranslated(0.0, 0.0, -3.6);
}

void myInit(char* progname)
{
	glutInitDisplayMode(GLUT_SINGLE | GLUT_RGBA | GLUT_DEPTH);
	glutInitWindowSize(700, 500);
	glutInitWindowPosition(0, 0);
	glutCreateWindow(progname);
	glClearColor(0.0, 0.0, 0.0, 0.0);
	glShadeModel(GL_SMOOTH);
	glEnable(GL_DEPTH_TEST);
}

int main(int argc, char** argv)
{
	glutInit(&argc, argv);
	myInit(argv[0]);
	//setUpTexture();
	loadTextures();

	glutKeyboardFunc(myKeyboard);
	glutReshapeFunc(myReshape);
	if (attack_flag == 0) {
		glutPassiveMotionFunc(updateMouse);
	}
	glutDisplayFunc(myDisplay);
	



	glutMainLoop();
	return 0;
}

/*
	do {
		glVertex2d(bone_x + 0.02, -0.4);
		glVertex2d(bone_x + 0.02, bone_y);
		glVertex2d(bone_x, bone_y);
		glVertex2d(bone_x, -0.4);

		bone_x = bone_x + 0.03;
		bone_y = bone_y + 0.015;

		numRectangles++;

	} while(bone_x < 0.18);
	/*
		glVertex2d(0.02, -0.4);
		glVertex2d(0.02, -0.2);
		glVertex2d(0.0, -0.2);
		glVertex2d(0.0, -0.4);

		glVertex2d(0.05, -0.4);
		glVertex2d(0.05, -0.2);
		glVertex2d(0.03, -0.2);
		glVertex2d(0.03, -0.4);
	*/