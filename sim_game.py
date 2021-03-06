import pygame
import sys
import random
pygame.init()

white = (255, 255, 255)
yellow = (255, 255, 102)
black = (0, 0, 0)
red = (255, 00, 80)
green = (0, 255, 0)
blue = (0, 0, 255)

word_font = pygame.font.SysFont("comicsansms", 20)

display_w = 1200
display_h = 700

x1 = 450
x2 = 675
x3 = 225
y1 = 50
y2 = 175
y3 = 425
y4 = 550

point_arr = [[x1, y1], [x2, y2], [x2, y3], [x1, y4], [x3, y3], [x3, y2]]
lines_list = []

disp = pygame.display.set_mode((display_w, display_h))
pygame.display.set_caption('SIM Game by 201RDB138')

clock = pygame.time.Clock()


def make_game_field():
    for i in range(6):
        pygame.draw.circle(disp, red, point_arr[i], 5)

    title = 'Enter 2 points e.g. 1;2:'
    mesg = word_font.render(title, True, red)
    disp.blit(mesg, [800, 100])


def points():
    for i in range(6):
        value = word_font.render(str(i), True, white)
        disp.blit(value, point_arr[i])


def message(msg, color):
    mesg = word_font.render(msg, True, color)
    disp.blit(mesg, [700, 500])


def lines(plines, lenght):
    for i in range(lenght):
        pygame.draw.line(disp, plines[i][2], plines[i][0], plines[i][1], 3)


def check_game(player_list):
    play = False
    pl_len = len(player_list)
    for i in range(pl_len):
        for j in range(pl_len):
            if i != j:
                if player_list[i][0] == player_list[j][0]:
                    for n in range(pl_len):
                        if (player_list[n][0] == player_list[i][1] and player_list[n][1] ==
                            player_list[j][1]) or (
                            player_list[n][1] == player_list[i][1] and player_list[n][0] ==
                                player_list[j][1]):
                            play = True
    return play


def check_blue(player_list):
    play = -1
    pl_len = len(player_list)
    for i in range(pl_len):
        for j in range(pl_len):
            if i != j:
                if player_list[i][0] == player_list[j][0]:
                    for n in range(pl_len):
                        if (player_list[n][0] == player_list[i][1] and player_list[n][1] ==
                            player_list[j][1]) or (
                            player_list[n][1] == player_list[i][1] and player_list[n][0] ==
                                player_list[j][1]):
                            play = -1
                        else:
                            play = 0

    return play


def rules():
    active = False
    user_text = ''
    input_rect = pygame.Rect(500, 400, 50, 40)
    while not active:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE:
                    user_text = user_text[:-1]
                elif event.key == pygame.K_RETURN:
                    active = True
                else:
                    user_text += event.unicode

        disp.fill(0)
        title = 'SIM game rules:'
        mesg = word_font.render(title, True, red)
        disp.blit(mesg, [display_w / 5, 100])

        body = ['Both players take turns connecting 2 points in a hexagon. The aim of this game',
                'is to not make a triangle using only one players lines. Meaning the player who',
                'creates a triangle first or has no more moves left which do not make a trinagle',
                'loses the game.',
                'Be careful with your inputs, game does not have good error handling!',
                'To choose who begins the game input "a" for computer or "b" for yourself',
                'Press enter to play']
        label = []
        for line in range(len(body)):
            label.append(word_font.render(body[line], True, yellow))

        for line in range(len(label)):
            disp.blit(label[line], [display_w / 5, 150 + 25 * line])

        pygame.draw.rect(disp, blue, input_rect)
        text_surface = word_font.render(user_text, True, (255, 255, 255))
        disp.blit(text_surface, (input_rect.x + 5, input_rect.y + 5))
        input_rect.w = max(5, text_surface.get_width() + 10)
        pygame.display.flip()
        clock.tick(60)

    return str(user_text)


def game_loop():
    red_list = []
    blue_list = []
    blue_try = []
    player1 = rules()
    clock.tick(10)
    playing = True
    game = False
    game_play = False
    user_text = ''
    while playing:
        while game:
            if player1 == 'a':
                message('You lost the game! To play again press "p"', red)
            else:
                message('You won the game! To play again press "p"', green)
            lines_list.clear()
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_p:
                        game_loop()

        if player1 == 'a':
            rez = -1
            while rez == -1:
                p1 = random.randint(0, 5)
                p2 = random.randint(0, 5)
                while p2 == p1:
                    p1 = random.randint(0, 5)
                    p2 = random.randint(0, 5)
                palist_try = [p1, p2]
                palist_try.sort()
                blue_try.append(palist_try)
                rez = check_blue(blue_try)
            palist = palist_try
            if ([point_arr[palist[0]], point_arr[palist[1]], red] not in lines_list) and ([point_arr[palist[0]], point_arr[palist[1]], blue] not in lines_list):
                lines_list.append([point_arr[palist[0]], point_arr[palist[1]], blue])
                blue_list.append(palist)
                game_play = check_game(blue_list)
                player1 = 'b'

        input_rect = pygame.Rect(800, 150, 50, 40)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE:
                    user_text = user_text[:-1]
                elif event.key == pygame.K_RETURN:
                    point = user_text.split(';')
                    p1 = int(point[0])
                    p2 = int(point[1])
                    plist = [p1, p2]
                    plist.sort()
                    if ([point_arr[plist[0]], point_arr[plist[1]], red] in lines_list) or ([point_arr[plist[0]], point_arr[plist[1]], blue] in lines_list):
                        for i in range(900):
                            message('Line already exists!', red)
                            pygame.display.update()
                    else:
                        lines_list.append([point_arr[plist[0]], point_arr[plist[1]], red])
                        red_list.append(plist)
                        game_play = check_game(red_list)
                        player1 = 'a'
                        user_text = ''
                else:
                    user_text += event.unicode

        pygame.draw.rect(disp, blue, input_rect)
        text_surface = word_font.render(user_text, True, (255, 255, 255))
        disp.blit(text_surface, (input_rect.x + 5, input_rect.y + 5))
        input_rect.w = max(5, text_surface.get_width() + 10)
        pygame.display.flip()

        lenght = len(lines_list)
        disp.fill(black)
        lines(lines_list, lenght)

        if game_play:
            game = True

        make_game_field()
        points()

    pygame.quit()
    quit()


game_loop()
