"""
Made by Tiago Taquelim
19/03/17
Map generation
"""

import pygame, random, os
from settings import *

#Pre loading the music
pygame.mixer.pre_init(44100,16,2,4096)

#Starting the engine ;)
pygame.init()
clock = pygame.time.Clock()

#Paths
game_folder = os.path.dirname(__file__)
graphics_folder = os.path.join(game_folder, "Graphics")
music_folder = os.path.join(game_folder, "Music")
#Fonts
font = pygame.font.SysFont(None, 25)

#START THE SCREEN
screen = pygame.display.set_mode() # Default to screen resolution.

screen_dim = screen.get_rect() #Then get the user screen dimensions

display = pygame.display.set_mode((screen_dim[2],screen_dim[3]),
                                  pygame.DOUBLEBUF | pygame.RESIZABLE | pygame.FULLSCREEN)

pygame.display.set_caption(TITLE)
display.fill(green)

#Loading the graphics
house = pygame.image.load(os.path.join(graphics_folder, "house.png")).convert_alpha()
gold = pygame.image.load(os.path.join(graphics_folder, "gold.png")).convert_alpha()
grass = pygame.image.load(os.path.join(graphics_folder, "grass.png")).convert_alpha()
water = pygame.image.load(os.path.join(graphics_folder, "water.png")).convert_alpha()
tree01 = pygame.image.load(os.path.join(graphics_folder, "tree01.png")).convert_alpha()
hotbar = pygame.image.load(os.path.join(graphics_folder, "bar.png")).convert_alpha()
build_icon = pygame.image.load(os.path.join(graphics_folder, "build_icon.png")).convert_alpha()
resource_bar = pygame.image.load(os.path.join(graphics_folder, "r_bar.png")).convert_alpha()
msg_bar = pygame.image.load(os.path.join(graphics_folder, "msg_bar.png")).convert_alpha()
wood_icon = pygame.image.load(os.path.join(graphics_folder, "wood_icon.png")).convert_alpha()
food_icon = pygame.image.load(os.path.join(graphics_folder, "food_icon.png")).convert_alpha()
gold_icon = pygame.image.load(os.path.join(graphics_folder, "gold_icon.png")).convert_alpha()
start_button = pygame.image.load(os.path.join(graphics_folder, "button_new.png")).convert_alpha()
load_button = pygame.image.load(os.path.join(graphics_folder, "button_load.png")).convert_alpha()
exit_button = pygame.image.load(os.path.join(graphics_folder, "button_exit.png")).convert_alpha()
start_on_button = pygame.image.load(os.path.join(graphics_folder, "button_on_new.png")).convert_alpha()
load_on_button = pygame.image.load(os.path.join(graphics_folder, "button_on_load.png")).convert_alpha()
exit_on_button = pygame.image.load(os.path.join(graphics_folder, "button_on_exit.png")).convert_alpha()
bg = pygame.image.load(os.path.join(graphics_folder, "bg.jpg")).convert_alpha()

#Load music
pygame.mixer.music.load(os.path.join(music_folder, "bg_music_0.mp3"))


#variables
tiles = []

tiles_water = []
tiles_grass  = []
tiles_gold = []
tiles_trees = []

icons = []

#game default resources
resources_gold = 0
resources_food = 100
resources_wood = 100

timer = 0
display.blit(msg_bar, [screen_dim[2]/2 - 100, 0])


