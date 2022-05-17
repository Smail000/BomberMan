
# Initialization
import pygame, sys, random, os.path, time
from pygame import image, font
pygame.init()
font.init()

Window = pygame.display.set_mode([502, 600])
Clock = pygame.time.Clock()
pygame.display.set_caption('PyBomberMan')

# Defines
def get_around(field, x, y):
    ret = []
    if x > 0 and x < len(field[0])-1 and y > 0 and y < len(field)-1:
        ret.append(field[y-1][x-1]) # 123
        ret.append(field[y-1][x])   # 8-4
        ret.append(field[y-1][x+1]) # 765
        ret.append(field[y][x+1])
        ret.append(field[y+1][x+1])
        ret.append(field[y+1][x])
        ret.append(field[y+1][x-1])
        ret.append(field[y][x-1])
    else:
        if x == 0:
            ret.append(field[y][x+1])
            if y == 0:
                ret.append(field[y+1][x+1])
                ret.append(field[y+1][x])
            elif y == len(field)-1:
                ret.append(field[y-1][x])
                ret.append(field[y-1][x+1])
            else:
                ret.append(field[y+1][x+1])
                ret.append(field[y+1][x])
                ret.append(field[y-1][x])
                ret.append(field[y-1][x+1])
        
        elif x == len(field[0])-1:
            ret.append(field[y][x-1])
            if y == 0:
                ret.append(field[y+1][x])
                ret.append(field[y+1][x-1])
            elif y == len(field)-1:
                ret.append(field[y-1][x-1])
                ret.append(field[y-1][x])
            else:
                ret.append(field[y+1][x])
                ret.append(field[y+1][x-1])
                ret.append(field[y-1][x-1])
                ret.append(field[y-1][x])
        
        elif y == 0:
            ret.append(field[y][x+1])
            ret.append(field[y+1][x+1])
            ret.append(field[y+1][x])
            ret.append(field[y+1][x-1])
            ret.append(field[y][x-1])

        elif y == len(field)-1:
            ret.append(field[y-1][x-1])
            ret.append(field[y-1][x])
            ret.append(field[y-1][x+1])
            ret.append(field[y][x+1])
            ret.append(field[y][x-1])

    return ret

def generate(len_x, len_y, count_bombs):
    field = [['-' for i in range(len_x)] for i in range(len_y)]

    for i in range(count_bombs):
        field[random.randint(0, len(field)-1)][random.randint(0, len(field[0])-1)] = {'type': 'bomb', 'fog': False, 'flag': False}

    for y, up in enumerate(field):
        for x, elem in enumerate(up):
            if elem != {'type': 'bomb', 'fog': False, 'flag': False}:
                field[y][x] = {'type': str(get_around(field, x, y).count({'type': 'bomb', 'fog': False, 'flag': False})), 'fog': False, 'flag': False, 'x': x, 'y': y}

    return field

def free(field, x, y):
    field[y][x]['fog'] = True

    null_list = list()
    for i in get_around(field, x, y):
        if i['type'] == '0' and not i['fog']:
            null_list.append(i)
        else:
            field[i['y']][i['x']]['fog'] = True

    if null_list != list():
        while True:
            cell = null_list[0]

            if not cell['fog']:
                field[cell['y']][cell['x']]['fog'] = True

                for i in get_around(field, cell['x'], cell['y']):
                    if i['type'] == '0' and not i['fog']:
                        null_list.append(i)
                    else:
                        field[i['y']][i['x']]['fog'] = True

            null_list.remove(cell)
            if null_list == list():
                break
    return field

# Colors
green = [112,255,40]
gray = [159,159,159]

# Settings
mode = 'game'

len_x, len_y = 20, 20
x0, y0 = 3, 101
bomb_size = 20
pedding = 5

count_bombs = 50

quit = False
pressed = False

bomb_img = image.load(os.path.join('assets', 'bomb.png'))
bomb_img = pygame.transform.scale(bomb_img, (bomb_size, bomb_size))

flag_img = image.load(os.path.join('assets', 'flag.png'))
flag_img = pygame.transform.scale(flag_img, (bomb_size, bomb_size))

cells = font.Font(None, bomb_size*2)
title = font.Font(None, 30)

colors = {
    '0': [112,255,40],
    '1': [0,0,255],
    '2': [13,117,15],
    '3': [255,0,0],
    '4': [170,0,255],
    '5': [255,183,0],
    '6': [44,244,255],
    '7': [117,111,113],
    '8': [0,0,0],
}

# Main loop

field = generate(len_x, len_y, count_bombs)
start_time = time.perf_counter()
started = False
# for y, up in enumerate(field):
#     print(' '.join([up[id]['type'][0] for id, i in enumerate(up)]))


while not quit:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            quit = True
            sys.exit()

    left_button, _, right_button = pygame.mouse.get_pressed()
    
    mx, my = pygame.mouse.get_pos()

    Window.fill(green)

    if mode == 'menu':
        Window.blit(cells.render('PyBomber by Kirill', False, gray), [120, 100])

    elif mode == 'game' or mode == 'end' or mode == 'win':

        if count_bombs == sum(len([x for x in i if not x['fog']]) for i in field):
            mode = 'win'

        if mode == 'game':
            if started:
                Window.blit(cells.render(f'Time: {int(time.perf_counter() - start_time)}', False, gray), [200, 50])
            else:
                Window.blit(cells.render(f'Time: 0', False, gray), [200, 50])
        elif mode == 'end':
            Window.blit(cells.render('You lose', False, gray), [200, 50])
        if mode == 'win':
            Window.blit(cells.render('You win', False, gray), [200, 50])

        for x in range(len_x):
            for y in range(len_y):

                if not field[y][x]['fog']:
                    pygame.draw.polygon(
                        Window,
                        gray,
                        ([x0+x*(bomb_size+pedding), y0+y*(bomb_size+pedding)], 
                        [x0+x*(bomb_size+pedding), y0+y*(bomb_size+pedding)+bomb_size],
                        [x0+x*(bomb_size+pedding)+bomb_size, y0+y*(bomb_size+pedding)+bomb_size],
                        [x0+x*(bomb_size+pedding)+bomb_size, y0+y*bomb_size+(y*pedding)]))
                    if field[y][x]['flag']:
                        Window.blit(flag_img, [x0+x*(bomb_size+pedding), y0+y*(bomb_size+pedding)])
                else:
                    if field[y][x]['type'] == 'bomb':
                        Window.blit(bomb_img, [x0+x*(bomb_size+pedding), y0+y*(bomb_size+pedding)])
                    else:
                        Window.blit(cells.render(field[y][x]['type'], False, colors[field[y][x]['type']]), [x0+x*(bomb_size+pedding), y0+y*(bomb_size+pedding)])

                if mode == 'game' and ( mx > x0+x*(bomb_size+pedding) and mx < x0+x*(bomb_size+pedding)+bomb_size and my > y0+y*(bomb_size+pedding) and my < y0+y*(bomb_size+pedding)+bomb_size ):

                    if not started:
                        started = True
                        start_time = time.perf_counter()
                    if left_button and not pressed:
                        if field[y][x]['flag']:
                            field[y][x]['flag'] = False
                        else:
                            if field[y][x]['type'] == 'bomb':
                                mode = 'end'
                            if field[y][x]['type'] == '0':
                                field = free(field, x, y)
                            else:
                                field[y][x]['fog'] = True
                    elif right_button and not pressed:
                        field[y][x]['flag'] = not field[y][x]['flag']
    
    if left_button or right_button:
        pressed = True
    else:
        pressed = False

    pygame.display.update()
    Clock.tick(60)


