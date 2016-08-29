#! /usr/bin/env python
# -*- coding: utf-8 -*-
#作者:Ferminal
#功能：射击类游戏
#说明：第一个python程序游戏

#1 - Import library
#Import random library, using random functions；导入random库，使用随机功能
import random
#Import math library, the use of mathematical functions；导入math库，使用数学函数功能
import math
import pygame
from pygame.locals import *

#2 - Initialize the game
#Import pygame function；pygame库初始化
pygame.init()
#Define the length and width of the game screen；设置游戏屏幕的长和宽
width, height = 600, 400
#Using pygame screen definition function；使用pygame屏幕画图功能
screen=pygame.display.set_mode((width,height))
#Set the control up and down around the queue；定义上下左右按键功能
keys = [False,False,False,False]
#Set the initial position of the player；设置初始player在屏幕上的位置
playerpos = [100,100]
#Define the firing accuracy and arrow；定义射击准确率和箭头
acc=[0,0]
arrows=[]
#Set a villain role, set the initial starting position；定义坏蛋出现定时器，坏蛋出现的初始位置，显示血量
badtimer=100
badtimer1=0
badguys=[[536,270]]
healthvalue=216
#3 -Load looping images
#Import screen background image, must be put in the first place；导入背景画面图
humian = pygame.image.load("D:\mywork\game001\images\hu_chunse1.png")
#Import player picture；导入射击者图片
player = pygame.image.load("D:\mywork\game001\images\green.jpg")
#Import protected images；导入被保护者图片
baohu = pygame.image.load("D:\mywork\game001\images\zaohu1.jpg")
#Import shot arrow；导入箭头图片
jiantou = pygame.image.load("D:\mywork\game001\images\jiantou1.jpg")
#Import bad pictures and copy；导入坏人图片及复制坏人图片
badguyimg1 = pygame.image.load("D:\mywork\game001\images\huaidan1.jpg")
badguyimg=badguyimg1
#Import healthbar and health；导入血量图片及减少血量图片
healthbar = pygame.image.load("D:\mywork\game001\images\healthbar1.jpg")
health = pygame.image.load("D:\mywork\game001\images\health1.jpg")
#Import gameover and youwin picture；导入游戏结束画面及胜利画面
gameover = pygame.image.load("D:\mywork\game001\images\gameover1.png")
youwin = pygame.image.load("D:\mywork\game001\images\youwin1.png")
#4 - keep looping through
#Games forever cycle；游戏主程序循环启动
running = 1#游戏是否进行
exitcode = 0
while running:
	#5 - clear the screen before drawing it again
	screen.fill(0)
	#6 - draw the screen elements；加入屏幕元素
	#保证背景图片能够铺满整个屏幕
	for x in range(width/humian.get_width()+1):
		for y in range(height/humian.get_height()+1):
			screen.blit(humian,(x*100,y*100))
	#Protected image position and number；被保护者在屏幕显示初始位置，4个被保护者
	screen.blit(baohu,(0,30))
	screen.blit(baohu,(0,130))
	screen.blit(baohu,(0,230))
	screen.blit(baohu,(0,330))
	#Mouse position function；鼠标的位置定义
	position = pygame.mouse.get_pos()
	#The angle between the mouse and the player position,position[1]for the X axis, position[0] for the Y axis；
	#鼠标与player之间的位置，计算出player的旋转方向，x、y坐标换算，利用math三角函数实现
	angle = math.atan2(position[1]-(playerpos[1]),position[0]-(playerpos[0]))
	playerrot = pygame.transform.rotate(player,360-angle*57.29)
	playerpos1 = (playerpos[0]-playerrot.get_rect().width/2,playerpos[1]-playerrot.get_rect().height/2)
	screen.blit(playerrot, playerpos1)
	#Draw the arrow on the screen；将箭头画到屏幕上，箭头速度，箭头超过屏幕删除，箭头射击方向及位置
	for bullet in arrows:
		index=0
		velx=math.cos(bullet[0])*10
		vely=math.sin(bullet[0])*10
		bullet[1]+=velx
		bullet[2]+=vely
		if bullet[1]<-64 or bullet[1]>536 or bullet[2]<-64 or bullet[2]>395:
			arrows.pop(index)
		index+=1
		for projectile in arrows:
			arrow1 = pygame.transform.rotate(jiantou, 360-projectile[0]*57.29)
			screen.blit(arrow1,(projectile[1],projectile[2]))
	#Draw the bad guy to the screen；将坏人画到屏幕上，坏人出现位置随机，定时器设置出现频率
	if badtimer==0:
		badguys.append([536,random.randint(40,345)])
		badtimer=100-(badtimer1*2)
		if badtimer1>=15:
			badtimer1=15
		else:
			badtimer1+=5
	index=0
	for badguy in badguys:
		if badguy[0]<0:
			badguys.pop(index)
		badguy[0]-=1
		#Health value condition；被保护者血量显示，每次被撞击后，随机减少血量
		badrect=pygame.Rect(badguyimg.get_rect())
		badrect.top=badguy[1]
		badrect.left=badguy[0]
		if badrect.left<64:
			healthvalue-=random.randint(5,20)
			badguys.pop(index)
		#The arrow hit the bad guy；当箭头射中坏人，箭头和坏人都将删除
		index1=0
		for bullet in arrows:
			bullrect=pygame.Rect(jiantou.get_rect())
			bullrect.left=bullet[1]
			bullrect.top=bullet[2]
			if badrect.colliderect(bullrect):
				acc[0]+=1
				badguys.pop(index)
				arrows.pop(index1)
		index+=1
	for badguy in badguys:
		screen.blit(badguyimg,badguy)
	#7 - update the screen
	#Set time identification；显示时间，1分30秒时间倒计时显示，字体大小，显示位置等
	font = pygame.font.Font(None,24)
	survivedtext = font.render(str((60000-pygame.time.get_ticks())/60000)+":"+str((60000-pygame.time.get_ticks())/1000%60).zfill(2),True,(0,0,0))
	textRect = survivedtext.get_rect()
	textRect.topright=[510,10]
	screen.blit(survivedtext,textRect)
	#draw health bar；显示血量条，位置，每次减少量随机，将绿色血条覆盖红色血条；
	screen.blit(healthbar,(10,10))
	for health1 in range(healthvalue):
		screen.blit(health,(health1+10,10))
	pygame.display.flip()
	#8 - loop through the event
	#检查屏幕上操作事件，退出、键盘按下、放开，鼠标点击等事件；
	for event in pygame.event.get():
	    # check if the event is the X button；退出游戏
		if event.type==pygame.QUIT:
		    #if it is quit the game
			pygame.quit()
			exit(0)
		#Key press operation；按下键盘方向键
		if event.type == pygame.KEYDOWN:
			if event.key==K_w:
				keys[0]=True
			elif event.key==K_a:
				keys[1]=True
			elif event.key==K_s:
				keys[2]=True
			elif event.key==K_d:
				keys[3]=True
		#Directional button on the operation；放开键盘方向键
		if event.type == pygame.KEYUP:
			if event.key==K_w:
				keys[0]=False
			elif event.key==K_a:
				keys[1]=False
			elif event.key==K_s:
				keys[2]=False
			elif event.key==K_d:
				keys[3]=False
		#When the mouse click, calculate the angle between the arrow and the player；点击鼠标事件
		if event.type ==pygame.MOUSEBUTTONDOWN:
			position=pygame.mouse.get_pos()
			#点击一次鼠标记录一次射击，算准确率
			acc[1]+=1
			arrows.append([math.atan2(position[1]-(playerpos1[1]+32),position[0]-(playerpos1[0]+26)),playerpos1[0]+32,playerpos1[1]+32])