def game_intro():
    global timer
    timer_act = 0 #timer is the solution for showing images and text during a certain amout of time

    intro = True
    a = True
    b = True
    c = True

    display.blit(bg, [0,0] )

    while intro:
        timer += 1

        if timer_act < timer:
            display.blit(msg_bar, [screen_dim[2]/2 - 100, 0])

        if a:
            display.blit(start_button, [screen_dim[2]/2 - 150,screen_dim[3]/2 - 100])
        if b:
            display.blit(load_button, [screen_dim[2]/2 - 150,screen_dim[3]/2 ])
        if c:
            display.blit(exit_button, [screen_dim[2]/2 - 150,screen_dim[3]/2 + 100])



        for event in pygame.event.get():


            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            if event.type == pygame.MOUSEMOTION:

                mouse_pos = pygame.mouse.get_pos()
                x = mouse_pos[0]
                y = mouse_pos[1]


                if x < screen_dim[2]/2 + 150  and x > screen_dim[2]/2 - 150 and y < screen_dim[3]/2 - 50 and y >screen_dim[3]/2 - 100:
                    display.blit(start_on_button, [screen_dim[2]/2 - 150,screen_dim[3]/2 - 100])
                    a = False

                else:
                    a = True

                if x < screen_dim[2]/2 + 150  and x > screen_dim[2]/2 - 150 and y < screen_dim[3]/2 + 50 and y > screen_dim[3]/2:
                    display.blit(load_on_button, [screen_dim[2]/2 - 150,screen_dim[3]/2 ])
                    b = False
                else:
                    b = True

                if x < screen_dim[2]/2 + 150  and x > screen_dim[2]/2 - 150 and y < screen_dim[3]/2 + 150 and y > screen_dim[3]/2 + 100:
                    display.blit(exit_on_button, [screen_dim[2]/2 - 150,screen_dim[3]/2 + 100])
                    c = False
                else:
                    c = True

            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                x = mouse_pos[0]
                y = mouse_pos[1]


                if x < screen_dim[2]/2 + 150  and x > screen_dim[2]/2 - 150 and y < screen_dim[3]/2 - 50 and y >screen_dim[3]/2 - 100:
                    intro = False
                    mapGenerate()
                    mapRead()

                if x < screen_dim[2]/2 + 150  and x > screen_dim[2]/2 - 150 and y < screen_dim[3]/2 + 50 and y > screen_dim[3]/2:
                    screen_msg(screen_dim[2]/2 - 100, 0 , red, "Not Working")
                    timer_act = timer + 50

                if x < screen_dim[2]/2 + 150  and x > screen_dim[2]/2 - 150 and y < screen_dim[3]/2 + 150 and y > screen_dim[3]/2 + 100:
                    pygame.quit()
                    quit()



        pygame.display.update()
        clock.tick(20)

def espace_():
    pass


def resource_display():
    #Displaying a background
    display.blit(resource_bar,[0,0])

    #converting to string for displaying purposes
    dis_resources_food = str(resources_food)
    dis_resources_gold = str(resources_gold)
    dis_resources_wood = str(resources_wood)

    display_food = font.render( dis_resources_food, True, white)
    display_gold = font.render( dis_resources_gold , True, white)
    display_wood = font.render(dis_resources_wood , True, white)



    display.blit(food_icon, [0,5])
    display.blit(wood_icon, [0,20])
    display.blit(gold_icon, [0,35])
    display.blit(display_food, [25,5])
    display.blit(display_wood, [25,20])
    display.blit(display_gold, [25,35])



def mapGenerate():
    """
    Generates a code map with numbers from 0 to 3 wich represent and will spawn the objects for the map
    in a random process.
    0-> water
    1-> grass
    2-> trees
    3-> gold
    """
    file = open("mapcode.txt", "w")

    #Basic Random Algorithm
    for row in range(rows):
        for tile in range(squares):

            typee = random.randint(0,3)

            if tile == (squares - 1):
                #Without space in the to dont mess the reading algorithm.
                file.write("%i"%(typee))
            else:
                file.write("%i "%(typee))

        file.write(" \n")


    file.close()


    
#Random map generation system:
def mapRead():
    """
	This function is going to read the mapcode.txt created in the
	generation function to create a visible map with graphics from
	the numbers on the map sheet.
	"""

    tile_x = 0
    tile_y = 0

    file = open("mapcode.txt", "r")
	
    for line in file:

        numbs = line.split(" ")


        for tile in numbs:

            if tile == "0":
                display.blit(water, [tile_x,tile_y])


                tiles.append((tile_x,tile_y))
                tiles_water.append((tile_x,tile_y))

                tile_x += 50
            if tile == "1":
                display.blit(grass, [tile_x,tile_y])


                tiles.append((tile_x,tile_y))
                tiles_grass.append((tile_x,tile_y))
                    
                tile_x += 50

            if tile == "2":
                display.blit(grass, [tile_x,tile_y])
                display.blit(tree01, [tile_x,tile_y])

                tiles.append((tile_x,tile_y))
                tiles_trees.append((tile_x,tile_y))

                tile_x += 50

            if tile == "3":
                display.blit(grass, [tile_x,tile_y])
                display.blit(gold, [tile_x,tile_y])

                tiles.append((tile_x,tile_y))
                tiles_gold.append((tile_x,tile_y))
                    
                tile_x += 50

        #starting a new line...
        tile_x = 0
        tile_y += 50


    #Coverting the lists tiles in strings for logging
    tiles_all = str(len(tiles))
    trees_all = str(len(tiles_trees))
    grass_all = str(len(tiles_grass))
    gold_all = str(len(tiles_gold))
    water_all = str(len(tiles_water))

    file2 = open("log.txt","w")
    file2.writelines("Total tiles: " + tiles_all + "\n")
    file2.writelines("Tree tiles: " + trees_all+ "\n")
    file2.writelines("Grass tiles: " + grass_all+ "\n")
    file2.writelines("Gold tiles: " + gold_all+ "\n")
    file2.writelines("Water tiles: " + water_all+ "\n")

    file2.close()
    file.close()


