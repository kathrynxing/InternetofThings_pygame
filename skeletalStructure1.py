#Kathryn IOT game
#Jan 14th   v1
#Jan 17th   v1.1
#Jan 17th   v2.1 -- player direction; Obstacles
#           v2.10-- invalid resolution of obstacles e-g(-1, 70) fixed--__random_space
#           v2.11-- Obstacles showing 'move_ip' direction       fixed
#           v2.12-- Obstacles collide with eachother            fixed--counter
#           v2.13-- difficulty adjustment                       -----
#Jan 18th   v2.20-- player touch obstacle; SCORE_text display   implemented
#           v2.21-- delete obstacles falling past bottom        fixed
#           v2.23-- Info_Display -textbox on screen             implemented
#Jan 19th   v3.10-- import icon images; fit to line             implemented
#Jan 20th   v3.11-- moves background                            -----
#           v3.12-- tutorial                                    -----
#           v3.20-- end sensor                                  -----
#           v3.21-- player going into obstacles                 -----
#           v3.21-- test plan                                   -----


import os
import sys
import pygame as pg
import random as rd

#Global variables
CAPTION = "Exploring Internet of THings"
SCREEN_SIZE = (500,700)

TRANSPARENT = (0, 0, 0, 0)

DIRECT_DICT = {pg.K_LEFT    :(-1, 0),
               pg.K_RIGHT   :( 1, 0),
               pg.K_UP      :( 0,-1),
               pg.K_DOWN    :( 0, 1)}

PLAYER_SIZE = (20,20)

ADD_OBSTACLE_RATE = 35
ADD_SCORE_RATE = 7
TOPLEFT_SCORE = (10, 0)#(10, 40)
CENTER_OTHER = (SCREEN_SIZE[0]/2,SCREEN_SIZE[1]/2)
TEXTCOLOUR = (255, 255, 255) #white

IMAGE_icon1 = pg.image.load('obj1.png')
IMAGE_icon2 = pg.image.load('obj2.png')
IMAGE_icon3 = pg.image.load('obj3.png')
IMAGE_icon4 = pg.image.load('obj4.png')
IMAGE_icon5 = pg.image.load('obj5.png')
IMAGE_icon6 = pg.image.load('obj6.png')
IMAGE_List = (IMAGE_icon1,IMAGE_icon2,IMAGE_icon3,IMAGE_icon4,IMAGE_icon5,IMAGE_icon6)

