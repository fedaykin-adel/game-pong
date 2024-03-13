import pygame 
import sys
import random
#inicia o pygame
pygame.init()

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
        self.dy = 0
        self.score = 0
        self.color_text = (255,255,255)
        #define a fonte do jogo, no caso estou usando a fonte padrão passando None como argumento
        self.font = pygame.font.Font(None, 25)
    def draw(self):
        pygame.draw.rect(screen,self.color,self.rect)
    def update(self,ball):
        #limite da classe player
        self.limit()

        #detecta colisão do player ou inimigo com a bola
        self.collide(ball)
        self.rect.centery += self.dy
    def move_top(self):
        self.dy = -self.speed
    def move_down(self):
        self.dy = self.speed
    def stop(self):
        self.dy = 0
    def limit(self):
        #aqui estamos prevendo a próxima posição antes de atualizar o jogo
        if self.rect.top + self.dy < 0:
            self.dy = self.rect.top
        if self.rect.bottom + self.dy > size[1]:
            self.dy = size[1] - self.rect.bottom
    def collide(self,ball):
        #detecta colisão
        if self.rect.colliderect(ball):
            #define o lado direito do jogador para colisão           #define o lado esquedo do inimido para colisão
            if abs(self.rect.right - ball.rect.left) < ball.radius or abs(self.rect.left - ball.rect.right) < ball.radius:
                ball.speed_x *= -1
    def enemy_ia(self,ball):
        #lógica para seguir a bola
        if self.rect.centery < ball.rect.y:
            self.rect.centery += self.speed
        if self.rect.centery > ball.rect.y:
            self.rect.centery -= self.speed
        
        #limite do inimigo para não atravessar a tela
        if self.rect.top <=0:
            self.rect.top= 0
        if self.rect.bottom >= size[1]:
            self.rect.bottom = size[1]
    def display_score(self, left,top):
        text = self.font.render(f"Score: {self.score}",True,self.color_text)
        text_rect = text.get_rect(left=left,top=top)
        screen.blit(text, text_rect)     
class Ball():
    def __init__(self, x,y,radius):
        self.radius = radius
        self.x = x
        self.y = y
        #cria o retângulo fora do circulo 
        self.rect = pygame.rect.Rect(self.x - self.radius,self.y- self.radius, 2 * self.radius,2 * self.radius)
        self.speed_y = 7 * random.choice((-1,1))
        self.speed_x = 7 * random.choice((-1,1))
        self.color = (50,50,50)
        self.add_score = True
        self.done = False
    def draw(self):
        pygame.draw.circle(screen, self.color, (self.rect.centerx, self.rect.centery), self.radius)
    def update(self):
        dx = 0
        dy = 0

        #limite da classe bola
        self.limit()
        
        dx = self.speed_x
        dy = self.speed_y

        self.rect.centerx += dx 
        self.rect.centery += dy
        
    def limit(self):
        if self.rect.top <= 0 or self.rect.bottom >= size[1]:
            self.speed_y *= -1
    def score(self,player, enemy):
        if self.add_score:
            #se a bola passar o lado do jogador, ponto do adversario
            if self.rect.left <= 0 - self.rect.width:
                enemy.score += 10
                self.add_score = False
                self.done = True
            #se a bola passar o lado do adversario, ponto do jogador
            if self.rect.right > 600 + self.rect.width:
                player.score += 10
                self.add_score = False
                self.done = True
    def reset(self):
        if self.done:
            self.rect.center = self.x,self.y
            self.add_score = True
            self.speed_x = 7 * random.choice((-1,1))
            self.speed_y = 7 * random.choice((-1,1))
            self.done = False  

#centro da tela para desenhar a bola
centerx,centery = size[0] // 2, size[1] // 2

#tamanho da bola
radius = 15

#classe da bola
ball = Ball(centerx,centery, radius)
    
# tamanho do player e do inimigo e a velocidade de ambos
width = 15
height = 200
speed = 10

#posição inicial do jogador
x = 25
y = size[1] // 2

#classe do player
player = Player(x,y,width,height,speed)

#posição inicial do adversário
x = size[0] - 25
y = size[1] // 2

#classe do adversário
enemy = Player(x,y,width,height,speed)

#motor de processamento
run = True
while run:
    #preenche a tela a cada quadro
    screen.fill((0,0,0))
    
    #detecção de eventos
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            #sai do loop principal 
            run = False
    

    #detecta tecla pressionada
    key = pygame.key.get_pressed()
    if key[pygame.K_w]:
        #caso pressionado a tecla w, o jogador e movido para cima
        player.move_top()
    elif key[pygame.K_s]:
        #caso pressionado a tecla s, o jogador e movido para baixo
        player.move_down()
    else:
        #caso nenhuma tecla esteja sendo pressionada, o personagem fica parado
        player.stop()
    #adiciona score quando houver ponto
    ball.score(player, enemy)
    
    #ai enemy
    enemy.enemy_ia(ball)
    
    #mostrando o score passando a posição do placar
    player.display_score(20,20)
    enemy.display_score(size[1] - 100, 20)
    
    #update 
    player.update(ball)
    enemy.update(ball)
    ball.update()

    #draw
    player.draw()
    enemy.draw()
    ball.draw()
    
    #reset game
    ball.reset()
    
    #relógio para controle de fps
    pygame.time.Clock().tick(60)
    #atualiza a tela. 
    pygame.display.flip()
#encerra a aplicação
pygame.quit()
sys.exit()