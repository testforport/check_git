#Создай собственный Шутер!
from pygame import *
from random import randint
from time import time as t

#Классы
class GameSprite(sprite.Sprite):
#конструктор класса
    def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed):
        #Вызываем конструктор класса (Sprite):
        sprite.Sprite.__init__(self)

        #каждый спрайт должен хранить свойство image - изображение
        self.image = transform.scale(image.load(player_image), (size_x, size_y))
        self.speed = player_speed
        self.x_speed = 0

        #каждый спрайт должен хранить свойство rect - прямоугольник, в который он вписан
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y

        self.width = size_x
        self.height = size_y
    #метод, отрисовывающий героя на окне
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Player(GameSprite):
   #метод для управления спрайтом стрелками клавиатуры
    def update(self):
        keys = key.get_pressed()
        if keys[K_LEFT] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys[K_RIGHT] and self.rect.x < win_width - 80:
            self.rect.x += self.speed
    #метод "выстрел" (используем место игрока, чтобы создать там пулю)
    def fire(self):
        global lives
        bullet = Bullet(player_image="bullet.png", 
                        player_x=self.rect.x+self.width//2, 
                        player_y=self.rect.y, 
                        size_x=10, 
                        size_y=30, 
                        player_speed=100)

        bullets.add(bullet)
        fire_sound.play()

class Enemy(GameSprite):
    def update(self):
        global lost
        self.rect.y += self.speed
        if self.rect.y >= win_height:
            self.rect.y = 0
            self.rect.x = randint(0, win_width-120)
            lost += 1
class Asteroid(GameSprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y >= win_height:
            self.rect.y = 0
            self.rect.x = randint(0, win_width-120)

class Bullet(GameSprite):
    def update(self):
        self.rect.y -= self.speed 

        if self.rect.y <= 0:
            self.kill()

def restart():
    global lost
    global score
    global lives
    lost = 0
    score = 0
    lives = 5

    for enemy in monsters:
        enemy.kill()
    for bullet in bullets:
        bullet.kill()
    for asteroid in asteroids:
        asteroid.kill()
    
    for i in range(5):
        enemy = Enemy(player_image="ufo.png", 
                        player_x=randint(0, win_width-120), 
                        player_y=0,
                        size_x=80,
                        size_y=80, 
                        player_speed=randint(1, 3))
        monsters.add(enemy)
    for i in range(3):
        asteroid = Asteroid(player_image="asteroid.png", 
                    player_x=randint(0, win_width-120), 
                    player_y=0,
                    size_x=80,
                    size_y=80, 
                    player_speed=randint(4, 6))
        asteroids.add(asteroid)

#Переменные
clock = time.Clock()
FPS = 30
t1 = 0
lost = 0
score = 0
win_width = 900
win_height = 700
window_size = (900, 700)
lives = 5
bullets = sprite.Group()


font.init()
font1 = font.SysFont("Arial", 36)

font2 = font.SysFont("Arial", 72)

font3 = font.SysFont("Arial", 108)

#
mixer.init()
mixer.music.load('space.ogg')
mixer.music.play()
window = display.set_mode(window_size)
background = transform.scale(image.load('galaxy.jpg'),(window_size))

fire_sound = mixer.Sound("fire.ogg")

#обьекты
playerShip = sprite.Group()
spaceship = Player(player_image="rocket.png", 
                    player_x=win_width//2, 
                    player_y=win_height - 120, 
                    size_x=80, 
                    size_y=80, 
                    player_speed=10)
playerShip.add(spaceship)

monsters = sprite.Group()
for i in range(5):
    enemy = Enemy(player_image="ufo.png", 
                    player_x=randint(0, win_width-120), 
                    player_y=0,
                    size_x=80,
                    size_y=80, 
                    player_speed=randint(1, 3))
    monsters.add(enemy)

asteroids = sprite.Group()
for i in range(3):
    asteroid = Asteroid(player_image="asteroid.png", 
                player_x=randint(0, win_width-120), 
                player_y=0,
                size_x=80,
                size_y=80, 
                player_speed=randint(4, 6))
    asteroids.add(asteroid)
#цикл
run = True
finish = False
rel_time = False
num_fire = 0
text_fail = font2.render("Иноплянетяне заполонили землю!", 1, (255, 0, 0))
text_win = font2.render("Иноплянетяне уничтожены!", 1, (0, 255, 0))
while run:
    for e in event.get():
        if e.type == QUIT:
            run = False
        elif e.type == KEYDOWN:
            if e.key == K_SPACE:
                if num_fire < 5 and rel_time == False:
                    fire_sound.play()
                    spaceship.fire()
                    num_fire += 1
                if num_fire >= 5 and rel_time == False:
                    last_time = t()
                    rel_time = True
            if finish == True and e.key == K_r:
                restart()
                finish = False

    if not finish:
        asteroidShot = sprite.groupcollide(asteroids, bullets, False, True)
        collides = sprite.groupcollide(monsters, bullets, True, True)
        for c in collides:
            score = score + 1
            enemy = Enemy(player_image="ufo.png", 
                player_x=randint(0, win_width-120), 
                player_y=0,
                size_x=80,
                size_y=80, 
                player_speed=randint(1, 3))
            monsters.add(enemy)
        window.blit(background, (0,0))
        spaceship.update()
        monsters.update()
        bullets.update()
        asteroids.update()
        spaceship.reset()
        monsters.draw(window)
        bullets.draw(window)
        asteroids.draw(window)
        text_lose = font1.render("Пропущено: " + str(lost), 1, (255, 255, 255))
        text_destroy = font1.render("Уничтожено: " + str(score), 1, (255, 255, 255))
        text_lives = font3.render(str(lives), 1, (255, 255, 255))
        window.blit(text_lose, (10, 40))
        window.blit(text_destroy, (10, 10))
        window.blit(text_lives, (825, 10))

        if lost >= 10 or lives <= 0:
            finish = True
            window.blit(text_fail, (200, 200))
        elif sprite.groupcollide(playerShip, monsters, False, True):
            lives -= 1
            enemy = Enemy(player_image="ufo.png", 
                    player_x=randint(0, win_width-120), 
                    player_y=0,
                    size_x=80,
                    size_y=80, 
                    player_speed=randint(1, 3))
            monsters.add(enemy)
        elif sprite.groupcollide(playerShip, asteroids, False, True):
            lives -= 1
            asteroid = Asteroid(player_image="asteroid.png", 
                player_x=randint(0, win_width-120), 
                player_y=0,
                size_x=80,
                size_y=80, 
                player_speed=randint(4, 6))
            asteroids.add(asteroid)
        elif score >= 100:
            finish = True
            window.blit(text_win, (200, 200))

    display.update()
    clock.tick(FPS)