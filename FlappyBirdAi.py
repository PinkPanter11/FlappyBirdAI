import pygame
import random
import math

pygame.init()

display_w = 600
display_h = 400

black = (0,0,0)
white = (255,255,255)
red = (200,0,0)
green = (0,200,0)
blue = (0,0,255)
lred = (255,0,0)
lgreen = (0,255,0)
silver = (208,208,208)
lbrown = (203,112,14)

gameDisplay = pygame.display.set_mode((display_w,display_h))
pygame.display.set_caption("Flappy Birds")

clock = pygame.time.Clock()

vogelImg = pygame.image.load("Vogel.png")

#Inputs

# Y-1. Hinderniss
# X-1. Hinderniss
# Y Player

def sigmoid(x):
  return round((1 / (1 + math.exp(-x))),5)

def convert_to_standart(yh1,xh1,y):
    yh1 = (yh1-50)/200
    xh1 = (xh1-display_w//2-200)/150
    y = y/display_h
    return yh1,xh1,y

def neuralNet(yh1,xh1,y,weights):
    yh1,xh1,y = convert_to_standart(yh1,xh1,y)
    inputs = [yh1,xh1,y]

    #calculation layer 2
    layer2 = [[],[],[],[],[]]
    for neuron in weights[0]:
        count = 0
        for weight in neuron:
            layer2[count].append(inputs[weights[0].index(neuron)]*weight)
            count += 1
    count = 0
    for i in layer2:
        layer2[count] = sigmoid(sum(i))
        count += 1

    #calculation layer 3
    layer3 = [[],[],[],[],[]]
    for neuron in weights[1]:
        count = 0
        for weight in neuron:
            layer3[count].append(layer2[weights[1].index(neuron)]*weight)
            count += 1
    count = 0
    for i in layer3:
        layer3[count] = sigmoid(sum(i))
        count += 1

    #calculation output
    output = [[]]
    for neuron in weights[2]:
        count = 0
        for weight in neuron:
            output[count].append(layer3[weights[2].index(neuron)]*weight)
            count += 1
    count = 0
    for i in output:
        output[count] = sigmoid(sum(i))
        count += 1
        
    return output

def draw_rect(x,y,w,h,color):
    pygame.draw.rect(gameDisplay,color,[x,y,w,h])

def text_objects(text, font):
    textSurface = font.render(text, True, black)
    return textSurface, textSurface.get_rect()

def createButton(msg, x, y, w, h, ci, ca):
    draw_rect(x, y, w, h, ci)
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    if mouse[0] > x and mouse[0] < x+w:
        if mouse[1] > y and mouse[1] < y+h:
            draw_rect(x+3, y+3, w-6, 50-6, ca)
            if click[0] == 1:
                return True

    smallText = pygame.font.Font("freesansbold.ttf", 20)
    textSurface, textRect = text_objects(msg, smallText)
    textRect.center = ((x+(w/2)), (y+(h/2)))
    gameDisplay.blit(textSurface, textRect)

def clickedButton(x, y, w, h):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    if mouse[0] > x and mouse[0] < x+w:
        if mouse[1] > y and mouse[1] < y+h:
            if click[0] == 1:
                return True



def draw_player(x,y):
    gameDisplay.blit(vogelImg,(x,y))

def gravity(y):
    if y < display_h-20:
        y += 3
    return y
    
def jump(y,j):
    if j > 25:
        return y,j,False
    elif j < 19:
        return y-6,j+1,True
    elif j < 24:
        return y-4,j+1,True
    else:
        return y-3,j+1,True

def draw_hindernisse(hindernisse):
    for i in hindernisse:
        draw_rect(i[0],0,25,display_h,lgreen)
        draw_rect(i[0],i[1],25,100,white)

def move_hindernisse(hindernisse):
    a = []
    for i in hindernisse:
        if i[0]-2+25 > 0:
            a.append([i[0]-2,i[1]])
    return a

def intersect(x,y,hindernisse):
    for i in hindernisse:
        if i[0]+25 > x and i[0] < x+20:
            a = i[1]
            if y+1 > a and y+19 < a+100:
                return False
            return True
    return False

def set_score(score):
    font = pygame.font.SysFont(None, 25)
    text = font.render("Score: " +str(score), True, black)
    gameDisplay.blit(text, (display_w-100, 0))

def draw_gen(gen):
    font = pygame.font.SysFont(None, 25)
    text = font.render("Gen: " +str(gen), True, black)
    gameDisplay.blit(text, (20, 0))    

def draw_genplayer(z):
    font = pygame.font.SysFont(None, 25)
    text = font.render("Player: " +str(z), True, black)
    gameDisplay.blit(text, (20, 25))

def geth1(x,hindernisse):
    a = []
    for i in hindernisse:
        if i[0]+25 > x and i[0]-275 <= x:
            a.append(i)
    if len(a) == 1:
        return a[0][1],a[0][0]
    return a[0][1],a[0][0]

def create_weights():
    weights = [[]]
    for neuron in range(0,3):
        weights[0].append([])
        for weight in range(0,5):
            a = random.randint(-100,100)
            weights[0][-1].append(a/100)
    for j in range(0,1):
        weights.append([])
        for h in range(0,5):
            weights[-1].append([])
            for g in range(0,5):
                a = random.randint(-100,100)
                weights[-1][-1].append(a/100)
    weights.append([])
    for i in range(0,5):
        weights[-1].append([])
        for k in range(0,1):
            a = random.randint(-100,100)
            weights[-1][-1].append(a/100)
    return weights

def mutate(weights):
    a=[]
    for i in weights:
        a.append([])
        for k in i:
            a[-1].append([])
            for j in k:
                b=random.randint(-10,10)
                a[-1][-1].append(round(j+b/100,4))
    return a

##def fuse(w1,w2):
##    a = []
##    count1 = 0
##    for i in w1:
##        a.append([])
##        count2 = 0
##        for k in i:
##            a[-1].append([])
##            count3 = 0
##            for j in k:
##                r=random.randint(-10,10)
##                a[-1][-1].append(round((j+w2[count1][count2][count3])/2+r/100,4))
##                count3 = 0
##            count2+=1
##        count1+=1
##    return a

def mix(a,b):
    c = []
    for i in a:
        c.append(mutate(i))
        c.append(mutate(i))
        c.append(mutate(i))
    c.append(a[b.index(max(b))])
    return c

##def dead(score):
##    noreplay = True
##    while noreplay:
##        for event in pygame.event.get():
##            if event.type == pygame.QUIT:
##                pygame.quit()
##                quit()
##                
##        gameDisplay.fill(white)
##        textitext = pygame.font.Font("freesansbold.ttf", 50)
##        TextSurf, TextRect = text_objects("Your Score was: "+str(score), textitext)
##        TextRect.center = ((display_w/2),(display_h/2))
##        gameDisplay.blit(TextSurf, TextRect)
##
##        createButton("Replay", 250, 300, 100, 50, green, lgreen)
##
##        if clickedButton(250, 300, 100, 50):
##            noreplay = False
##            gameLoop()
##        
##        pygame.display.update()
##        clock.tick(30)

def calc_score(score,x,y,xh1,yh1):
    if x == xh1+24 or x == xh1+25:
        score = score//1 + 1
    else:
        a = yh1+50-y-10
        if a < 0:
          a = -a
        score = score//1 + (400-a)/1000
    return score

##def intro():
##    intro = True
##    while intro:
##        for event in pygame.event.get():
##            if event.type == pygame.QUIT:
##                pygame.quit()
##                quit()
##                
##        gameDisplay.fill(white)
##        textitext = pygame.font.Font("freesansbold.ttf", 50)
##        TextSurf, TextRect = text_objects("Flappy Bird", textitext)
##        TextRect.center = ((display_w/2),(display_h/2))
##        gameDisplay.blit(TextSurf, TextRect)
##
##        createButton("Play", 250, 300, 100, 50, green, lgreen)
##
##        if clickedButton(250, 300, 100, 50):
##            intro = False
##            gameLoop()
##        
##        pygame.display.update()
##        clock.tick(30)

def gameLoop(weights,z,gen):
    
    #print(weights)
    
    hindernisse = []

    x = display_w//2-200
    y = display_h//2

    k = x+150
    #x position der Hinderniss
    for i in range(0,100):
        hindernisse.append([k])
        k += 150

    #y position der Hindernisse
    m = 0
    for l in hindernisse:
        ok = False
        while not ok:
            a = random.randint(50,250)
            #Wenn abstand zu gross, neue Zufallszahl
            if m != 0:
                b = hindernisse[m-1][1] - a
                if b < 0:
                  b=-b
                if b > 150:
                  ok = False
                else:
                  ok = True
            else:
                ok = True
        hindernisse[m].append(a)
        m+=1

    hindernisse[0][1]=150
    #hindernisse = [[250, 150], [400, 145], [550, 85], [700, 222], [850, 111], [1000, 61], [1150, 167], [1300, 107], [1450, 214], [1600, 160], [1750, 180], [1900, 112], [2050, 104], [2200, 152], [2350, 167], [2500, 148], [2650, 148], [2800, 138], [2950, 72], [3100, 133], [3250, 58], [3400, 171], [3550, 89], [3700, 146], [3850, 232], [4000, 157], [4150, 178], [4300, 130], [4450, 229], [4600, 219], [4750, 240], [4900, 168], [5050, 233], [5200, 146], [5350, 242], [5500, 153], [5650, 154], [5800, 66], [5950, 205], [6100, 193], [6250, 171], [6400, 123], [6550, 184], [6700, 250], [6850, 117], [7000, 234], [7150, 200], [7300, 216], [7450, 199], [7600, 58], [7750, 67], [7900, 52], [8050, 123], [8200, 129], [8350, 83], [8500, 113], [8650, 73], [8800, 179], [8950, 170], [9100, 84], [9250, 61], [9400, 178], [9550, 222], [9700, 146], [9850, 148], [10000, 160], [10150, 161], [10300, 156], [10450, 153], [10600, 198], [10750, 120], [10900, 208], [11050, 176], [11200, 176], [11350, 211], [11500, 140], [11650, 230], [11800, 210], [11950, 91], [12100, 215], [12250, 89], [12400, 57], [12550, 92], [12700, 94], [12850, 95], [13000, 186], [13150, 226], [13300, 196], [13450, 144], [13600, 220], [13750, 97], [13900, 219], [14050, 125], [14200, 249], [14350, 129], [14500, 248], [14650, 150], [14800, 171], [14950, 80], [15100, 84]]

    jump_state = False

    score = 0

    j = 61
    
    crashed = False
    while not crashed:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    j = 0

        yh1,xh1 = geth1(x,hindernisse)
        if not jump_state: #Wenn gerade kein Sprung
            result = neuralNet(yh1,xh1,y,weights)
            if result[0] > 0.5:
                j = 0 #Sprung


                
        gameDisplay.fill(white)

        hindernisse = move_hindernisse(hindernisse)

        y,j,jump_state = jump(y,j)


        y = gravity(y)

        #print(result)

        score = calc_score(score,x,y,xh1,yh1)
        if score >= 100:
            return score
        
        draw_hindernisse(hindernisse)
        draw_player(x,y)

        set_score(score)
        draw_gen(gen)
        draw_genplayer(z)

        if intersect(x,y,hindernisse):
            crashed = True
            return score
            #dead(score)


        pygame.display.update()
        clock.tick(1200)

#intro()
a = []
for p in range(0,10):
    a.append(create_weights())
#a=[[[[0.0385, -1.105, 1.043, -0.548, -0.929], [1.298, 1.018, 1.825, 0.0765, -0.3985], [1.507, 1.2175, 0.8625, 2.55, 1.6105]], [[-0.937, -1.2905, -0.9565, -0.93, -0.384], [-1.115, -1.1275, -1.6185, -2.3725, -2.7955], [-0.278, 0.6285, 1.3395, 0.1785, 0.489], [-1.239, -1.582, -1.485, -1.3945, 0.143], [-0.792, 1.505, -0.732, 1.015, 0.478]], [[-0.827], [0.742], [-1.2635], [-0.161], [0.0255]]],[[[0.0385, -1.105, 1.043, -0.548, -0.929], [1.298, 1.018, 1.825, 0.0765, -0.3985], [1.507, 1.2175, 0.8625, 2.55, 1.6105]], [[-0.937, -1.2905, -0.9565, -0.93, -0.384], [-1.115, -1.1275, -1.6185, -2.3725, -2.7955], [-0.278, 0.6285, 1.3395, 0.1785, 0.489], [-1.239, -1.582, -1.485, -1.3945, 0.143], [-0.792, 1.505, -0.732, 1.015, 0.478]], [[-0.827], [0.742], [-1.2635], [-0.161], [0.0255]]],[[[0.0385, -1.105, 1.043, -0.548, -0.929], [1.298, 1.018, 1.825, 0.0765, -0.3985], [1.507, 1.2175, 0.8625, 2.55, 1.6105]], [[-0.937, -1.2905, -0.9565, -0.93, -0.384], [-1.115, -1.1275, -1.6185, -2.3725, -2.7955], [-0.278, 0.6285, 1.3395, 0.1785, 0.489], [-1.239, -1.582, -1.485, -1.3945, 0.143], [-0.792, 1.505, -0.732, 1.015, 0.478]], [[-0.827], [0.742], [-1.2635], [-0.161], [0.0255]]],[[[0.0385, -1.105, 1.043, -0.548, -0.929], [1.298, 1.018, 1.825, 0.0765, -0.3985], [1.507, 1.2175, 0.8625, 2.55, 1.6105]], [[-0.937, -1.2905, -0.9565, -0.93, -0.384], [-1.115, -1.1275, -1.6185, -2.3725, -2.7955], [-0.278, 0.6285, 1.3395, 0.1785, 0.489], [-1.239, -1.582, -1.485, -1.3945, 0.143], [-0.792, 1.505, -0.732, 1.015, 0.478]], [[-0.827], [0.742], [-1.2635], [-0.161], [0.0255]]],[[[0.0385, -1.105, 1.043, -0.548, -0.929], [1.298, 1.018, 1.825, 0.0765, -0.3985], [1.507, 1.2175, 0.8625, 2.55, 1.6105]], [[-0.937, -1.2905, -0.9565, -0.93, -0.384], [-1.115, -1.1275, -1.6185, -2.3725, -2.7955], [-0.278, 0.6285, 1.3395, 0.1785, 0.489], [-1.239, -1.582, -1.485, -1.3945, 0.143], [-0.792, 1.505, -0.732, 1.015, 0.478]], [[-0.827], [0.742], [-1.2635], [-0.161], [0.0255]]],[[[0.0385, -1.105, 1.043, -0.548, -0.929], [1.298, 1.018, 1.825, 0.0765, -0.3985], [1.507, 1.2175, 0.8625, 2.55, 1.6105]], [[-0.937, -1.2905, -0.9565, -0.93, -0.384], [-1.115, -1.1275, -1.6185, -2.3725, -2.7955], [-0.278, 0.6285, 1.3395, 0.1785, 0.489], [-1.239, -1.582, -1.485, -1.3945, 0.143], [-0.792, 1.505, -0.732, 1.015, 0.478]], [[-0.827], [0.742], [-1.2635], [-0.161], [0.0255]]],[[[0.0385, -1.105, 1.043, -0.548, -0.929], [1.298, 1.018, 1.825, 0.0765, -0.3985], [1.507, 1.2175, 0.8625, 2.55, 1.6105]], [[-0.937, -1.2905, -0.9565, -0.93, -0.384], [-1.115, -1.1275, -1.6185, -2.3725, -2.7955], [-0.278, 0.6285, 1.3395, 0.1785, 0.489], [-1.239, -1.582, -1.485, -1.3945, 0.143], [-0.792, 1.505, -0.732, 1.015, 0.478]], [[-0.827], [0.742], [-1.2635], [-0.161], [0.0255]]],[[[0.0385, -1.105, 1.043, -0.548, -0.929], [1.298, 1.018, 1.825, 0.0765, -0.3985], [1.507, 1.2175, 0.8625, 2.55, 1.6105]], [[-0.937, -1.2905, -0.9565, -0.93, -0.384], [-1.115, -1.1275, -1.6185, -2.3725, -2.7955], [-0.278, 0.6285, 1.3395, 0.1785, 0.489], [-1.239, -1.582, -1.485, -1.3945, 0.143], [-0.792, 1.505, -0.732, 1.015, 0.478]], [[-0.827], [0.742], [-1.2635], [-0.161], [0.0255]]],[[[0.0385, -1.105, 1.043, -0.548, -0.929], [1.298, 1.018, 1.825, 0.0765, -0.3985], [1.507, 1.2175, 0.8625, 2.55, 1.6105]], [[-0.937, -1.2905, -0.9565, -0.93, -0.384], [-1.115, -1.1275, -1.6185, -2.3725, -2.7955], [-0.278, 0.6285, 1.3395, 0.1785, 0.489], [-1.239, -1.582, -1.485, -1.3945, 0.143], [-0.792, 1.505, -0.732, 1.015, 0.478]], [[-0.827], [0.742], [-1.2635], [-0.161], [0.0255]]],[[[0.0385, -1.105, 1.043, -0.548, -0.929], [1.298, 1.018, 1.825, 0.0765, -0.3985], [1.507, 1.2175, 0.8625, 2.55, 1.6105]], [[-0.937, -1.2905, -0.9565, -0.93, -0.384], [-1.115, -1.1275, -1.6185, -2.3725, -2.7955], [-0.278, 0.6285, 1.3395, 0.1785, 0.489], [-1.239, -1.582, -1.485, -1.3945, 0.143], [-0.792, 1.505, -0.732, 1.015, 0.478]], [[-0.827], [0.742], [-1.2635], [-0.161], [0.0255]]]]

best = []
gen = 0
while True:
    b = []
    z=1
    for i in a:
        score = gameLoop(i,z,gen)
        b.append(score)
        if score > 100:
            best.append(i)
            print(best)
        z+=1
    for k in range(0,7):
        del a[b.index(min(b))]
        b.remove(min(b))
    a = mix(a,b)
    gen += 1
    #print(a)
        

pygame.quit()
quit()
