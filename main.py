import pygame
import sys
import math
from icecream import ic
import random


pygame.init()
pygame.font.init()
font = pygame.font.Font(None, 25)

size_window = (600,600)
screen = pygame.display.set_mode(size_window)
pygame.display.set_caption('ping pong')

class Player(pygame.sprite.Sprite):
    def __init__(self,x,y,width,height, speed):
        super().__init__()
        self.rect = pygame.rect.Rect(x,y,width,height)
        self.rect.center = x,y  
        self.speed = speed
        self.move_direction_top = False
        self.move_direction_down = False
        self.score = 0
        self.color_text = (255,255,255)
        self.color = (150,150,150)
        self.ry = 0
    def display_score(self, left,top):
        text = font.render(f"Score: {self.score}",True,self.color_text)
        text_rect = text.get_rect(left=left,top=top)
        screen.blit(text, text_rect) 
    def draw(self):
        pygame.draw.rect(screen,self.color, self.rect)
    def limit(self):
        if self.rect.top + self.ry < 0 :
            self.ry = 0 + self.rect.top    
        if self.rect.bottom + self.ry > size_window[1]:
            self.ry = size_window[1] - self.rect.bottom
        
    def update(self):
        
        self.limit()
        self.rect.centery += self.ry
        
    def move_top(self):
        self.ry = -self.speed
        
    def move_down(self):
        self.ry = self.speed
        
    def stop(self):
        self.ry = 0    
    
    def oponente_ia(self):
        if self.rect.centery < ball.rect.y:
            self.rect.centery += self.speed
        if self.rect.centery > ball.rect.y:
            self.rect.centery -= self.speed
            
        if self.rect.top <=0:
            self.rect.top= 0
        if self.rect.bottom >= 600:
            self.rect.bottom = 600
    
     
        
          
class Ball(pygame.sprite.Sprite):
    def __init__(self,x,y,width,height):
        super().__init__()
        self.radius = math.sqrt((width ** 2 + height ** 2) / 4)
        self.x = x
        self.y = y
        self.rect = pygame.rect.Rect(x,y,width,height)
        self.rect.center = x ,y
        self.speed_x = random.randint(3,8) * random.choice((-1,1))
        self.speed_y = random.randint(3,8) * random.choice((-1,1))
        
        self.color = (50,50,50)
        self.direction = 1
        # self.angle = 260
        self.quick = False
        self.add_score = True
        self.done = False
        self.cooldown = 25
        # self.score_time = pygame.time.get_ticks()
        self.last_update = pygame.time.get_ticks()
    def reset(self):
        if self.done:
            self.rect.center = self.x,self.y
            self.add_score = True
            self.speed_x = random.randint(3,8) * random.choice((-1,1))
            self.speed_y = random.randint(3,8) * random.choice((-1,1))
            self.done = False
    def draw(self):
        pygame.draw.circle(screen, self.color, (self.rect.centerx,self.rect.centery), self.radius)
    def collision(self,target):
        if self.rect.colliderect(target):
            if not self.quick:
                self.last_update = pygame.time.get_ticks()
                self.quick = True
                if abs(self.rect.left - target.rect.right) < self.radius or abs(self.rect.right - target.rect.left) < self.radius:
                    self.speed_x *= -1
                if abs(self.rect.bottom - target.rect.top) < self.radius or abs(self.rect.top - target.rect.bottom) < self.radius:
                    self.speed_y *= -1
            
    # def collision_limit(self):
    #     if abs(self.rect.top - 0) < self.radius or abs(self.rect.bottom - 600) < self.radius :
    #         if not self.quick:
    #             self.quick = True
    #             self.last_update = pygame.time.get_ticks()
    #             self.speed_y *= -1
    def limit(self):
        if self.rect.centery + self.radius <= 0 or self.rect.centery + self.radius >= size_window[1]:
            # if not self.quick:
            self.last_update = pygame.time.get_ticks()
            self.quick = True
            self.speed_y *= -1
   
    def tick_quick(self):
        current_update = pygame.time.get_ticks()
        if self.quick and current_update - self.last_update > self.cooldown : 
            self.last_update = pygame.time.get_ticks()
            # self.quick = False 
    def score(self,tg):
        tg.score += 10
        self.add_score = False
        self.done = True
    def update(self):
        ry = 0
        rx = 0
        
        rx = self.speed_x
        ry = self.speed_y 
        
        if self.add_score:
            if self.rect.left <= 0 - self.rect.width:
                self.score(enemie)
                
            if self.rect.right > 600 + self.rect.width:
                self.score(player)
        
        self.limit()
        
        self.collision(player)
        self.collision(enemie)
        
        self.tick_quick()
        
        self.rect.centerx += rx
        self.rect.centery += ry
  
    
# player settings        
x , y = 25 , size_window[1]//2 
width,height = 25, 200
player = Player(x,y,width,height , 10)

#enemy setting
x, y = size_window[0] - 25 , size_window[1]//2 
width,height = 25, 200
enemie = Player(x,y,width,height , 10)


# ball setting
centerx,centery = size_window[0] // 2, size_window[1] // 2
width_ball = 20
height_ball = 20
ball = Ball(centerx,centery , width_ball, height_ball)


#group
# ball_collection = pygame.sprite.Group()
# ball_collection.add(ball)
# score_time = True

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
         
    screen.fill((0,0,0))
    
    key = pygame.key.get_pressed()
    if key[pygame.K_w]:
        player.move_top()
    elif key[pygame.K_s]:
        player.move_down()
    else:
        player.stop()
    enemie.oponente_ia()
    # player.oponente_ia()
    
   
    player.display_score(20,20)
    enemie.display_score(size_window[1] - 100, 20)
    
   
    player.update()
    enemie.update()
    ball.update()    
    
    
    player.draw()
    enemie.draw()
    ball.draw()
    
    ball.reset()
        
    pygame.time.Clock().tick(60)
    pygame.display.flip()