
# Indice
* [Basico](#basico)
* [Classe player](#Classe-player)
* [Classe bola](#classe-bola)
* [Limites](#limites)
* [Colissão](#colissão)
* [Ia oponente](#ia-oponente)
* [Direção aleatoria](#direção-aleatoria)
* [Score](#score)
* [Reset game](#reset-game)
* [font e placar](#font-e-placar)

Nesse tutorial vamos criar um jogo antigo chamdo pong.... 


Para começar vamos  biaxar o pygame

```bash
    pip install pygame
```

# Basico 
a estrutura simplificada da tela do jogo sera esta: 

```python{.line-numbers}
    import pygame 
    import sys
    #inicia o pygame
    pygame.init()

    #cria a tela e seta o tamanho no caso 600x600
    size = (600,600)
    screen = pygame.display.set_mode(size)
    
    #title
    pygame.display.set_caption('game pong')

    #motor de processamento
    run = True
    while run:
        #detecção de eventos
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                #sai do loop principal 
                run = False
    
    #encerra a aplicação
    pygame.quit()
    sys.exit()
```

# Classe player
Em seguida vamos criar o nosso jogador, para isso eu criei uma classe chamada player para ficar mais organizado, tambem criei uma classe para a bola mas por enquanto vamos focar no player. 
Para o player vou cirar uma classe passando posição x,y, algura, largura e velocidade, nada muito complicado. Tambem vou centarlizar o retangulo com rect.center 

```python{.line-numbers}
    class Player():
        def __init__(self,x,y,width,height, speed):
            self.rect = pygame.rect.Rect(x,y,width,height)
            self.rect.center = x,y
            self.speed = speed
            self.color = (150,150,150)
            self.dy = 0
```
Como so iremos mover o personagem para cima e para baixo, vou criar apenas um controlador de eixo, no caso estou criando o dy (leia delta y).

Agora cirar algumas funções dentro da classe player, elas serão responsaveis por desenhar, mover e atualizar o personagem. 

```python{.line-numbers}
    class Player():
        def __init__(self,x,y,width,height, speed):
            self.rect = pygame.rect.Rect(x,y,width,height)
            self.rect.center = x,y
            self.speed = speed
            self.color = (150,150,150)
            self.dy = 0
        def draw(self):
            pass
        def update(self):
            pass
        def move_top(self):
            pass
        def move_down(self):
            pass     
        def stop(self):
            pass    
```

Começando pelo desenho do personagem, vou utilizar a função draw do pygame.

```python{.line-numbers}
    def draw(self):
        pygame.draw.rect(screen,self.color,self.rect)
```

Para desenhar, temos que passar para a função draw.rect a tela (screen) que define em qual tela vai ser desenhado, a cor, e a posição x, y, altua e largura, mas voce pode simplesmente passar o parametro rect. 

Para o movimento, vamos ter algo assim

```python{.line-numbers}
    def update(self):
        
        self.rect.centery += self.dy
    def move_top(self):
        self.dy = -self.speed
    def move_down(self):
        self.dy = self.speed
    def stop(self):
        self.dy = 0
```
Para implementar a logica de movimento, estou atualizando a posição centery do rect do player somando delta y, para o movimento para cima estou negativando a variavel speed e para o movimento para baixo estou apenas atribuindo a velocidade, como eu estou lidando com atualizaçao constante fui obrigado a implementar uma função chamada stop que define o controlador de eixo dy como 0. 

# Classe bola

```python{.line-numbers}
    class Ball():
        def __init__(self, x,y,radius):
            self.radius = radius
            self.x = x
            self.y = y
            self.rect = pygame.rect.Rect(self.x - self.radius,self.y- self.radius, 2 * self.radius,2 * self.radius)
            self.speed_y = 7
            self.speed_x = 7
            self.color = (50,50,50)
        def draw(self):
            pass
        def update(self):
            pass
```
Alguns pontos importantes aqui... diferente do player que a velocidade inicial e 0, na bola eu ja setei ela com uma velocidade inicial de 7 pixels. Tambem estou criando um rect para facilitar a movimentação e colisão, em uma situação normal, ao criar um rect para a esfera ela ficaria dentro da esfera, mas para facilitar a minha vida estou criando o retangulo por fora da esfera multiplicando o raio dela por 2.

agora, na logica do desenho e da atualização, temos algo com isso.
```python{.line-numbers}
    def draw(self):
        pygame.draw.circle(screen, self.color, (self.rect.centerx, self.rect.centery), self.radius)
    def update(self):
        dx = 0
        dy = 0

        dx = self.speed_x
        dy = self.speed_y

        self.rect.centerx += dx 
        self.rect.centery += dy
```

Para desenhar a bola, estou usando a função draw.circle passando o parametro da posição separado de x e y e o paramentro do raio do circulo. 
Para a atualização da bola estou definindo dx e dy como estado inicial 0 e em seguida atribuindo o valor da velocidade no respectivo eixo, depois movendo o centro da bola x e y com o controlador de posição dx e dy.

Com isso podemos declarar as classes bola, personagem e inimigo. 

```python{.line-numbers}
    ...codigo anterior...
    pygame.display.set_caption('ping pong')
    class Player():
        ...resto do codigo player...
    class Ball():
        ...resto do codigo da bola...

    #centro da tela para desenhar a bola
    centerx,centery = size[0] // 2, size[1] // 2

    #tamanho da bola
    radius = 15

    #classe da bola
    ball = Ball(centerx,centery, radius)
        
    # tamanho do player e do inimigo e a velocidade de ambos
    width = 25
    height = 200
    speed = 10

    #posição inicial do jogador
    x = 25
    y = size[1] // 2
    
    #classe do player
    player = Player(x,y,width,height,speed)

    #posição inicial do adversario
    x = size[0] - 25
    y = size[1] // 2
    
    #classe do adversario
    enemie = Player(x,y,width,height,speed)


    #motor de renderização
    run = True
    while run:
        ...restante do codigo... 
    
```

Instanciei as classes necessarias antes do meu loop principal, assim so precisamos declarar elas uma vez. Detalhando um pouco, na classe da bola, eu setei a poxição x e y no centro da tela e declarei o raio da esfera como 15, enquanto o jogador eu setei no eixo x 25 pixels para a direita e centralizado no eixo y, fiz a mesma coisa com o jogador adversario espelhando para o lado direito da tela, como o tamanho do jogador e do inimigo são os mesmos, criei o mesmo paramentro para os dois. 

agora, juntando tudo no nosso loop principal, teremos algo como isso


```python{.line-numbers}
    ...codigo anteriro
    run = True
    while run:
        #detecção de eventos
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
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

        #update 
        player.update()
        enemie.update()
        ball.update()

        #draw
        player.draw()
        enemie.draw()
        ball.draw()

```
Adicionei o movimento do jogador no nosso motor de renderização, para isso usei a função get_pressed do pygame para detectar a tecla pressionada e mover de acordo com o que queremos. Logo em seguida eu defino os updates necessarios e os desenhos necessarios.

Pronto... agora, se voce iniciar o jogo apenas com isso, tudo o que voce vera sera uma tela preta... por que? Como estamos lidando com um loop infinito ele percorre e renderiza muito rapido, então vamos adicionar um relogio que sera o controle da quantidade de quadros por segundo (fps) que seram exibidos junto com a função de atualização do pygame, a função flip, isso tudo dentro do nosso loop principal, o codigo fica assim... 

```python{.line-numbers}
    ...codigo anteriro
    run = True
    while run:
        #detecção de eventos
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        #detecta tecla pressionada
        key = pygame.key.get_pressed()
        if key[pygame.K_w]:
            player.move_top()
        elif key[pygame.K_s]:
            player.move_down()
        else:
            player.stop()

        #update 
        player.update()
        enemie.update()
        ball.update()

        #draw
        player.draw()
        enemie.draw()
        ball.draw()
        
        #relogio para controle de fps
        pygame.time.Clock().tick(60)
        #atualiza a tela. 
        pygame.display.flip()
```
Se executarmos o codigo agora, você notara que os objetos estão se movendo mas com outro erro, ele acontece por que não estamos limpando a tela a cada frame então o computador apenas copia e coloca o objeto para a nova posição mas permanece com a posição antiga, para arrumar isso e simples, basta acidionar essa linha antes da detecção de tecla. 

```python{.line-numbers}
    screen.fill((0,0,0))

    key = pygame.key.get_pressed()
    if key[pygame.K_w]:
        player.move_top()
    elif key[pygame.K_s]:
        player.move_down()
    else:
        player.stop()
```

Basicamente a cada freme ele preenche a tela com a cor preta apagando o ultimo estado da bola. 

Certo, agora nos temos um jogo quase funcional, mas se voce reparar o jogador esta atravessando a area visivel da tela e a bola a mesma coisa, para isso iremos implementar alguns limites e em seguida as colisões. 

# limites
Para começar o limite, precisamos entender um pouco da regra do jogo pong original.
Na versão original as areas do top e do chão são considerados como "parede" e nada passa por cima ou por baixo, para isso vamos implementar na nossa classe do jogador e da bola os limites da tela.
Vamos começar pelo jogador
```python{.line-numbers}
    def limit(self):
        #aqui estamos prevendo a proxima posição antes de atualizar o jogo
        if self.rect.top + self.dy < 0:
            self.dy = self.rect.top
        if self.rect.bottom + self.dy > size[1]:
            self.dy = size[1] - self.rect.bottom
```
O limite e simples... caso o topo do jogagor mais o delta y for menor do que 0, ele posiciona o jogador como o topo do jogador, ja para o limite inferior e a mesma logica, se a area de baixo do jogador passar o tamanho da altura da tela, ele define a posição como o limite da altura da tela a parte inferior do jogador, vamos aplicar uma logica semelhate para a bola. 

Na classe da bola, vamos adicionar o limite
```python{.line-numbers}
    def limit(self):
        if self.rect.top <= 0 or self.rect.bottom >= size[1]:
            self.speed_y *= -1
```
A logica do limite da bola e mais simples, so precisamos verificar a parte superior da esfera for menor que zero ou a parte inferior da esfera for maior do que o tamanho da tela ele inverte a velocidade, fazendo a bola ir para o lado contrario. Com as funções construidas, so precisamos adicionar a função do limite nos respectivos updates, segue o exemplo

```python{.line-numbers}
    #limite da classe player
    def update(self):
        self.limit()
        self.rect.centery += self.ry
```

```python{.line-numbers}
    #limite da classe bola
    def update(self):
        rx = 0
        ry = 0

        self.limit()
        rx = self.speed_x
        ry = self.speed_y

        self.rect.centerx += rx 
        self.rect.centery += ry
```

# Colissão
Bom, chegou a parte da colisão entre objetos, para isso vou utilizar colliderect do pygame, a implementação e simples, e funciona assim, usando o rect do personagem vou aplicando a colisão com o objeto da bola, que retorna um booleano, logo so precisamos colocar em dentro de um if e quando ocorrer a colissão revertemos a direção da bola, dessa vez no eixo x.

```python{.line-numbers}
    #função da colisão do player
    def collide(self,ball):
        if self.rect.colliderect(ball):
            if abs(self.rect.right - ball.rect.left) < ball.radius or abs(self.rect.left - ball.rect.right) < ball.radius:
                ball.speed_x *= -1
```
Agora basta implementar a função no update player passando o objeto da bola como paramentro, tambem precisamos passar a bola no update do personagem e no inimigo no loop principal. 

```python{.line-numbers}
    #update player
    def update(self,ball):
        self.limit()
        self.collide(ball)
        self.rect.centery += self.ry
```
```python{.line-numbers} 
    key = pygame.key.get_pressed()
    if key[pygame.K_w]:
        player.move_top()
    elif key[pygame.K_s]:
        player.move_down()
    else:
        player.stop()
    
    #update passando a bola como paramentro para inimigo e o personagem
    player.update(ball)
    enemie.update(ball)
    ball.update()

    #draw
    player.draw()
    enemie.draw()
    ball.draw()      
```
Como estamos fazendo tudo no mesmo arquivo, eu não precisaria passar como parametro no player.update a bola, mas estou fazendo isso para ficar mais organizado caso você decida separar as classes player e a bola em outro arquivo.

# Ia oponente
Agora para a logica do controle do oponente, eu decidi deixar o jogo um pouco mais dificil que o normal, então estou usando o centro Y do oponente e comparando com a cordenada y da bola, dessa forma fazemos o oponente so seguir a bola para onde ela for. Tambem precisamos adicionar o limite do oponente para não atravessar a tela. 

```python{.line-numbers}
    def oponente_ia(self,ball):
        #logica para seguir a bola
        if self.rect.centery < ball.rect.y:
            self.rect.centery += self.speed
        if self.rect.centery > ball.rect.y:
            self.rect.centery -= self.speed
        
        #limite do inimigo para não atravessar a tela
        if self.rect.top <=0:
            self.rect.top= 0
        if self.rect.bottom >= size[1]:
            self.rect.bottom = size[1]
            
```
depois so precisamos declarar a função no nosso loop principal passando a bola com oparametro 

```python{.line-numbers}
    key = pygame.key.get_pressed()
    if key[pygame.K_w]:
        player.move_top()
    elif key[pygame.K_s]:
        player.move_down()
    else:
        player.stop()
    
    #ai enemie
    enemie.oponente_ia(ball)
    
    #update 
    player.update(ball)
    enemie.update(ball)
    ball.update()
```
Temos um jogo funcional agora :3
# Direção aleatoria
 Mas vamos fazer algumas pequenas modificacoes para adicionar algumas coisas, vamos começar coma a direção aleatoria da bola no inicio do jogo. Para isso vamos importar a biblioteca random, a logica e que quando o jogo inicia ele escolha randomicamente a direção que a bola vai seguir, para o player ou para o inimigo. Pra isso so precisamos multiplucar a velocidade x e y pela escolha aleatoria em -1,1 

```python{.line-numbers}
    import random
    class Ball():
        def __init__(self, x,y,radius):
            self.radius = radius
            self.x = x
            self.y = y
            self.rect = pygame.rect.Rect(self.x - self.radius,self.y- self.radius, 2 * self.radius,2 * self.radius)
            self.speed_y = 7 * random.choice((-1,1))
            self.speed_x = 7 * random.choice((-1,1))
            self.direction = 1
            self.color = (50,50,50)
```

# Score
Para o sistema de pontos vamos entender a regra do jogo de novo, caso a bola passe a linha de visao do jogador, o ponto e do adversario, caso a bola passe pelo adversaio o ponto e do jogador, simples e rapido, podemos escrever algo assim:

```python{.line-numbers}
    class Ball():
        def __init__(self, x,y,radius):
            ...inits anteriores...
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

    
```
Adicionei um booleano, add_score, que ficara responsavel para que o score seja adicionado panas uma vez, como estamos chamando ele na função update e caso não tivesse essa variavel o contador de pontos iria a loucura. 
Depois disso so precisamos adicionar a função score no nosso loop principal passando como parametro o objeto do jogador e do inimigo

```python{.line-numbers}
    key = pygame.key.get_pressed()
    if key[pygame.K_w]:
        player.move_top()
    elif key[pygame.K_s]:
        player.move_down()
    else:
        player.stop()
    
    #adiciona score quando houver ponto
    ball.score(player, enemie)
    
    #ai enemie
    enemie.oponente_ia(ball)
    
    #update 
    player.update(ball)
    enemie.update(ball)
    ball.update()

```
Tambem e preciso adicionar score ao player. 

```python{.line-numbers}
    class Player():
        def __init__(self,x,y,width,height, speed):
            self.rect = pygame.rect.Rect(x,y,width,height)
            self.rect.center = x,y
            self.speed = speed
            self.color = (150,150,150)
            self.ry = 0
            self.score = 0
```

# Reset game
A logica para resetar o jogo e simples e vamos adicionar na nossa classe bola 

```python{.line-numbers}
    def reset(self):
        if self.done:
            self.rect.center = self.x,self.y
            self.add_score = True
            self.speed_x = 7 * random.choice((-1,1))
            self.speed_y = 7 * random.choice((-1,1))
            self.done = False
```
Caso o done retorne um true, ele define a posição inicial de volta para o centro, seto o add_score para true para voltar a contar os pontos, e defino um novo angulo para a bola com speed random -1 e 1, tambem precisamos setar o done para false. Feito isso e so implementar no nosso motor de renderização e taram, um jogo que numca acaba. 


```python{.line-numbers} 
    key = pygame.key.get_pressed()
    if key[pygame.K_w]:
        player.move_top()
    elif key[pygame.K_s]:
        player.move_down()
    else:
        player.stop()
    
    #ai enemie
    enemie.oponente_ia(ball)
    
    #update passando a bola como paramentro para inimigo e o personagem
    player.update(ball)
    enemie.update(ball)
    ball.update()

    #draw
    player.draw()
    enemie.draw()
    ball.draw()    

    #reset game
    ball.reset()  
```

# Font e placar
Mas... onde está o placar? bom... para isso vamos precisar implementar uma font no pygame, vamos fazer algumas modificalções.

```python{.line-numbers}
    pygame.init()
    pygame.font.init()

    
    class Player(pygame.sprite.Sprite):
    def __init__(self,x,y,width,height, speed):
        ...resto do init...
        self.color = (150,150,150)
        self.ry = 0
        self.color_text = (255,255,255)
        #define a fonte do jogo, no caso estou usando a fonte padrão passando None como argumento
        self.font = pygame.font.Font(None, 25)
    def display_score(self, left,top):
        text = self.font.render(f"Score: {self.score}",True,self.color_text)
        text_rect = text.get_rect(left=left,top=top)
        screen.blit(text, text_rect) 
    

```
Para implementar a fonte, precisando usar a função font do pygame e passar o tipo de font que quer usar e o tamanho, no meu caso vou usar a fonte padram, mas caso queira usar outra fonte e so baixar o arquivo e insesir aqui, tambem estou definindo a cor do texto como branco.  

Depois disso precisamos renderizar o que queremos que seja escrito na tela, então chamamos a função font.render passando o texto, cor e logo em seguida definimos a posição do texto, por fim nos usamos a função blit na tela do jogo passando o texto que criamos e a posição rect.

Depois disso vamos adicionar o display score do player e do adversario no loop principal, passando a posição que queremos que o texto seja exibido, no meu caso estou exibindo o placar nos cantos superiores.

```python{.line-numbers} 
    key = pygame.key.get_pressed()
    if key[pygame.K_w]:
        player.move_top()
    elif key[pygame.K_s]:
        player.move_down()
    else:
        player.stop()
    
    #ai enemie
    enemie.oponente_ia(ball)
    
    #mostrando o score
    player.display_score(20,20)
    enemie.display_score(size[1] - 100, 20)
    

    #update passando a bola como paramentro para inimigo e o personagem
    player.update(ball)
    enemie.update(ball)
    ball.update()

    #draw
    player.draw()
    enemie.draw()
    ball.draw()    

    #reset game
    ball.reset()  
```

Pronto, o jogo esta completo, sinta-se livre para mexer e customizar o jogo, não me preocupei no estilo do jogo pois não era o foco. 