class Player(object):
    """
    User controlled character; 
    """
    SIZE = PLAYER_SIZE
    def __init__(self, pos, speed):
        """
        Pos-center; setting up player
        """
        self.rect = pg.Rect((0,0), Player.SIZE)
        self.rect.center = pos
        self.speed = speed
        self.image = self.make_image()
        
    def make_image(self):
        """
        Create 'hero'; image is a Surface obj. on which a rectangle is drawn
        """
        image = pg.Surface(self.rect.size).convert_alpha()
        image.fill(TRANSPARENT)
        image_rect = image.get_rect()
        pg.draw.rect(image, pg.Color("blue"), image_rect)
        return image
    
    def update(self, keys, screen_rect):
        """
        Update position according to keys pressed
        """
        for key in DIRECT_DICT:
            if keys[key]:
                self.rect.x += DIRECT_DICT[key][0]*self.speed
                self.rect.y += DIRECT_DICT[key][1]*self.speed
            self.rect.clamp_ip(screen_rect) #keep Player on screen
            
    def check_collisions(self, objects, object_type):
        """
        Check whether Player has hit specified objects
        'Objects' is a list of obstacle/other objects
        """
        result = False   
        for ind in objects:
            if object_type=='obstacle':
                if self.rect.colliderect(ind.rect_left)or self.rect.colliderect(ind.rect_right):
                    result = True
            elif object_type=='other':
                print("to be inplemented")

        return result
                
    def draw(self, surface):
        """
        Paint to surface; image at a certain place
        """
        surface.blit(self.image, self.rect)
        
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
        self.rect_left = pg.Rect((0,-SCREEN_SIZE[1]/10),(self.side_left,SCREEN_SIZE[1]/10))
        self.side_right = self.center+ self.random_space('right')
        self.rect_right = pg.Rect((self.side_right,-SCREEN_SIZE[1]/10),(SCREEN_SIZE[0]-self.side_right,SCREEN_SIZE[1]/10))
        self.speed = speed
        
        self.image_icon_left = self.make_icon('left')
        self.image_icon_right = self.make_icon('right')
        
        self.image_left = self.make_image('left')
        self.image_right= self.make_image('right')
        
    def random_space(self, direction):
        """
        Generate appropriate space between the pair of rectangles
        so player would be able to pass
        """
        randomspace = 0
        if direction =='left':
            if PLAYER_SIZE[0]<= self.center-50:
                randomspace = rd.randint(PLAYER_SIZE[0]-6, self.center-50)
            else:
                randomspace = self.center-50              
        else:
            if PLAYER_SIZE[0]<= (450-self.center):
                randomspace = rd.randint(PLAYER_SIZE[0]-6,450-self.center)
            else:
                randomspace = 450-self.center     
        return randomspace
    def make_icon (self, lr):
        image_icon = IMAGE_List[rd.randint(0,5)]
        #image_icon.convert_alpha()
        ####
        if lr =='left':
            self.rect_icon_left = image_icon.get_rect()
            image_icon = pg.transform.scale(image_icon,(self.rect_icon_left.width,self.rect_left.height))
            self.rect_icon_left.topright = (self.rect_left.topright)
            
        else:
            self.rect_icon_right = image_icon.get_rect()
            image_icon = pg.transform.scale(image_icon,(self.rect_icon_right.width,self.rect_right.height))
            self.rect_icon_right.topleft = (self.rect_right.topleft)            
            
        return image_icon
    
    def make_image(self, rect):
        """
        Makes a rectangle
        """
        if rect =='left':
            image= pg.Surface(self.rect_left.size).convert_alpha()
        else:
            image = pg.Surface(self.rect_right.size).convert_alpha()
            
        #change to a pixel format suitable for quick blitting
        image.fill(pg.Color("black"))
        image_rect = image.get_rect()
        pg.draw.rect(image,pg.Color("blue"),image_rect.inflate(0,0))
        return image
    
    def move(self):
        """
        Move each pair of obstacles down every frame (update postion)
        Move icons with them too
        """
        self.rect_left.move_ip(0, self.speed)
        self.rect_right.move_ip(0, self.speed)
        self.rect_icon_right.move_ip(0, self.speed)
        self.rect_icon_left.move_ip(0, self.speed)
        
    def draw(self, surface):
        """
        Blit images to the target surface. Include icons
        """
        surface.blit(self.image_left, self.rect_left)
        surface.blit(self.image_right, self.rect_right)
        surface.blit(self.image_icon_left, self.rect_icon_left)
        surface.blit(self.image_icon_right, self.rect_icon_right)
        
        
##class Destination(object):
##    """
##    End-sensors as destinations
##    """
##    def __init__(self)

class Info_Display (object):
    """
    Text display with a backgound (textbox) for instructions and Score display;
    Each info_display object is one or more text_obj on one shape
    Uniformal font; text - list of lines; centre - boolean indicating position
    """  
    def __init__(self, texts, center):
        """
        Initialize bg, texts
        """
        self.font = pg.font.SysFont(None, 48)##font change
        self.center = center
        self.bg_size = [500, 700]
        self.text_surfaces = self.make_textSurface(texts,center)

        self.bg_rect = pg.Rect((0,0),self.bg_size)
        self.bg_rect.center = self.bg_center
        self.bg_image = pg.Surface(self.bg_rect.size).convert_alpha()
        self.bg_image.fill(TRANSPARENT)
        image_rect = self.bg_image.get_rect()
        pg.draw.rect(self.bg_image, pg.Color("black"), image_rect)
 
    def make_textSurface(self, texts, center):
        """
        Turn each item in the list into a Surface object; return a list of Surfaces
        Set bg_size, bg_center
        """
        text_surfaces = []
        #initialize width of bg to the window width
        ##exception handle
        try :
            for text in texts:
                text_obj = self.font.render(text, 1, TEXTCOLOUR)
                temp_width = text_obj.get_width()
                if temp_width >=self.bg_size[0]:
                    self.bg_size[0] = temp_width
                text_surfaces.append(text_obj)
        except IndexError:
            print ("index error")
        self.lines = len(text_surfaces)
        self.bg_size[1] = 40*self.lines+10
        
        if center:
            self.bg_center = (CENTER_OTHER[0],CENTER_OTHER[1]+self.bg_size[1]/2)
        else:
            self.bg_center = (TOPLEFT_SCORE[0]+self.bg_size[0]/2, self.bg_size[1]/1.5)
        return text_surfaces
    
    def draw(self, surface):
        surface.blit(bg_image, bg_rect)
        counter = 0
        for text in self.text_surfaces:
            temp_textrect = text.get_rect()
            temp_textrect.center = (CENTER_OTHER[0], CENTER_OTHER[1]+40*counter)
            counter+=1
            surface.blit(text, temp_textrect)
            
    def draw_score(self, surface,score, x, y):
        textobj = self.font.render(score, 1, TEXTCOLOUR)#return a Surface object
        textrect = textobj.get_rect()
        textrect.topleft = (x, y)
        surface.blit(textobj, textrect)
       
