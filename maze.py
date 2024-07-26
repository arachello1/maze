#create a Maze game!
from pygame import *
window = display.set_mode((700, 500))
display.set_caption('maze')
background = transform.scale(image.load('background.jpg'), (700, 500))
clock = time.Clock()
fps = 60
game = True
finish = False

#parent class for sprites
class GameSprite(sprite.Sprite):
   #class constructor
    def __init__(self, player_image, player_x, player_y, player_width, player_height, player_speed):
        super().__init__()
        #every sprite must store the image property
        self.image = transform.scale(image.load(player_image), (player_width, player_height))
        self.speed = player_speed
        #every sprite must have the rect property – the rectangle it is fitted in
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y


    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))
    

class Hero(GameSprite):
    def update(self):
        keys = key.get_pressed()
        if keys[K_LEFT] and self.rect.x > 0:
            self.rect.x -= self.speed
        if keys[K_RIGHT] and self.rect.x < 650:
            self.rect.x += self.speed
        if keys[K_UP] and self.rect.y > 0:
            self.rect.y -= self.speed
        if keys[K_DOWN] and self.rect.y < 445:
            self.rect.y += self.speed

class Enemy(GameSprite):
    direction = 'left'
    def update(self):
        if self.rect.x <= 450:
            self.direction = 'right'
        if self.rect.x >= 650:
            self.direction = 'left'
        if self.direction == 'left':
            self.rect.x -= self.speed
        if self.direction == 'right':
            self.rect.x += self.speed
class Wall(sprite.Sprite):
    def __init__(self, color1, color2, color3, x, y, width, height):
        self.color1 = color1
        self.color2 = color2
        self.color3 = color3
        self.width = width
        self.height = height
        # picture of the wall — a rectangle of the desired size and color
        self.image = Surface((self.width, self.height))
        self.image.fill((color1, color2, color3))
        # each sprite must store a rect property
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
    def draw_wall(self):
        window.blit(self.image, (self.rect.x, self.rect.y))


mixer.init()
mixer.music.load('jungles.ogg')
mixer.music.play()

hero = Hero('hero.png', 10, 400, 65, 65, 10)
enemy = Enemy('cyborg.png', 620, 300, 65, 65, 3)
goal = GameSprite('treasure.png', 580, 415, 65, 65, 0)
wall1 = Wall(0, 0, 0, 200, -50, 25, 450)
wall2 = Wall(0, 0, 0, 430, 100, 25, 450)

font.init()
font = font.Font(None, 70)
lose = font.render('YOU LOSE!', True, (255, 0, 0))
win = font.render('YOU WIN!', True, (0, 255, 0))
while game:
    for e in event.get():
        if e.type == QUIT:
           game = False
    if not finish:
        window.blit(background, (0, 0))
        hero.update()
        enemy.update()
        hero.reset()
        enemy.reset()
        goal.reset()
        wall1.draw_wall()
        wall2.draw_wall()
        if sprite.collide_rect(hero, enemy) or sprite.collide_rect(hero, wall1) or sprite.collide_rect(hero, wall2):
            window.blit(lose, (200, 200))
            finish = True
        if sprite.collide_rect(hero, goal):
            window.blit(win, (200, 200))
            finish = True
    display.update()
    clock.tick(fps)


    