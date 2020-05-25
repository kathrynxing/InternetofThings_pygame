import os
import sys
import pygame as pg
import random as rd
PLAYER_SIZE = (20,20)
SCREEN_SIZE = (500,700)

TRANSPARENT = (0, 0, 0, 0)

DIRECT_DICT = {pg.K_LEFT    :(-1, 0),
               pg.K_RIGHT   :( 1, 0),
               pg.K_UP      :( 0, 1),
               pg.K_DOWN    :( 0,-1)}

PLAYER_SIZE = (20,20)
class ObstaclePair(object):
    """
    Obstacle pair: non-user controlled
    """
    SPEED = -5
    def __init__(self, sides, speed):
        """
        Randomly generate the rect for 2 rectangles
        --(0,-70),(random, 70)
        --(random,-70), (500-random, 70)
        """
        
        self.center = rd.randint(sides[0],sides[1])
        
        self.side_left = self.center- self.random_space('left')
        self.rect_left = pg.Rect((0,-70),(self.side_left,70))
        self.side_right = self.center+ self.random_space('right')
        self.rect_right = pg.Rect((self.side_right,-70),(500-self.side_right,70))
        self.speed = -5
        ##modify speed
        
        self.image_left = self.make_image('left')
        self.image_right= self.make_image('right')
        
    def random_space(self, direction):
        """
        Generate appropriate space between the pair of rectangles
        so player would be able to pass
        """
        randomspace = 0
        if direction =='left':
            if PLAYER_SIZE[0]/2<= self.center-30:
                randomspace = rd.randint(PLAYER_SIZE[0]/2, self.center)
            else:
                randomspace = self.center-30              
        else:
            if PLAYER_SIZE[0]/2 <= (470-self.center):
                randomspace = rd.randint(PLAYER_SIZE[0]/2,470-self.center)
            else:
                randomspace = 470-self.center     
        return randomspace
    
    def make_image(self, rect):
        """
        Makes a rectangle
        """
        if rect =='left':
            #v2.10--print ('\nleft size',self.rect_left.size)
            image= pg.Surface(self.rect_left.size).convert_alpha()
        else:
            #v2.10--print ('\nright size',self.rect_left.size)
            image = pg.Surface(self.rect_right.size).convert_alpha()
        #change to a pixel format suitable for quick blitting
        image.fill(pg.Color("black"))
        image_rect = image.get_rect()
        pg.draw.rect(image,pg.Color("orange"),image_rect.inflate(0,0))
        return image
    
    def move(self):
        """
        Move each pair of obstacles down every frame (update postion)
        """
        self.rect_left.move_ip(0, self.speed)
        self.rect_right.move_ip(0, self.speed)
        
    def draw(self, surface):
        """
        Blit images to the target surface.
        """
        surface.blit(self.image_left, self.rect_left)
        surface.blit(self.image_right, self.rect_right)


os.environ['SDL_VIDEO_CENTERED']='1'
pg.init()
pg.display.set_caption('test')
pg.display.set_mode(SCREEN_SIZE)
screen = pg.display.get_surface()
screen.fill(pg.Color('white'))
testA = ObstaclePair([50,450],5)
for x in range (100):
    testA.move()
testA.draw(screen)
pg.quit()
sys.exit()