class Background(object):
    """
    Creates a background object; a list of backgound images; 
    """
    def __init__(self, image_name, width):
        self.image = pg.image.load(image_name)
        self.rect = self.image.

        ###
class App(object):
    """
    Events, game loop and overall program flow
    """
    def __init__(self):
        """
        Get a reference to the display surface; setup attributes;
        Create Player instance.
        Create 1st obstacle pair.
        """
        self.screen = pg.display.get_surface()
        # return a Surface object from current display
        self.screen_rect = self.screen.get_rect()
        self.clock = pg.time.Clock()
        self.fps = 60
        #frames per second
        self.done = False
        self.keys = pg.key.get_pressed()
        self.player = Player(self.screen_rect.center, 5)
        
        self.score = 0
        self.counter_score = 0
        self.score_display = Info_Display(("Score:"), False)
        
        self.obstacles =[]
        self.sides = [150, 350]
        self.obstacle_counter = 0
        self.endSensors = []        
        
    def event_loop(self):
        """
        One event loop; detect key pressed
        """
        for event in pg.event.get():
            if event.type == pg.QUIT or self.keys[pg.K_ESCAPE]:
                self.done = True
            elif event.type in (pg.KEYUP, pg.KEYDOWN):
                #KEYUP, KEYDOWN--event type
                self.keys = pg.key.get_pressed()
                
    def render(self):
        """
        Perform drawing by calling individual draw methods
        Update screen with bg image
        """
        self.screen.fill(pg.Color("lightblue"))
        self.player.draw(self.screen)
        
        for obstacle in self.obstacles:
            #v2.10--print ("check printing")
            obstacle.draw(self.screen)
        ##for loop draw() in Obstacles/Endsensor
        self.score_display.draw_score(self.screen,'Score: %s' % (self.score),10,0)
        pg.display.update()
        #update Surface to display
 #   def totorial(self):
        
    def main_loop(self):
        """
        Overall game loop
        """
        ##Add Intro tutorial
        while not self.done:
            self.event_loop()
            self.player.update(self.keys, self.screen_rect)

            self.obstacle_counter +=1
            self.counter_score +=1
            if self.counter_score == ADD_SCORE_RATE:
                self.counter_score =0
                self.score +=1
                
            if self.obstacle_counter==ADD_OBSTACLE_RATE:
                self.obstacle_counter = 0
                self.obstacles.append(ObstaclePair(self.sides, 2))
                end = len(self.obstacles)-1
                self.sides = [self.obstacles[end].side_left, self.obstacles[end].side_right]

            for obstacle in self.obstacles:
                if obstacle.rect_left.top > SCREEN_SIZE[1]:
                    self.obstacles.remove(obstacle)
                else:
                    obstacle.move()
            if self.player.check_collisions(self.obstacles, 'obstacle'):
                self.score-=1
                
            self.render()
            self.clock.tick(self.fps)
            
def main():
    """
    Prepare our environment, create a display, and start the progame.
    """
    os.environ['SDL_VIDEO_CENTERED']='1'
    pg.init()
    pg.display.set_caption(CAPTION)
    pg.display.set_mode(SCREEN_SIZE)
    ##add backgound music
    App().main_loop()
    pg.quit()
    sys.exit()

if  __name__=="__main__":
    main()
    