def blit_hotbar():
    display.blit(hotbar, [0,screen_dim[3] - screen_dim[3]/5])


def hotbar_add_item():

    display.blit(build_icon, [20,(screen_dim[3] - screen_dim[3]/5) + 15])
    icons.append((20,(screen_dim[3] - screen_dim[3]/5) + 15))


def buy_tile(tile, color):
    #Highlights the tile
    hrect = pygame.draw.rect(display, color, [tile[0], tile[1],50,50], 1)
        

def build_house(tile):
    x = tile[0]
    y = tile[1]

    display.blit(house, [x,y])
    print("House built at", tile)

def get_tile():
    mouse_pos = pygame.mouse.get_pos()

    x = mouse_pos[0]
    y = mouse_pos[1]
    for tile in tiles:
        if tile[0] <= x and (tile[0] + 50) >= x and tile[1] <= y and (tile[1] + 50) >= y:

            print("Object get at: ", tile)
            return tile
def get_icon():
    mouse_pos = pygame.mouse.get_pos()

    x = mouse_pos[0]
    y = mouse_pos[1]

    for icon in icons:
        if (icon[0] <= x and (icon[0] + 50) >= x and icon[1] <= y and (icon[1] + 50) >= y):
            blit_hotbar()
            print("clicked")
            return icon

def destroyObject(tile):
    x = tile[0]
    y = tile[1]

    display.blit(water, [x,y])
    print("Destroying in :",x,y)

def load_buttons():
    blit_hotbar()
    hotbar_add_item()

def load_builder():
    display.blit(house, (20,(screen_dim[3] - screen_dim[3]/5) + 15))
    blit_hotbar()


def screen_msg(x,y,color,msg):
    render_msg = font.render(msg , True, color)
    display.blit(render_msg, [x,y])



"""
Game loop is where the game updates and makes the decisions
"""


timer_act = 0 #timer is the solution for showing images and text during a certain amout of time


#Game calling
game_intro()

pygame.mixer.music.set_volume(0.5)
pygame.mixer.music.play(-1) #-1 is for looping the music

running = True

while running:
    #Keep game running at right speed
    clock.tick(FPS)

    timer += 1


    #MSG BAR display
    if timer_act < timer:
        display.blit(msg_bar, [screen_dim[2]/2 - 100, 0])


    #Process input events
    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:

            if event.key == pygame.K_ESCAPE:
                #display_menu() TODO
             pass

            if event.key == pygame.K_DELETE:

                destroyObject(get_tile())

            #Build a house
            if event.key == pygame.K_1:
                if resources_wood >= 50:
                    resources_wood -= 50

                    buy_tile(get_tile(), blue)
                    build_house(get_tile())
                else:
                    screen_msg(screen_dim[2]/2 - 100, 0, red, "Not enought wood")
                    timer_act = timer + 50





                    #Buy a tile
            if event.key == pygame.K_2:
                buy_tile(get_tile(), blue)


    #Update
    load_buttons()

    #Display the resources

    resource_display()

    """
    TO USE WHEN DOING HOTBAR
    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONDOWN:
             get_icon()
            load_builder()
    """
    #Draw / Render


    #Updating the display after the changes
    pygame.display.update()

#End of the game loop
pygame.quit()
quit()












