"""
版本说明：
       'v.1.0.1'：框架搭建
       'v.1.0.2'：视线游戏开始和关闭
       'v.1.0.3'：创建墙壁
       'v.1.0.4'：设置文字
       'v.1.0.5'：创建我方角色
       'v.1.0.6'：实现我方角色的移动
       'v.1.0.7'：创建敌方角色
       'v.1.0.8'：实现墙壁碰撞效果

"""


import pygame,time,random

COLOR_BLACK=pygame.Color(0,0,0)
COLOR_RED=pygame.Color(255,0,0)
version="v1.0.8"

class MainGame():
    window = None
    SCREEN_HEIGHT = 700
    SCREEN_WIDTH = 1200
    C_P1 = None
    Enemy_list = []
    Enemy_count = 24
    Bullet_list = []
    Enemy_bullet_list = []
    Explode_list = []
    Wall_list = []
    Steel_list=[]

    def startgame(self):
        pygame.display.init()
        MainGame.window = pygame.display.set_mode([MainGame.SCREEN_WIDTH, MainGame.SCREEN_HEIGHT])
        MainGame.C_P1= MyCharacter(1160, 630)
        self.creatEnemy()
        self.creatWalls()
        self.creatSteels()
        pygame.display.set_caption("RescureMyBay" + version)

        while True:
            MainGame.window.fill(COLOR_BLACK)
            self.getEvents()
            MainGame.window.blit(self.getTextSurface("当前生命值:%d" % 20), (25, 20))
            MainGame.window.blit(self.getTextSurface("剩余子弹数量:%d" % 20), (25, 40))
            if MainGame.C_P1 and MainGame.C_P1.live:
                MainGame.C_P1.displayCharacter()
                MainGame.C_P1.hitWalls()
                MainGame.C_P1.hitSteels()
            else:
                del MainGame.C_P1
                MainGame.C_P1=None
            if MainGame.C_P1 and not MainGame.C_P1.stop==True:
                MainGame.C_P1.move()
            self.blitEnemy()
            self.blitWalls()
            self.blitSteels()
            time.sleep(0.1)
            pygame.display.update()

    def creatMyCharacter(self):
        MainGame.C_P1= MyCharacter(1160, 630)


    def creatEnemy(self):
        tops= [100,200,500,600]
        for i in range(MainGame.Enemy_count//4):
            for top in tops:
                speed = random.randint(10, 20)
                left = random.randint(1, 5)
                eC = Enemy(left * 190, top, speed)
                MainGame.Enemy_list.append(eC)


    def creatWalls(self):
        position=[(1120,100),(1140,100),(1160,100),(400,420),(400,440),(400,460),(20,300),(40,300),(60,300),(500,340),(500,360),(500,380)]
        for left,top in position:
            wall=Walls(left,top)
            MainGame.Wall_list.append(wall)

    def creatSteels(self):
        for i in range(60):
            MainGame.Steel_list.append(Steels(i*20,680))
            MainGame.Steel_list.append(Steels(i*20,0))
            if i<35:
                MainGame.Steel_list.append(Steels(0, i * 20))
            if i<31:
                MainGame.Steel_list.append(Steels(1180, i * 20))
            if i<20:
                if i<6 or i>8:
                    MainGame.Steel_list.append(Steels(400, 300 + i * 20))
                if i>3:
                    MainGame.Steel_list.append(Steels(i * 20, 300))
                if i<17:
                    MainGame.Steel_list.append(Steels(500, i * 20))
            if i<40:
                MainGame.Steel_list.append(Steels(400 + i * 20, 400))
            if i<5:
                MainGame.Steel_list.append(Steels(1090, i * 20))
            if i<2:
                MainGame.Steel_list.append(Steels(1090 + i * 20, 100))

    def blitEnemy(self):
        for eC in MainGame.Enemy_list:
            if eC.live:
                eC.displayCharacter()
                eC.randomMove()
                eC.hitSteels()
                eC.hitWalls()
            else:
                MainGame.Enemy_list.remove(eC)

    def blitWalls(self):
        for wall in MainGame.Wall_list:
            wall.displaywall()


    def blitSteels(self):
        for steel in MainGame.Steel_list:
            steel.displaysteel()

    def blitBullet(self):
        pass

    def blitEnemyBullet(self):
        pass

    def blitBaby(self):
        pass


    def getTextSurface(self,text):
        pygame.font.init()
        font = pygame.font.SysFont("kaiti", 18)
        textsurface = font.render(text, True, COLOR_RED)
        return textsurface

    def getEvents(self):
        eventlist = pygame.event.get()
        for event in eventlist:
            if event.type == pygame.QUIT:
                self.endgame()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE and not MainGame.C_P1:
                    self.creatMyCharacter()
                if MainGame.C_P1 and MainGame.C_P1.live:
                    if event.key == pygame.K_LEFT:
                        print("向左调头")
                        MainGame.C_P1.direction = 'L'
                        MainGame.C_P1.stop = False

                    elif event.key == pygame.K_RIGHT:
                        print("向右调头")
                        MainGame.C_P1.direction = 'R'
                        MainGame.C_P1.stop = False
                    elif event.key == pygame.K_UP:
                        print("向上调头")
                        MainGame.C_P1.direction = 'U'
                        MainGame.C_P1.stop = False
                    elif event.key == pygame.K_DOWN:
                        print("向下调头")
                        MainGame.C_P1.direction = 'D'
                        MainGame.C_P1.stop = False
                    elif event.key == pygame.K_SPACE:
                        pass
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT or event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                    if MainGame.C_P1 and MainGame.C_P1.live:
                        MainGame.C_P1.stop = True

    def displayExplodes(self):
        pass

    def endgame(self):
        print('Thank You')
        exit()


class BaseItem(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        

class Baby(BaseItem):
    def __init__(self,left,top):
        self.img = pygame.image.load('img/baby.png')
        self.image = pygame.transform.scale(self.img, (20, 20))
        self.rect = self.image.get_rect()
        self.rect.left = left
        self.rect.top = top

    def displaybaby(self):
        MainGame.window.blit(self.image,self.rect)


class Character(BaseItem):
    def __init__(self,left,top):
        self.speed = 15
        self.stop = True
        self.live = True
        self.hp=10
        self.stop_imgs={'U':pygame.image.load('img/U0.png'),
                        'D':pygame.image.load('img/D0.png'),
                        'R':pygame.image.load('img/R0.png'),
                        'L':pygame.image.load('img/L0.png')}
        self.U = [pygame.image.load("img/U1.png"),
                  pygame.image.load("img/U2.png"),
                  pygame.image.load("img/U3.png"),
                  pygame.image.load("img/U4.png"),
                  pygame.image.load("img/U5.png"),
                  pygame.image.load("img/U6.png"),
                  pygame.image.load("img/U7.png")]
        self.D = [pygame.image.load("img/D1.png"),
                  pygame.image.load("img/D2.png"),
                  pygame.image.load("img/D3.png"),
                  pygame.image.load("img/D4.png"),
                  pygame.image.load("img/D5.png"),
                  pygame.image.load("img/D6.png"),
                  pygame.image.load("img/D7.png"),
                  pygame.image.load("img/D8.png")]
        self.L = [pygame.image.load("img/L1.png"),
                  pygame.image.load("img/L2.png"),
                  pygame.image.load("img/L3.png"),
                  pygame.image.load("img/L4.png"),
                  pygame.image.load("img/L5.png"),
                  pygame.image.load("img/L6.png"),
                  pygame.image.load("img/L7.png")]
        self.R = [pygame.image.load("img/R1.png"),
                  pygame.image.load("img/R2.png"),
                  pygame.image.load("img/R3.png"),
                  pygame.image.load("img/R4.png"),
                  pygame.image.load("img/R5.png"),
                  pygame.image.load("img/R6.png"),
                  pygame.image.load("img/R7.png"),
                  pygame.image.load("img/R8.png")]
        self.imgs = {'U': self.U,'D': self.D,'R': self.R,'L': self.L}
        self.step = 0
        self.direction = 'U'
        self.stop_img = self.stop_imgs[self.direction]
        self.image=pygame.transform.scale(self.stop_img, (50, 50))
        self.rect = self.image.get_rect()
        self.rect.left = left
        self.rect.top = top
        self.oldleft = self.rect.left
        self.oldtop = self.rect.top

    def move(self):
        self.oldleft = self.rect.left
        self.oldtop = self.rect.top
        if self.direction == 'L':
            self.rect.left -= self.speed
        elif self.direction == 'R':
            self.rect.left += self.speed
        elif self.direction == 'U':
            self.rect.top -= self.speed
        elif self.direction == 'D':
            self.rect.top += self.speed

    def stay(self):
        self.rect.left = self.oldleft
        self.rect.top = self.oldtop

    def hitSteels(self):
        for steel in MainGame.Steel_list:
            if pygame.sprite.collide_rect(self, steel):
                self.stay()

    def hitWalls(self):
        for wall in MainGame.Wall_list:
            if pygame.sprite.collide_rect(self, wall):
                self.stay()

    def shot(self):
        pass

    def displayCharacter(self):
        if self.stop==False:
            if self.step<len(self.imgs[self.direction]):
                MainGame.window.blit(self.image, self.rect)
                self.img=self.imgs[self.direction][self.step]
                self.image = pygame.transform.scale(self.img, (50, 50))
                self.step += 1
            else:
                self.step=0
                MainGame.window.blit(self.image, self.rect)
                self.img = self.imgs[self.direction][self.step]
                self.image = pygame.transform.scale(self.img, (50, 50))
                self.step += 1
        else:
            self.stop_img = self.stop_imgs[self.direction]
            self.image = pygame.transform.scale(self.stop_img, (50, 50))
            MainGame.window.blit(self.image, self.rect)



class MyCharacter(Character):
    def __init__(self,left,top):
        super(MyCharacter,self).__init__(left,top)

    def hitEnemy(self):
        pass



class Enemy(Character):
    def __init__(self, left, top, speed):
        #super(Enemy, self).__init__(left, top)
        self.stop_imgs = {'U': pygame.image.load('img/EU.png'),
                    'D': pygame.image.load('img/ED.png'),
                    'R': pygame.image.load('img/ER.png'),
                    'L': pygame.image.load('img/EL.png')}
        self.direction = self.randDirection()
        self.stop_img = self.stop_imgs[self.direction]
        self.image = pygame.transform.scale(self.stop_img, (50, 50))
        self.rect = self.image.get_rect()
        self.rect.left = left
        self.rect.top = top
        self.speed = speed
        self.step = 50
        self.stop = True
        self.live=True
        self.hp=2

    def randDirection(self):
        num = random.randint(1, 4)
        if num == 1:
            return 'U'
        elif num == 2:
            return 'D'
        elif num == 3:
            return 'L'
        elif num == 4:
            return 'R'

    def randomMove(self):
        if self.step <= 0:
            self.direction = self.randDirection()
            self.step = 50
        else:
            self.move()
            self.step -= 1

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



class Walls():
    def __init__(self, left, top):
        self.img = pygame.image.load('img/walls.gif')
        self.image=pygame.transform.scale(self.img, (20, 20))
        self.rect = self.image.get_rect()
        self.rect.left = left
        self.rect.top = top
        self.live = True
        self.hp = 6

    def displaywall(self):
        MainGame.window.blit(self.image,self.rect)


class Steels():
    def __init__(self,left,top):
        self.img = pygame.image.load('img/steels.gif')
        self.image = pygame.transform.scale(self.img, (20, 20))
        self.rect = self.image.get_rect()
        self.rect.left = left
        self.rect.top = top

    def displaysteel(self):
        MainGame.window.blit(self.image,self.rect)



class Music():
    def __init__(self, fileName):
        pass

    def play(self):
        pass


MainGame().startgame()