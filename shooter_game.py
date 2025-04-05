
from pygame import *
from random import randint
from time import time as timer
mixer.init()
fire_sound = mixer.Sound("fire.ogg")
lost = 0
ochki = 0


class GameSprite(sprite.Sprite):
    def __init__(self, player_image,player_x,player_y,w,h,player_speed):
        super().__init__()
        self.image= transform.scale(image.load(player_image), (w,h))
        self.speed= player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y


    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Player(GameSprite):
    def update(self):
        keys=key.get_pressed()
        if keys[K_LEFT] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys[K_RIGHT] and self.rect.x < 700 - 80:
            self.rect.x += self.speed
        if keys[K_UP] and self.rect.y > 5:
            self.rect.y -= self.speed
        if keys[K_DOWN] and self.rect.y < 500 - 80:
            self.rect.y += self.speed
    def fire(self):
        bullet = Bullet('bullet.png', self.rect.centerx, self.rect.top, 15,20,15)
        bullets.add(bullet)
class Enemy(GameSprite):
    def update(self):
        self.rect.y += self.speed
        global lost
        if self.rect.y > 500:
            self.rect.y = 0
            lost = lost + 1
            self.rect.x = randint(0,620)

class Bullet(GameSprite):
    def update(self):
        self.rect.y -= self.speed
        if self.rect.y < 0:
            self.kill()

bullets = sprite.Group()

font.init()
font2 = font.SysFont('Arial',35)
font1 = font.SysFont('Arial',70)

win = font1.render('YOU WIN', True,(0, 255, 0))
lose = font1.render('YOU LOSE', True, (255,0,0))

finish = False
display.set_caption('Shoter')
window= display.set_mode((700,500))
display.set_caption('ракетааааааааа')
bg= transform.scale(image.load('galaxy.jpg'), (700,500))


ship= Player('rocket.png', 5 , 500-80,80,100,4)
mixer.music.load('space.ogg')
mixer.music.play()
mixer.music.set_volume(0.1)

monsters = sprite.Group()
for i in range(5):
    monster = Enemy('ufo.png', randint(0,620), -40,80,50,randint(1,5))
    monsters.add(monster)

asteroids = sprite.Group()
for i in range(3):
    asteroid = Enemy('asteroid.png', randint(0,620), -40,80,50,randint(1,3))
    asteroids.add(asteroid)

finish = False

run =True

num_fire = 0
real_time = False
while run:
    for e in event.get():
        if e.type == QUIT:
            run = False
        if e.type ==KEYDOWN:
            if e.key == K_SPACE:
                if num_fire < 5 and real_time ==False:
                    num_fire +=1
                    fire_sound.play()
                    ship.fire()
                if num_fire >= 5 and real_time ==False:
                    last_time = timer()
                    rel_time= True
                
    if not finish:
        window.blit(bg, (0,0))
        if real_time:
            now_time=timer()
            if now_time - last_time < 3:
                reload = font2.render ('Malt, reload..',True, (150,0,0))
                window.blit(reload,(250,400)) 
            else:
                num_fire = 0
                real_time=False






        ship.reset()
        ship.update()
        monsters.draw(window)
        monsters.update()
        bullets.draw(window)
        bullets.update()
        asteroids.draw(window)
        asteroids.update()
        text_lose = font2.render ('Пропущено:'+str(lost), True, (255,255,255))
        window.blit(text_lose, (10,20))
        text_skore = font2.render ('очки:'+str(ochki), True, (255,255,255))
        window.blit(text_skore, (10,50))
        if sprite.groupcollide(monsters,bullets,True,True):
            ochki += 1
            monster = Enemy('ufo.png', randint(0,620), -40,80,50,randint(1,5))
            monsters.add(monster)
        if ochki > 9:
            finish = True
            window.blit(win, (200,200))


        if lost > 2:
            finish = True
            window.blit(lose, (200,200))


        if sprite.spritecollide(ship,monsters, True):
            finish = True
            window.blit(lose, (200,200))




    display.update()
    time.delay(10)

