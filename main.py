"""
版本说明：
       'v.1.0.1'：框架搭建

"""


import pygame,time,random

COLOR_BLACK=pygame.Color(0,0,0)
COLOR_RED=pygame.Color(255,0,0)
version="v1.0.1"

class MainGame():
    def __init__(self):
        pass

    def startgame(self):
        pass

    def creatMyCharacter(self):
        pass

    def creatEnemy(self):
        pass

    def creatWalls(self):
        pass

    def creatSteels(self):
        pass

    def blitEnemy(self):
        pass

    def blitWalls(self):
        pass

    def blitSteels(self):
        pass

    def blitBullet(self):
        pass

    def blitEnemyBullet(self):
        pass

    def getTextSurface(self,text):
        pass

    def getEvents(self):
        pass

    def displayExplodes(self):
        pass

    def endgame(self):
        pass


class BaseItem(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)


class Character(BaseItem):
    def __init__(self):
        pass

    def move(self):
        pass

    def action(self):
        pass

    def stay(self):
        pass

    def hitSteels(self):
        pass

    def hitWalls(self):
        pass

    def shot(self):
        pass

    def displayCharacter(self):
        pass



class MyCharacter(Character):
    def __init__(self,left,top):
        super(MyCharacter,self).__init__(left,top)

    def hitEnemy(self):
        pass



class Enemy(Character):
    def __init__(self, left, top, speed):
        pass

    def randDirection(self):
        pass

    def randomMove(self):
        pass

    def hitMyCharacter(self):
        pass

    def shot(self):
        pass



class Bullet(BaseItem):
    def __init__(self, c):
        pass

    def bulletMove(self):
        pass

    def dispalybullet(self):
        pass

    def hitEnemyTank(self):
        pass

    def hitWalls(self):
        pass

    def hitMyCharacter(self):
        pass



class Explode():
    def __init__(self, tank):
        pass

    def displayexplode(self):
        pass



class Wall():
    def __init__(self, left, top):
        pass

    def dispalywall(self):
        pass


class Steels():
    def __init__(self):
        pass

    def displaySteels(self):
        pass



class Music():
    def __init__(self, fileName):
        pass

    def play(self):
        pass


MainGame().startgame()