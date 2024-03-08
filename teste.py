import pygame 
import sys
import random
#inicia o pygame
pygame.init()
pygame.font.init()

#cria a tela e seta o tamanho no caso 600x600
size = (600,600)
screen = pygame.display.set_mode(size)

#title
pygame.display.set_caption('game pong')

class Player():
    def __init__(self,x,y,width,height, speed):
        self.rect = pygame.rect.Rect(x,y,width,height)
        self.rect.center = x,y
        self.speed = speed
        self.color = (150,150,150)
        self.ry = 0
        self.score = 0
        self.color_text = (255,255,255)
        self.font = pygame.font.Font(None, 25)
    def display_score(self, left,top):
        text = self.font.render(f"Score: {self.score}",True,self.color_text)
        text_rect = text.get_rect(left=left,top=top)
        screen.blit(text, text_rect) 
    def draw(self):
        pygame.draw.rect(screen,self.color,self.rect)
    def update(self,ball):
        self.limit()
        self.collide(ball)
        self.rect.centery += self.ry
    def move_top(self):
        self.ry = -self.speed
    def move_down(self):
        self.ry = self.speed
    def stop(self):
        self.ry = 0
    def limit(self):
        if self.rect.top + self.ry < 0:
            self.ry = 0 + self.rect.top
        if self.rect.bottom + self.ry > size[1]:
            self.ry = size[1] - self.rect.bottom
    def stop(self):
        self.ry = 0    
    def collide(self,ball):
        if self.rect.colliderect(ball):
            if abs(self.rect.right - ball.rect.left) < ball.radius or abs(self.rect.left - ball.rect.right) < ball.radius:
                ball.speed_x *= -1
            
        # if abs(self.rect.bottom - ball.rect.top) < ball.radius or abs(self.rect.top - ball.rect.bottom) < ball.radius:
        #     ball.speed_y *= -1
    def oponente_ia(self,ball):
        
        if self.rect.centery < ball.rect.y:
            self.rect.centery += self.speed
        if self.rect.centery > ball.rect.y:
            self.rect.centery -= self.speed

        if self.rect.top <=0:
            self.rect.top= 0
        if self.rect.bottom >= size[1]:
            self.rect.bottom = size[1]
    
class Ball():
    def __init__(self, x,y,radios):
        self.radius = radios
        self.x = x
        self.y = y
        self.rect = pygame.rect.Rect(self.x - self.radius,self.y- self.radius, 2 * self.radius,2 * self.radius)
        self.speed_y = 7 * random.choice((-1,1))
        self.speed_x = 7 * random.choice((-1,1))
        # self.direction = 1   
        self.color =( 50,50,50)
        self.add_score = True
        self.done = False
    def score(self,player, enemie):
        if self.add_score:
            if self.rect.left <= 0 - self.rect.width:
                enemie.score += 10
                self.add_score = False
                self.done = True
                
            if self.rect.right > 600 + self.rect.width:
                player.score += 10
                self.add_score = False
                self.done = True
    def draw(self):
        pygame.draw.circle(screen, self.color, (self.rect.centerx, self.rect.centery), self.radius)
        
    def limit(self):
        if self.rect.top <= 0 or self.rect.bottom >= size[1]:
            self.speed_y *= -1
    def reset(self):
        if self.done:
            self.rect.center = self.x,self.y
            self.add_score = True
            self.speed_x = 7 * random.choice((-1,1))
            self.speed_y = 7 * random.choice((-1,1))
            self.done = False
    def update(self,player, enemie):
        rx = 0
        ry = 0

        self.score(player, enemie)
        self.limit()
        
        rx = self.speed_x
        ry = self.speed_y
        
        self.rect.centerx += rx 
        self.rect.centery += ry

#difinindo o centro da tela para desenhar a bola
centerx,centery = size[0] // 2, size[1] // 2
#definir o tamanho da bola
radius = 15

#classe da bola
ball = Ball(centerx,centery, radius)

# tamanho do player e do inimigo.
width = 10
height = 200
speed = 10

#defini posição inicial 
x = 25
y = size[1] // 2


#classe do player
player = Player(x,y,width,height,speed)

#defini posição inicial do jogador adversario
x = size[0] - 25
y = size[1] // 2

#classe do player
enemie = Player(x,y,width,height,speed)
        
#motor de processamento
run = True
while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
    
    
    screen.fill((0,0,0))
    
    key = pygame.key.get_pressed()
    if key[pygame.K_w]:
        player.move_top()
    elif key[pygame.K_s]:
        player.move_down()
    else:
        player.stop()
    
    #ai enemie
    enemie.oponente_ia(ball)
    
    player.display_score(20,20)
    enemie.display_score(size[1] - 100, 20)
    
    #update 
    player.update(ball)
    enemie.update(ball)
    ball.update(player,enemie)

    #draw
    player.draw()
    enemie.draw()
    ball.draw()      

    ball.reset()
    #relogio para controle de fps
    pygame.time.Clock().tick(60)
    #atualiza a tela. 
    pygame.display.flip()
    
#sai do pygame e fecha a tela
pygame.quit()
sys.exit()