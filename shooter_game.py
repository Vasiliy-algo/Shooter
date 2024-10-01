#Создай собственный Шутер!
from random import randint
from pygame import *

class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_width, player_height, player_x, player_y, player_speed):
        super().__init__()
        self.image = transform.scale(image.load(player_image), (player_width, player_height))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Player (GameSprite):
    def __init__(self, player_image, player_width, player_height, player_x, player_y, player_speed):
        super().__init__(player_image, player_width, player_height, player_x, player_y, player_speed) 
        self.speed_fire = 30
        self.ammo = 5
        self.reload = 0
        
    def update(self):
        keys_pressed = key.get_pressed()
        

        if keys_pressed[K_d] and self.rect.x < 1300:
                self.rect.x += self.speed

        if keys_pressed[K_a] and self.rect.x > 0:
                self.rect.x -= self.speed
        self.speed_fire += 1
    def fire (self):
        keys_pressed = key.get_pressed()
        if self.ammo <= 0:
            self.reload += 1

        if self.reload >= 5:
            text_reload = font5.render('Перезарядка',1,(255, 205, 0))
            window.blit(text_reload, (500,900))            
            if self.reload >= 60:
                self.ammo = 5
                self.reload = 0

            
    
        if self.ammo > 0:
            if keys_pressed[K_SPACE]:
                if self.speed_fire >= 15:
                    bullet = Bullet('bullet.png', 16, 25, self.rect.centerx - 8, 850, 15)
                    billets.add(bullet)
                    self.speed_fire = 0
                    self.ammo -= 1
                    

            
                
            
            
            #bullet_fire.play()

class asteroidse(GameSprite):
    def update(self):
        self.rect.y += self.speed
        

        if self.rect.y > 1000:
            self.rect.y = -70
            self.speed = randint(2, 4)
            self.rect.x = randint(100, 1300)


class Enemy(GameSprite):
    def update(self):
        self.rect.y += self.speed

        if self.rect.y > 1000:
            self.rect.y = -110
            self.speed = randint(2, 4)
            self.rect.x = randint(100, 1300)
            global lose 
            lose += 1
        
        

class Bullet(GameSprite):
    def update(self):
        self.rect.y -= self.speed
        
    

game = True
lose = 0
hit = 0
hp = 3



window = display.set_mode((1400, 1000))
display.set_caption('space wars')

space = transform.scale(image.load('galaxy.jpg'), (1400, 1000))
mixer.init()
mixer.music.load('space.ogg')
#bullet_fire = mixer.Sound('fire.ogg')
#mixer.music.play()
player = Player('rocket.png', 100, 150, 700, 850, 10)
billets = sprite.Group()
aliens = sprite.Group()
asteroids = sprite.Group()
for i in range(1, 6):
    alien = Enemy('ufo.png', 120, 70, randint(100, 1300), -70, randint(2, 4))
    aliens.add(alien)



asteroids.add(asteroidse('asteroid.png', 120, 110, randint(100, 1300), -110, randint(2, 4)))
asteroids.add(asteroidse('asteroid.png', 120, 110, randint(100, 1300), -400, randint(2, 4)))


font.init()
font1 = font.SysFont('Arial', 36)
font2 = font.SysFont('Arial', 36)
font3 = font.SysFont('Arial', 72)
font4 = font.SysFont('Arial', 72)
font5 = font.SysFont('Arial', 72)
font6 = font.SysFont('Arial', 72)






clock = time.Clock()
FPS = 60
while game:
    
    for e in event.get():
        if e.type == QUIT:
            game = False
    if hit < 10 and lose < 3 and hp != 0:    
        text_lose = font1.render('Пропущено: ' + str(lose), 1,(255, 255, 255))
        text_hit = font2.render('Счет: ' + str(hit), 1,(255, 255, 255))
        text_hp = font6.render('HP' + str(hp), 1,(25, 255, 25))
        window.blit(space, (0, 0))

        aliens.draw(window)
        aliens.update()

        asteroids.draw(window)
        asteroids.update()

        billets.draw(window)
        billets.update()

        player.reset()
        player.update()
        player.fire()

        sprites_list = sprite.groupcollide( aliens, billets, True, True)
        for i in sprites_list:
            alien = Enemy('ufo.png', 120, 70, randint(100, 1300), -70, randint(2, 4))
            aliens.add(alien)
            hit += 1 
        
        sprites_lis = sprite.spritecollide(player, aliens, True)
        for i in sprites_lis:
            hp -= 1
        
        sprites_asteroid_bullet = sprite.groupcollide( asteroids, billets, False, True)

        sprites_asteroid = sprite.spritecollide(player, asteroids, True)
        for i in sprites_asteroid:
            hp -= 1



    elif hit >= 10:
        text_win = font3.render('Победа', 1,(105, 255, 105))
        window.blit(text_win,(600,500))

    elif lose >= 3:
        text_lost = font4.render('Проигрыш', 1,(255, 105, 105))
        window.blit(text_lost,(600,500))

    elif hp <= 3:
        text_lost = font4.render('Проигрыш', 1,(255, 105, 105))
        window.blit(text_lost,(600,500))


    text_lose = font1.render('Пропущено: ' + str(lose), 1,(255, 255, 255))
    text_hit = font2.render('Счет: ' + str(hit), 1,(255, 255, 255))
    text_hp = font6.render('HP: ' + str(hp), 1,(25, 255, 25))
    window.blit(text_lose,(1,50))
    window.blit(text_hit,(1,20))
    window.blit(text_hp,(1270,20))
    





        


    display.update()
    clock.tick(FPS)