# 9 - Move player moving frequency；方向键每次移动频率大小
	if keys[0]:
		playerpos[1]-=4
	elif keys[2]:
		playerpos[1]+=4
	if keys[1]:
		playerpos[0]-=4
	elif keys[3]:
		playerpos[0]+=4
	badtimer-=1
	#Win or lost check；判断整盘游戏结果，输、赢等
	if pygame.time.get_ticks()>=60000:
		running=0
		exitcode=1
	if healthvalue<=0:
		running=0
		exitcode=0
	if acc[1]!=0:
		accuracy=acc[0]*1.0/acc[1]*100
		#保留小数点后两位设置
		accuracy1='{:.2f}'.format(accuracy)
	else:
		accuracy=0
		accuracy1=0
#如果被保护者血量没有了，显示失败图片，否则算出射击精度结果及显示胜利图片
if exitcode==0:
	pygame.font.init()
	font = pygame.font.Font(None,24)
	text = font.render("Accuracy: "+str(accuracy1)+"%",True,(255,0,0))
	textRect = text.get_rect()
	textRect.centerx = screen.get_rect().centerx
	textRect.centery = screen.get_rect().centery+24
	screen.blit(gameover,(0,0))
	screen.blit(text,textRect)
else:
	pygame.font.init()
	font = pygame.font.Font(None,24)
	text = font.render("Accuracy: "+str(accuracy1)+"%",True,(255,0,0))
	textRect = text.get_rect()
	textRect.centerx = screen.get_rect().centerx
	textRect.centery = screen.get_rect().centery+24
	screen.blit(youwin,(0,0))
	screen.blit(text,textRect)
while 1:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			pygame.quit()
			exit(0)
	pygame.display.flip()