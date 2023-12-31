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
       'v.1.0.9'：创建子弹
       'v.1.0.10'：修复墙壁位置bug
       'v.1.0.11'：创建敌方子弹
       'v.1.0.12'：创建爆炸效果
       'v.1.0.13'：创建baby
       'v.1.0.14'：添加音效
       'v.1.0.15'：我方与敌方碰撞效果
       'v.1.0.16'：营救baby&修改撞墙效果
       'v.1.0.17'：修改敌方子弹打墙效果&实现胜利和失败的效果

"""


import pygame,time,random

COLOR_BLACK=pygame.Color(0,0,0)
COLOR_RED=pygame.Color(255,0,0)
COLOR_YELLOW=pygame.Color(255,255,0)
version="v1.0.17"

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
    MyBullet_count=100
    Victory=False
    GameOver=False
    baby=None

    def startgame(self):
        pygame.display.init()
        MainGame.window = pygame.display.set_mode([MainGame.SCREEN_WIDTH, MainGame.SCREEN_HEIGHT])
        MainGame.C_P1= MyCharacter(1160, 630)
        MainGame.baby=Baby(1120,30)
        self.creatMyCharacter()
        self.creatEnemy()
        self.creatWalls()
        self.creatSteels()
        pygame.display.set_caption("RescureMyBay" + version)

        while True:
            MainGame.window.fill(COLOR_BLACK)
            self.getEvents()
            MainGame.baby.displaybaby()
            if MainGame.C_P1 and MainGame.C_P1.live:
                MainGame.window.blit(self.getTextSurface("当前生命值:%d" % MainGame.C_P1.hp), (25, 20))
            else:
                MainGame.window.blit(self.getTextSurface("当前生命值:%d" % 0), (25, 20))
            MainGame.window.blit(self.getTextSurface("剩余子弹数量:%d" % MainGame.MyBullet_count), (25, 40))
            if MainGame.C_P1 and MainGame.C_P1.live:
                MainGame.C_P1.displayCharacter()
                MainGame.C_P1.hitWalls()
                MainGame.C_P1.hitSteels()
                MainGame.C_P1.hitEnemy()
                MainGame.C_P1.rescureBaby()
            else:
                del MainGame.C_P1
                MainGame.C_P1=None
                MainGame.GameOver=True
            if MainGame.C_P1 and not MainGame.C_P1.stop==True:
                MainGame.C_P1.move()

            self.blitEnemy()
            self.creatEnemyBullet()
            self.blitWalls()
            self.blitSteels()
            self.blitBullet()
            self.blitEnemyBullet()
            self.displayExplodes()
            if MainGame.Victory:
                MainGame.window.blit(self.getend('VICTORY'), (350, 250))
            if MainGame.GameOver:
                MainGame.window.blit(self.getend('GAMEOVER'), (250, 250))
            time.sleep(0.1)
            pygame.display.update()

    def creatMyCharacter(self):
        MainGame.C_P1= MyCharacter(1160, 630)
        music = Music('img/start.wav')
        music.play()


    def creatEnemy(self):
        tops= [100,200,500,600]
        for i in range(MainGame.Enemy_count//4):
            for top in tops:
                speed = random.randint(10, 20)
                left = random.randint(1, 5)
                eC = Enemy(left * 190, top, speed)
                MainGame.Enemy_list.append(eC)


    def creatWalls(self):
        position=[(1090,100),(1110,100),(1130,100),(1150,100),(1170,100),(400,480),(400,440),(400,460),(20,300),(40,300),(60,300),(500,340),(500,360),(500,320)]
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
                if i<7 or i>9:
                    MainGame.Steel_list.append(Steels(400, 300 + i * 20))
                if i>3:
                    MainGame.Steel_list.append(Steels(i * 20, 300))
                if i<16 or i>18:
                    MainGame.Steel_list.append(Steels(500, i * 20))
            if i<40:
                MainGame.Steel_list.append(Steels(400 + i * 20, 400))
            if i<5:
                MainGame.Steel_list.append(Steels(1090, i * 20))

    def creatEnemyBullet(self):
        for EC in MainGame.Enemy_list:
            num = random.randint(1, 1000)
            if num <= 20:
                MainGame.Enemy_bullet_list.append(Bullet(EC))

    def blitEnemy(self):
        for eC in MainGame.Enemy_list:
            if eC.live:
                eC.displayCharacter()
                eC.randomMove()
                eC.hitSteels()
                eC.hitWalls()
                eC.hitMyCharacter()
            else:
                MainGame.Enemy_list.remove(eC)

    def blitWalls(self):
        for wall in MainGame.Wall_list:
            if wall.live:
                wall.displaywall()
            else:
                MainGame.Wall_list.remove(wall)


    def blitSteels(self):
        for steel in MainGame.Steel_list:
            steel.displaysteel()

    def blitBullet(self):
        for bullet in MainGame.Bullet_list:
            if bullet.live:
                bullet.displaybullet()
                bullet.bulletMove()
                bullet.hitEnemy()
                bullet.hitWalls()
                bullet.hitSteels()
            else:
                MainGame.Bullet_list.remove(bullet)

    def blitEnemyBullet(self):
        for eBullet in MainGame.Enemy_bullet_list:
            if eBullet.live:
                eBullet.displaybullet()
                eBullet.bulletMove()
                eBullet.enemybullethitWalls()
                eBullet.hitSteels()
                if MainGame.C_P1 and MainGame.C_P1.live:
                    eBullet.hitMyCharacter()
            else:
                MainGame.Enemy_bullet_list.remove(eBullet)


    def getTextSurface(self,text):
        pygame.font.init()
        font = pygame.font.SysFont("kaiti", 18)
        textsurface = font.render(text, True, COLOR_RED)
        return textsurface

    def getend(self,text):
        pygame.font.init()

        font = pygame.font.SysFont("arial", 150)
        textsurface = font.render(text, True, COLOR_YELLOW)
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
                        print('发射子弹')
                        if MainGame.MyBullet_count>0:
                            MainGame.MyBullet_count-=1
                            m = Bullet(MainGame.C_P1)
                            MainGame.Bullet_list.append(m)
                            music = Music('img/fire.wav')
                            music.play()
                        else:
                            print('子弹数量不足')
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT or event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                    if MainGame.C_P1 and MainGame.C_P1.live:
                        MainGame.C_P1.stop = True

    def displayExplodes(self):
        for explode in MainGame.Explode_list:
            if explode.live:
                explode.displayexplode()
            else:
                MainGame.Explode_list.remove(explode)

    def endgame(self):
        print('Thank You')
        exit()


class BaseItem(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        

class Baby(BaseItem):
    def __init__(self,left,top):
        self.img = pygame.image.load('img/baby.png')
        self.image = pygame.transform.scale(self.img, (50, 50))
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
        for EC in MainGame.Enemy_list:
            if pygame.sprite.collide_rect(self, EC):
                self.stay()
                music = Music('img/hit.wav')
                music.play()
                self.hp-=0.1
                if self.hp<=0:
                    self.live=False


    def rescureBaby(self):
        if pygame.sprite.collide_rect(self, MainGame.baby):
            MainGame.Victory=True

    def hitWalls(self):
        for wall in MainGame.Wall_list:
            if pygame.sprite.collide_rect(self, wall):
                self.stay()
                wall.hp-=5
                if wall.hp <= 0:
                    music = Music('img/blast.wav')
                    music.play()
                    wall.live = False



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
        if MainGame.C_P1 and pygame.sprite.collide_rect(self, MainGame.C_P1):
            self.stay()
            music = Music('img/hit.wav')
            music.play()
            MainGame.C_P1.hp -= 0.1
            if MainGame.C_P1.hp <= 0:
                MainGame.C_P1.live = False

    def hitWalls(self):
        for wall in MainGame.Wall_list:
            if pygame.sprite.collide_rect(self, wall):
                self.stay()
                wall.hp-=1







class Bullet(BaseItem):
    def __init__(self, C):
        self.image = pygame.image.load('img/enemymissile.gif')
        self.direction = C.direction
        self.rect = self.image.get_rect()
        if self.direction == 'U':
            self.rect.left = C.rect.left + C.rect.width / 2 - self.rect.width / 2
            self.rect.top = C.rect.top - self.rect.height
        elif self.direction == 'D':
            self.rect.left = C.rect.left + C.rect.width / 2 - self.rect.width / 2
            self.rect.top = C.rect.top + C.rect.height
        elif self.direction == 'L':
            self.rect.left = C.rect.left - self.rect.width
            self.rect.top = C.rect.top + C.rect.height / 2 - self.rect.height / 2
        elif self.direction == 'R':
            self.rect.left = C.rect.left + C.rect.width
            self.rect.top = C.rect.top + C.rect.height / 2 - self.rect.height / 2
        self.speed = 40
        self.live = True

    def bulletMove(self):
        if self.direction == 'U':
            self.rect.top -= self.speed

        elif self.direction == 'D':
            self.rect.top += self.speed

        elif self.direction == 'L':
            self.rect.left -= self.speed
        elif self.direction == 'R':
            if self.rect.left < MainGame.SCREEN_WIDTH - self.rect.width:
                self.rect.left += self.speed
            else:
                self.live = False

    def displaybullet(self):
        MainGame.window.blit(self.image,self.rect)

    def hitEnemy(self):
        for eC in MainGame.Enemy_list:
            if pygame.sprite.collide_rect(eC, self):
                self.live = False
                eC.hp-=2
                if eC.hp<=0:
                    MainGame.Explode_list.append(Explode(eC))
                    music = Music('img/blast.wav')
                    music.play()
                    eC.live=False


    def hitWalls(self):
        for wall in MainGame.Wall_list:
            if pygame.sprite.collide_rect(wall, self):
                self.live = False
                wall.hp -= 2
                if wall.hp <= 0:
                    music = Music('img/blast.wav')
                    music.play()
                    wall.live = False

    def enemybullethitWalls(self):
        for wall in MainGame.Wall_list:
            if pygame.sprite.collide_rect(wall, self):
                self.live = False

    def hitSteels(self):
        for steel in MainGame.Steel_list:
            if pygame.sprite.collide_rect(steel, self):
                self.live = False



    def hitMyCharacter(self):
        if pygame.sprite.collide_rect(self, MainGame.C_P1):
            music = Music('img/hit.wav')
            music.play()
            MainGame.C_P1.hp-=2
            self.live = False
            if MainGame.C_P1.hp<=0:
                MainGame.C_P1.live = False



class Explode():
    def __init__(self, C):
        self.rect = C.rect
        self.step = 0
        self.live = True
        self.imgs = [pygame.image.load("img/blast1.gif"),
                     pygame.image.load("img/blast2.gif"),
                     pygame.image.load("img/blast3.gif"),
                     pygame.image.load("img/blast4.gif"),
                     pygame.image.load("img/blast5.gif"),
                     pygame.image.load("img/blast6.gif"),
                     pygame.image.load("img/blast7.gif"),
                     pygame.image.load("img/blast8.gif")]
        self.img = self.imgs[0]
        self.image=pygame.transform.scale(self.img, (50, 50))

    def displayexplode(self):
        if self.step < len(self.imgs):
            MainGame.window.blit(self.image, self.rect)
            self.img = self.imgs[self.step]
            self.image = pygame.transform.scale(self.img, (50, 50))
            self.step += 1
        else:
            self.step = 0
            self.live = False


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
        self.fileName = fileName
        pygame.mixer.init()
        pygame.mixer.music.load(self.fileName)
    def play(self):
        pygame.mixer.music.play()



MainGame().startgame()

