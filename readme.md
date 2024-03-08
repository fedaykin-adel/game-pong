Nesse tutorial vamos criar um jogo antigo de pong.... 

Para começar vamos criar a estrutura usando pygame, para biaxar o pygame o comando e 

```python
    pip install pygame
```
[Limites](#limites)
# Basico #
a estrutura simplificada da tela do jogo sera esta: 

```python
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

# Inicio classe player
Em seguida vamos criar o nosso player, para criar o player eu criei uma classe chamada player para ficar mais organizado, tambem criei uma classe para a bola mas por enquanto vamos focar no player. 
Para o player vou cirar uma classe passando posição x,y, algura, largura e velocidade, nada muito complicado. Tambem vou centarlizar o retangulo com rect.center 

```python
    class Player():
        def __init__(self,x,y,width,height, speed):
            self.rect = pygame.rect.Rect(x,y,width,height)
            self.rect.center = x,y
            self.speed = speed
            self.color = (150,150,150)
            self.ry = 0
```
Como so iremos mover o personagem para cima e para baixo, vou criar apenas um controlador de eixo, no caso estou criando o ry.

Agora cirar algumas funções dentro da classe player, elas serão responsaveis por desenhar, mover e atualizar o personagem. 

```python
    class Player():
        def __init__(self,x,y,width,height, speed):
            self.rect = pygame.rect.Rect(x,y,width,height)
            self.rect.center = x,y
            self.speed = speed
            self.color = (150,150,150)
            self.ry = 0
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

Bom.. vamos começar por desenhar o personagem, para o desenho vou utilizar a função draw do pygame que ficaria assim 

```python
    def draw(self):
        pygame.draw.rect(screen,self.color,self.rect)
```

Para desenhar, temos que passar para a função draw.rect a tela (screen) que define em qual tela vai ser desenhado, a cor, e a posição x e y, altua e largura, mas voce pode simplesmente passar o parametro self.rect e o pygame ja vai pegar automaticamente a posição do player. 

para implementar o movimento, vamos ter algo assim

```python
    def update(self):
        
        self.rect.centery += self.ry
    def move_top(self):
        self.ry = -self.speed
    def move_down(self):
        self.ry = self.speed
    def stop(self):
        self.ry = 0
```
Para implementar a logica de movimento, estou atualizando a posição centery do rect do player, para movimentar para cima estou negativando a variavel speed e para o movimento para baixo estou apenas passando a velocidade, como eu estou lidando com atualizaçao constante fui obrigado a implementar uma função chamada stop que define o controlador de eixo ry como 0. 

# Inicio da classe Bola

```python
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
Alguns pontos importantes aqui... diferente do player que a velocidade inicial e 0, na bola eu ja setei ela com uma velocidade inicial de 7 pixels. Tambem estou criando um rect para a bola por que facilita na hora de aplicar a logida de movimento e do desenho, em uma situação normal ao criar um rect para a esfera ela ficaria dentro da bola, mas para facilitar a minha vida estou criando o retangulo por fora da esfera multiplicando o raio dela por 2.

agora, na logica do desenho e da atualização, temos algo com isso.
```python
    def draw(self):
        pygame.draw.circle(screen, self.color, (self.rect.centerx, self.rect.centery), self.radius)
    def update(self):
        rx = 0
        ry = 0

        rx = self.speed_x
        ry = self.speed_y

        self.rect.centerx += rx 
        self.rect.centery += ry
```

Para desenhar a bola, estou usando a função draw.circle passando o parametro da posição separado de x e y e com o paramentro do raio do circulo. Para a atualização da bola estou definindo rx e ry como estado inicial 0 e logo em seguida atribuindo o valor da velocidade no respectivo eixo e logo depois movendo o centro da bola x e y com o controlador de posição rx e ry.

com isso podemos declarar as classes bola, personagem e inimigo. 

```python
    ...codigo anterior...
    pygame.display.set_caption('ping pong')
    class Player():
        ...resto do codigo player...
    class Ball():
        ...resto do codigo da bola...

    #difinindo o centro da tela para desenhar a bola
    centerx,centery = size[0] // 2, size[1] // 2

    #definir o tamanho da bola
    radius = 15

    #classe da bola
    ball = Ball(centerx,centery, radius)
        
    # tamanho do player e do inimigo e a velocidade de ambos
    width = 25
    height = 200
    speed = 10
    #defini posição inicial do jogador
    x = 25
    y = size[1] // 2
    
    #classe do player
    player = Player(x,y,width,height,speed)

    #defini posição inicial do adversario
    x = size[0] - 25
    y = size[1] // 2
    
    #classe do adversario
    enemie = Player(x,y,width,height,speed)


    #motor de renderização
    run = True
    while run:
        ...restante do codigo... 
    
```

Bom... declarei antes do meu loop principal e logo em seguida das classes. Começando pela bola, eu setei a poxição x e y no centro da tela e declarei o raio da esfera como 15, enquanto o jogador eu setei no eixo x 25 pixels para a direita e centralizado no eixo y, fiz a mesma coisa com o jogador adversario espelhando para o lado direito da tela, como o tamanho do jogador e do inimigo são os mesmos, criei o mesmo paramentro para os dois. 

agora, juntando tudo no nosso loop principal, teremos algo como isso


```python
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
tambem adicionei o movimento do jogador no nosso motor de renderização, para isso usei a função get_pressed do pygame para detectar a tecla pressionada e mover de acordo com o que queremos 

pronto, agora se voce iniciar o jogo apenas com isso, tudo o que voce vera sera uma tela preta... por que? Como estamos lidando com um loop infinito ele percorre e renderiza muito rapido, então vamos adicionar um relogio que controla-ra a quantidade de quadros por segundo (fps) que seram exibidos junto com a função de atualização do pygame o flip, isso tudo dentro do nosso loop principal, o codigo fica assim... 

```python
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
Se executarmos o codigo agora, notaremos que os objetos estão se movendo mas com outro erro, ele acontece por que não estamos limpando a tela a cada frame então o computador apenas copia e coloca o objeto para a nova posição mas permanece com a posição antiga, para arrumar isso e simples, basta acidionar essa linha antes da detecção de tecla. 

```python
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

Certo, agora nos temos um jogo quase funcional, mas se voce reparar o jogador esta atravessando a area visivel da tela e a bola a mesma coisa, para isso iremos implementar alguns limites e colisões. 

# limites #
Para começar o limite, precisamos entender um pouco da regra do jogo pong original.
Na versão original as areas do top e do chão são considerados como "parede" e nada passa por cima ou por baixo, para isso vamos implementar na nossa classe do jogador e da bola os limites da tela.
Vamos começar pelo jogador
```python
    def limit(self):
        #aqui estamos prevendo a proxima posição antes de atualizar o jogo
        if self.rect.top + self.ry < 0:
            self.ry = 0 + self.rect.top
        if self.rect.bottom + self.ry > size[1]:
            self.ry = size[1] - self.rect.bottom
```
O limite e simples... caso o topo do jogagor mais o controle de posição ry for mais do que 0, ele posiciona o jogador como 0 + topo do jogador, ja para o limite inferior e a mesma logica, se a area de baixo do jogador passar o tamanho da altura da tela, ele define a posição como o limite da altura da tela menos a area de baixo do jogador, vamos aplicar uma logica semelhate para a bola. 
Na classe da bola, vamos adicionar o limite
```python
    def limit(self):
        if self.rect.top <= 0 or self.rect.bottom >= size[1]:
            self.speed_y *= -1
```

A logica do limite da bola para não atravessar o topo ou o fundo da tela e mais simples, so precisamos adicionar o limite do topo da bola com o limite maior ou igual que zero que e no fundo, a base da bola seja menor do que o tamanho da altura da tela, quando atingir qualquer um dos limites ele inverte a velocidade fazendo a bola ir para o lado contrario, desse jeito temos a logica de limite implementado para ambas as classes. vamos implementar o limite nas respectivas classes update, limite do player na classe update player e a bola no update bola 

```python
    def update(self):
        self.limit()
        self.rect.centery += self.ry
```

```python
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
Bom, chegou a parte da colisao entre objetos, para isso vou utilizar colliderect do pygame, a implementação e simples, e basicamente funciona assim, usando o rect do personagem vou aplicando a colisao com o objeto da bola, que retorna um booleano, logo so precisamos colocar em dentro de um if e quando ocorrer a colissão revertemos a direção da bola.

```python
    def collide(self,ball):
        if self.rect.colliderect(ball):
            if abs(self.rect.right - ball.rect.left) < ball.radius or abs(self.rect.left - ball.rect.right) < ball.radius:
                ball.speed_x *= -1
```
basta implementar a função do update player passando a bola como paramentro, tambem precisamos passar a bola no update do personagem e no inimigo no loop principal. 

```python
    def update(self,ball):
        self.limit()
        self.collide(ball)
        self.rect.centery += self.ry
```
```python 
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

# Ia oponente
Agora vamos criar a logica do oponente, basicamente vamos pegar o topo e o fundo do personagem e comparar com as cordenadas y da bola, se a bola passar algum dessas pontos, o jogador adversario se move seguindo a bola, tambem temo que declarar um limite para a movimentação do nosso oponemte, tudo o que precisamos criar uma pequena logica para criar um limite igual fizemos com o jogador.
```
    def oponente_ia(self,ball):
        if self.rect.centery < ball.rect.y:
            self.rect.centery += self.speed
        if self.rect.centery > ball.rect.y:
            self.rect.centery -= self.speed
        
        if self.rect.top <=0:
            self.rect.top= 0
        if self.rect.bottom >= size[1]:
            self.rect.bottom = size[1]
            
```
depois so precisamos declarar a função no nosso loop principal passando a bola com oparametro 

```python
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

# Direção da bola inicial aleatorio
Temos um jogo funcional agora :3 mas vamos fazer algumas pequenas modificacoes para adicionar algumas coisas, vamos começar coma a direção aleatoria da bola no inicio do jogo. importando a biblioteca random, vamos fazer uma logica que quando o jogo e iniciado ele escolha randomicamente a direção que a bola vai seguir, para o player ou para o inimigo. 

```python
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
Para o sistema de pontos vamos entender a regra do jogo de novo, caso a bola passe a linha de visao do jogador, o ponto e do adversario, caso a bola passe pelo adversaio o ponto e do jogador, simples e rapido, podemos escrever algo assim. e para não perder muito tempo junto com o score, vou adcionar um booleano que ficara responsavel por resetar a partida toda vez que alguem fizer um ponto.

```python
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

    def update(self,player, enemie):
        rx = 0
        ry = 0

        self.score(player, enemie)
        self.limit()
        rx = self.speed_x
        ry = self.speed_y

        self.rect.centerx += rx 
        self.rect.centery += ry
    
```
Adicionei um booleano, add_score, que ficara responsavel por dispara o score aprenas uma vez, como estamos chamando ele na função update e caso não tivesse essa variavel o contador de pontos iria a loucura, e no nosso loop principal, so precisamos passar em ball.update as variaveis player e enemie

```python
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
    ball.update(player,enemie)

```
Tambem e preciso adicionar score ao player. 

```python
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

```python
    def reset(self):
        if self.done:
            self.rect.center = self.x,self.y
            self.add_score = True
            self.speed_x = 7 * random.choice((-1,1))
            self.speed_y = 7 * random.choice((-1,1))
            self.done = False
```
Caso o done retorne um true, ele define a posição inicial de volta para o centro, seto o add_score para true para voltar a contar os pontos, e defino um novo angulo para a bola com speed random -1,1, tambem precisamos setar o done para false. feito isso e so implementar no nosso loop principal e taram, um jogo que numca acaba. 


```python 
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

# font e placar
Mas... onde está o placar? bom... para isso vamos precisar implementar uma font no pygame, para isso vamos fazer algumas modificalções, para simplificar vou implementar essa parte toda de uma vez e depois explicar.

```python
    pygame.init()
    pygame.font.init()

    

    class Player(pygame.sprite.Sprite):
    def __init__(self,x,y,width,height, speed):
        ...resto do init...
        self.color = (150,150,150)
        self.ry = 0
        self.color_text = (255,255,255)
        self.font = pygame.font.Font(None, 25)
    def display_score(self, left,top):
        text = self.font.render(f"Score: {self.score}",True,self.color_text)
        text_rect = text.get_rect(left=left,top=top)
        screen.blit(text, text_rect) 
    

```
Para implementar a fonte, precisando usar a classe font do pygame e passar o tipo de font que quer usar e o tamanho, no meu caso vou usar a fonte padram, mas caso queira usar outra fonte e so baixar o arquivo e insesir aqui 

```python 
    self.font = pygame.font.Font(...fonte aqui..., 25)
```
depois disso precisamos renderizar o que queremos que seja escrito na tela, e a cor, logo em seguida nos posicionamos onde queremos e blitamos na tela.

```python 
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

Depois disso so precisamos inserir no nosso loop principal a função que criamos o display_score passando as cordenadas que queremos.