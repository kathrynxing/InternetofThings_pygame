##score = 70
##a = 'Score: %s'
##b = [a,'%(score)']
##print ('Score: %s' % (score))
##c = ''.join(b)
##print (c)

##import pygame
##from  pygame.locals import *
##from sys import exit
##from random import randint
##import level1
##import level2
##import level3
##  
##  
### making out the starting screen
##  
##while True:
## pygame.init()
## screen=pygame.display.set_mode((640,480),0,24)
## caption=pygame.display.set_caption("Hungry Snake")
## f=pygame.font.SysFont("comicsansms",50)
## text1=f.render("Hungry Snake",True,(0,255,0))
## clock=pygame.time.Clock()
## start=pygame.font.SysFont("comicsansms",30)
## text2=start.render("Press s to start",True,(0,255,0))
## q=pygame.font.SysFont("comicsansms",30)
## text3=q.render("Press q to quit",True,(0,255,0))
## s=[[300,200],[280,200],[260,200],[240,200],[220,200],[200,200],[180,200],[180,220],[160,220],[140,220],[120,220],[120,240],[100,240]]
## a=[100,240]
## pygame.draw.rect(screen,(255,0,0),Rect(a,[20,20]),0)
## screen.blit(text1,(60,60))
## screen.blit(text2,(300,300))
## screen.blit(text3,(300,350))
## for i in s:
##  pygame.draw.rect(screen,(0,255,0),Rect(i,[20,20]),0)
##  pygame.display.flip()
##  clock.tick(10)
## pygame.display.flip()
##  
###event handling (Key events)
## while True:
##  for i in pygame.event.get():
##   if i.type==QUIT:
##    exit()
##  pressed=pygame.key.get_pressed()
##  if pressed[K_q]:
##   exit()
##  if pressed[K_s]:
##   break
## break
##  
### Level screen
##while True:
## press=pygame.key.get_pressed()
## for i in pygame.event.get():
##  if i.type==QUIT or  press[K_q]:
##   exit()
## screen.fill((0,0,0))
## mousepress=pygame.mouse.get_pressed()
## l1=pygame.font.SysFont("comicsansms",50)
## l2=pygame.font.SysFont("comicsansms",30)
## l3=pygame.font.SysFont("comicsansms",30)
## l4=pygame.font.SysFont("comicsansms",30)
## r2=Rect((100,200),l2.size("Press 1 for Level 1 "))
## r3=Rect((100,250),l3.size("Press 2 for Level 2 "))
## r4=Rect((100,300),l3.size("Press 3 for Level 3 "))
## screen.blit(l1.render("Select Your Level",True,(0,255,0)),(100,100))
## screen.blit(l2.render("Press 1 for Level 1 ",True,(0,255,0)),(100,200))
## screen.blit(l3.render("Press 2 for level 2 ",True,(0,255,0)),(100,250))
## screen.blit(l4.render("Press 3 for level 3 ",True,(0,255,0)),(100,300))
## pygame.display.update()
##  
## if press[K_1] or  (r2.collidepoint(pygame.mouse.get_pos()) and mousepress[0]):
##  level1.main()
## if press[K_2] or  (r3.collidepoint(pygame.mouse.get_pos()) and mousepress[0]):
##  level2.main()
## if press[K_3] or  (r4.collidepoint(pygame.mouse.get_pos()) and mousepress[0]):
##  level3.main()

import pygame
from  pygame.locals import *
from sys import exit
from random import randint
  
  
counter=0
  
def main():
 while True:
  b=[]
#update function used for incrementing the counter
  def update():
   global counter
   counter=(counter+1)%7
# blast function used for creating the blast through sprites on collision 
  def blast(w,h):
   image=pygame.image.load("explosed-sprite.png").convert_alpha()
   width,height=image.get_size()
   for i in xrange(int(width/w)):
    b.append(image.subsurface((i*w,0,w,h)))
   #print a
  up=1
  down=2
  right=3
  left=4
  step=20
  block=[20,20]
  x=randint(1,20)
  y=randint(2,22)
  applexy=[]
  snakexy=[int(x*20),int(y*20)]
  snakelist=[[x*20,y*20],[(x-20)*20,(y*20)]]
  apple=0
  dead=0
  grow=0
  direction=right
  score=0
  start=0
  screen=pygame.display.set_mode((640,480),0,24)
  clock=pygame.time.Clock()
  
#game loop
  while not dead:
   pressed=pygame.key.get_pressed()
   for i in pygame.event.get():
    if i.type==QUIT or pressed[K_q]:
     exit()
   if pressed[K_LEFT] and direction!=right:
     direction=left
   elif pressed[K_RIGHT] and direction!=left:
      direction=right
   elif pressed[K_UP] and direction!=down:
      direction=up
   elif pressed[K_DOWN] and direction!=up:
      direction=down
   if direction==right:
    snakexy[0]=snakexy[0]+step
    if snakexy[0]>=640:
     snakexy[0]=0
  
   elif direction==left:
    snakexy[0]=snakexy[0]-step
    if snakexy[0]<0:
     snakexy[0]=620
  
   elif direction==up:
    snakexy[1]=snakexy[1]-step
    if snakexy[1]<0:
     snakexy[1]=460
   elif direction==down:
    snakexy[1]=snakexy[1]+step
    if snakexy[1]>=480:
     snakexy[1]=0
  
   if snakelist.count(snakexy)>0:
    dead=1
   if apple==0:
    x1=randint(1,31)
    y1=randint(2,22)
    applexy=[int(x1*step),int(y1*step)]
    apple=1
  
   snakelist.insert(0,list(snakexy))
   if snakexy[0]==applexy[0] and snakexy[1]==applexy[1]:
    apple=0
    score=score+1
   else:
    snakelist.pop()
#display on the screen
   screen.fill((0,0,0))
   scr=pygame.font.SysFont("comicsansms",20)
   text4=scr.render("Score : %d"%score,True,(0,255,0))
   screen.blit(text4,(500,10))
   pygame.draw.rect(screen,(255,0,0),Rect(applexy,block),0)
   for i in snakelist:
    pygame.draw.rect(screen,(0,255,0),Rect(i,block))
   pygame.display.flip()
   clock.tick(15)
  
  
  if dead==1:
   blast(20,20)
   for i in xrange(7):
    screen.blit(b[counter],(snakexy[0],snakexy[1]))
    update()
    pygame.display.update()
    clock.tick(10)
#game over
   screen.fill((0,0,0))
   over=pygame.font.SysFont("comicsansms",40)
   text5=over.render("GAME OVER",True,(0,255,0))
   s1=pygame.font.SysFont("comicsansms",30)
   s2=pygame.font.SysFont("comicsansms",30)
   screen.blit(text5,(50,50))
   screen.blit(text4,(200,200))
   screen.blit(s1.render("Press s To Play Again",True,(0,255,0)),(50,250))
   screen.blit(s2.render("Press l For Level Selection ",True,(0,255,0)),(50,300))
   pygame.display.flip()
   while True:
    for i in pygame.event.get():
     if i.type==QUIT:
      exit()
    pressed=pygame.key.get_pressed()
    if pressed[K_q]:
     exit()
    if pressed[K_s]:
     main()
    if pressed[K_l]:
     break
   break
  
  
  
if __name__=='__main__':
 main()
