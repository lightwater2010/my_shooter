#Создай собственный Шутер!

from pygame import *
from random import randint
from time import time as t

window = display.set_mode((700,500))
display.set_caption("Шутер")

bg = transform.scale(image.load("galaxy.jpg"), (700,500))
font.init()
font1 = font.SysFont("Arial", 40)
font2 = font.SysFont("Arial", 80)
font3 = font.SysFont("Arial", 30)
class Game_Sprite(sprite.Sprite):
     def __init__(self, x,y, path, size, speed):
          super().__init__()
          self.path = path
          self.size = size
          self.image = transform.scale(image.load(self.path), self.size)
          self.speed = speed
          self.rect = self.image.get_rect()
          self.rect.x = x
          self.rect.y = y
     def draw_sprite(self):
          window.blit(self.image, (self.rect.x, self.rect.y))
class Bullet(Game_Sprite):
     def update(self):
          global bullets
          if self.rect.y < 0:
               self.kill()
          else:
               self.rect.y -= self.speed
     


class Enemy(Game_Sprite):
     def update(self, racket):
          global points
          global hp
          if self.rect.y > 500:
               self.rect.y = 0
               self.rect.x = randint(0,600)
               if self.path == "ufo.png":
                    racket.missing_enemies += 1
          elif sprite.spritecollide(self, bullets, True):
               self.rect.y = 0
               self.rect.x = randint(0,600)
               if self.path == "ufo.png":
                    points += 1
          elif self.rect.colliderect(racket.rect) == 1:
               self.rect.y = 0
               self.rect.x = randint(0,600)
               hp -= 1
          else:
               self.rect.y += self.speed
class Player(Game_Sprite):
     def __init__(self, x,y, path, size, speed, points,missing_enemies, hp):
          super().__init__(x,y, path, size, speed)
          self.points = points
          self.missing_enemies = missing_enemies
          self.hp = hp
          self.num_fires = 0
     def binding(self):
          keys_pressed = key.get_pressed()
          if keys_pressed[K_d] and self.rect.x <= 600:
               self.rect.x += self.speed
          if keys_pressed[K_a] and self.rect. x > 0:
               self.rect.x -= self.speed
     def fire_in_the_hole(self):
          global fire_sound
          bullets.add(Bullet(randint(self.rect.centerx,self.rect.centerx+10),self.rect.top, "bullet.png", (15,25), 10))
          fire_sound.play()
                    
                                     
                         
                    
     #def collision(self):
     #     global enemies
     #     for enemy in enemies:
     #          if self.rect.colliderect(enemy.rect) == 1:
     #               self.missing_enemies += 1
     #               enemy.rect.y = 0
     #               enemy.rect.x = randint(0,600)
game_run = True
FPS = 80
clock = time.Clock()
mixer.init()
mixer.music.load("space.ogg")
mixer.music.play()
racket = Player(300, 400, "rocket.png", (90,90), 6, 0, 0, 10)
bullets = sprite.Group()
enemies = sprite.Group()
asteroids = sprite.Group()
win_text = font2.render("You won!!!", True, (236, 158, 2))
lose_text = font2.render("You lost...?", True, (2, 126, 236))
finish = False
fire_sound = mixer.Sound('fire.ogg')
losing_sound = mixer.Sound("losing_sound.ogg")
winning_sound = mixer.Sound("victory.ogg")
points = racket.points
hp = racket.hp
reload_txt = font3.render("Your gun is reloading...", True, (219, 40, 22))
num_fires = racket.num_fires
rel_time = False
for i in range(1,6):
     enemy = Enemy(randint(0,600), 0, "ufo.png", (80,60), 1)
     enemies.add(enemy)
for x in range(3):
     asteroids.add(Enemy(randint(0,600), 0, "asteroid.png", (80,60),1))
while game_run:
     for ev in event.get():
          if ev.type == QUIT:
               game_run = False
          if ev.type == KEYDOWN:
               if ev.key == K_SPACE:
                    if num_fires < 15 and rel_time == False:
                         racket.fire_in_the_hole()
                         num_fires += 1
                    elif num_fires >= 15 and rel_time == False:
                         rel_time = True
                         time_reload = t()
     points_text = font1.render(f"Счёт: {points}", True, (233, 233, 233))
     missing_enemies_text = font1.render(f"Пропущено:{racket.missing_enemies}", True, (233, 233, 233))
     hp_text = font1.render(f"{hp} HP", True, (219, 40, 22))
     keys = keys_pressed = key.get_pressed()
     if not finish: 
          window.blit(bg, (0,0))
          racket.draw_sprite()
          enemies.draw(window)
          enemies.update(racket)
          asteroids.draw(window)
          asteroids.update(racket)
          racket.binding()
          bullets.draw(window)
          bullets.update()
          window.blit(points_text, (0,0))
          window.blit(missing_enemies_text, (0,40))
          window.blit(hp_text, (600,10))
          if rel_time:
               time_reload_end = t()
               if time_reload_end - time_reload < 2:
                    window.blit(reload_txt,(250, 400))
               else:
                    num_fires = 0
                    rel_time = False
          if racket.missing_enemies >= 10 or hp == 0:
              losing_sound.play()
              window.blit(lose_text, (200,200))
              finish  = True
          elif points >= 30:
               winning_sound.play()
               window.blit(win_text, (200,200))
               finish = True
     display.update()
     clock.tick(FPS)
     