import pygame
import random
from config import black,white,red,green,FPS,WIDTH,HEIGHT,APPLESIZE,SIZE,fontg,fontm,fontp
from funcoes import message, snake, score, obstacle
from assets import head_img,apple_img,tail_img,chompsnd,themesnd,obstacle_img

#Inicia o pygame
pygame.init()

#Configuração de tela, nome do jogo e ícone da maçã
gameDisplay = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption('Snake')
pygame.display.set_icon(apple_img)

#Clock
clock = pygame.time.Clock()


#Funções do jogo
def game_intro():
    
    intro = True
    #Música tema
    themesnd.play(loops=-1)

    while intro:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    intro = False
                if event.key == pygame.K_SPACE:
                    pygame.quit()
                    quit()

        #Tela de início
        gameDisplay.fill(white)
        message("Bem-vindo ao Python", 
        green,gameDisplay,
        -100, 
        "large")
        message("O objetivo do jogo é comer maçãs vermelhas e sobreviver",
        black,gameDisplay,
        -30)
        message("Quanto mais maçãs você comer, maior você fica",
        black,gameDisplay,
        10)
        message("Se você correr em si mesmo, ou nas bordas da tela, você morre",
        black,gameDisplay,
        50)
        message("CUIDADO COM O OBSTÁCULO!!!!!!!",
        red,gameDisplay,
        100)
        message("Pressione ENTER para iniciar ou ESPAÇO para sair",
        black,gameDisplay,
        180)

        pygame.display.update()
        clock.tick(5)

def gameLoop():
    gameExit = False
    gameOver = False

    #Coordenadas de onde nasce a cobra
    lead_x = WIDTH/2
    lead_y = HEIGHT/2

    #Controle da velocidade e direção
    lead_x_change = SIZE
    lead_y_change = 0
    direction = 'leste'

    #Coordenadas da maçã
    randAppleX = random.randrange(0,WIDTH-APPLESIZE,APPLESIZE)
    randAppleY = random.randrange(100,HEIGHT-APPLESIZE,APPLESIZE)

    #Coordenadas do obstáculo
    repete = False
    randObsX, randObsY = obstacle()

    #Checar se não coincidem
    if randObsY == randAppleY and randAppleX == randObsX:
        repete = True

    while repete:
        randObsX, randObsY = obstacle()
        if randObsY != randAppleY and randAppleX != randObsX:
            repete = False

    snakeList = []
    snakeLength = 1

    while not gameExit:

        while gameOver == True:
            #Tela de game over
            gameDisplay.fill(black)
            message("Game Over",red,gameDisplay,-50,"large")
            message("Aperte ENTER para jogar novamente ou Espaço para sair", red,gameDisplay)
            message("Final Score: {0}".format(snakeLength*100-100),red,gameDisplay,+50,"large")
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    gameExit = True
                    gameOver = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        gameExit = True
                        gameOver = False
                    if event.key == pygame.K_RETURN:
                        gameLoop()
                

        #Funcionalidades básicas do jogo
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                gameExit = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    direction = 'oeste'
                    lead_x_change = -SIZE
                    lead_y_change = 0
                elif event.key == pygame.K_RIGHT:
                    direction = 'leste'
                    lead_x_change = SIZE
                    lead_y_change = 0
                elif event.key == pygame.K_UP:
                    direction = 'sul'
                    lead_y_change = -SIZE
                    lead_x_change = 0
                elif event.key == pygame.K_DOWN:
                    direction = 'norte'
                    lead_y_change = SIZE
                    lead_x_change = 0

        #Se sair da tela
        if lead_y > HEIGHT or lead_y < 100 or lead_x < 0 or lead_x > WIDTH:
            gameOver = True

        #Troca de posição
        lead_x += lead_x_change
        lead_y += lead_y_change
    

        gameDisplay.fill(white)
        gameDisplay.blit(apple_img, (randAppleX,randAppleY))
        gameDisplay.blit(obstacle_img, (randObsX,randObsY))
        #pygame.draw.rect(gameDisplay,red,[randAppleX,randAppleY,APPLESIZE,APPLESIZE])

        #Tamanho da cobra
        snakeHead = []
        snakeHead.append(lead_x)
        snakeHead.append(lead_y)
        snakeList.append(snakeHead)
        
        if len(snakeList) > snakeLength:
            del snakeList[0]

        #Colisão com o próprio corpo
        for SEGMENT in snakeList[:-1]:
            if SEGMENT == snakeHead:
                gameOver = True

        snake(SIZE,snakeList,direction,gameDisplay)

        #Pontos
        score(snakeLength,gameDisplay)

        pygame.display.update()

        #Comer a maçã
        if lead_x >= randAppleX and lead_x <= randAppleX+APPLESIZE-SIZE:
            if lead_y >= randAppleY and lead_y <= randAppleY+APPLESIZE-SIZE:
                randAppleX = random.randrange(0,WIDTH-APPLESIZE,APPLESIZE)
                randAppleY = random.randrange(100,HEIGHT-APPLESIZE,APPLESIZE)

                #Checa se coincide com o obstáculo
                if randAppleX == randObsX and randAppleY == randObsY:
                    repete = True
                while repete:
                    randAppleX = random.randrange(0,WIDTH-APPLESIZE,APPLESIZE)
                    randAppleY = random.randrange(100,HEIGHT-APPLESIZE,APPLESIZE)
                    if randAppleX != randObsX and randAppleY != randObsY:
                        repete = False

                snakeLength += 1
                chompsnd.play()

        #Colisão com o obstáculo     
        if lead_x >= randObsX and lead_x <= randObsX+SIZE-SIZE:
            if lead_y >= randObsY and lead_y <= randObsY+SIZE-SIZE:
                gameOver = True
                chompsnd.play()

        clock.tick(FPS) 

    #Sai do jogo
    pygame.quit()
    quit()

#Funções rodando
game_intro()
gameLoop()
