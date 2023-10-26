import sys
import pygame
import random
import math
from colors import *
from ai import AI


pygame.init()

wd = 800
he = 500
sc = pygame.display.set_mode([wd, he])
init_count = 0
timer = pygame.time.Clock()
fps = 60
game_over = False
grid_size = 4
grid_padding = 8
height = 4
width = 4
board = [[0 for _ in range(width)] for _ in range(height)]
score = 0
ai_score = 0
ai_time = True
direction = ""
game_state = "menu"
timer_duration = 30
lives = 3
moves_without_change = 0
max_moves_without_change = 3
move_time_limit = 5
players = ["Player 1", "Player 2"]
current_player = 0
draw = False


def draw_score_board(remaining_time, move_time_limit, lives):
    global ai_score
    pygame.draw.rect(sc, (230, 230, 230), [0, 0, wd, 100])
    pygame.draw.rect(sc, WHITISH, [40, 140, 160, 240])
    pygame.draw.rect(sc, WHITISH, [600 + 40, 140, 160, 240])
    font = pygame.font.Font("freesansbold.ttf", 24)
    your_turn = font.render("Your Turn: ", True, (0, 0, 0))
    your_turn_rect = your_turn.get_rect(left=645, centery=50, top=160).inflate(10, 10)
    your_turn2 = font.render("AI's Turn: ", True, (0, 0, 0))
    your_turn_rect2 = your_turn2.get_rect(left=55, centery=50, top=160).inflate(10, 10)

    avatar_img = pygame.image.load("image.png")
    avatar_img = pygame.transform.scale(avatar_img, (80, 80))
    border_rect = avatar_img.get_rect(left=60 + 600, centery=50, top=200).inflate(
        10, 10
    )
    pygame.draw.rect(sc, (0, 0, 0), border_rect)
    avatar_rect = avatar_img.get_rect(left=60 + 600, centery=50, top=200)
    sc.blit(avatar_img, avatar_rect)

    avatar_img2 = pygame.image.load("aii.png")
    avatar_img2 = pygame.transform.scale(avatar_img2, (80, 80))
    avatar_rect2 = avatar_img2.get_rect(left=60, centery=50, top=200)
    border_rect2 = avatar_img.get_rect(left=60, centery=50, top=200).inflate(10, 10)
    pygame.draw.rect(sc, (0, 0, 0), border_rect2)
    sc.blit(avatar_img2, avatar_rect2)

    time_text = font.render("Time: {} sec".format(remaining_time), True, (255, 0, 0))
    time_rect = time_text.get_rect(center=(wd // 2, 50))
    sc.blit(time_text, time_rect)

    score_text2 = font.render("Score: {}".format(ai_score), True, (0, 0, 0))
    score_rect2 = score_text2.get_rect(left=60, centery=50, top=90 + 200).inflate(
        10, 10
    )
    sc.blit(score_text2, score_rect2)

    score_text = font.render("Score: {}".format(score), True, (0, 0, 0))
    score_rect = score_text.get_rect(left=660, centery=50, top=90 + 200).inflate(10, 10)
    sc.blit(score_text, score_rect)

    lives_text = font.render("Lives: {}".format(lives), True, (0, 0, 0))
    lives_rect = lives_text.get_rect(left=660 + 5, centery=50, top=110 + 200).inflate(
        10, 10
    )
    sc.blit(lives_text, lives_rect)
    if current_player == 0:
        timeout(move_time_limit)
        sc.blit(your_turn, your_turn_rect)
    else:
        sc.blit(your_turn2, your_turn_rect2)


def timeout(move_time_limit):
    timeout_radius = 40
    if current_player == 0:
        timeout_center = (700, 240)
    else:
        timeout_center = (100, 240)

    timeout_thickness = 100
    timeout_angle = (2 * math.pi) * (move_time_limit / 5)

    progress_surface = pygame.Surface(
        (2 * timeout_radius, 2 * timeout_radius), pygame.SRCALPHA
    )
    pygame.draw.circle(
        progress_surface, (0, 0, 0, 0), (timeout_radius, timeout_radius), timeout_radius
    )
    pygame.draw.arc(
        progress_surface,
        (0, 0, 0, 50),
        pygame.Rect(0, 0, 2 * timeout_radius, 2 * timeout_radius),
        math.pi / 2,
        math.pi / 2 + timeout_angle,
        timeout_thickness,
    )

    sc.blit(
        progress_surface,
        (timeout_center[0] - timeout_radius, timeout_center[1] - timeout_radius),
    )


def draw_board():
    pygame.draw.rect(sc, GRID_COLOR, [200, 100, wd - 400, he - 100], 0, 0)


def draw_tiles(board):
    for i in range(height):
        for j in range(width):
            val = board[i][j]
            if val <= 2048:
                color = CELL_COLORS[val]
            else:
                color = R
            pygame.draw.rect(sc, color, [j * 95 + 220, i * 95 + 120, 75, 75], 0, 5)
            if val > 0:
                vlen = len(str(val))
                font_size = 48 - (5 * vlen)
                font = pygame.font.Font("freesansbold.ttf", font_size)
                val_txt = font.render(str(val), True, CELL_NUMBER_COLORS[val])
                textc = val_txt.get_rect(center=(j * 95 + 257, i * 95 + 157))
                sc.blit(val_txt, textc)


def draw_new(board):
    global height, width
    if any(0 in row for row in board):
        for i in range(height):
            for j in range(width):
                if board[i][j] == 0:
                    board[i][j] = 2
                    return board
    return board


def mainmenu():
    pygame.init()
    pygame.display.set_caption("Main Menu")

    clock = pygame.time.Clock()
    font = pygame.font.Font(None, 32)
    button_width, button_height = 200, 50

    start_game_x = (wd - button_width) // 2
    start_game_y = (he - button_height) // 2 + 180

    start_game_button = pygame.Rect(
        start_game_x, start_game_y, button_width, button_height
    )

    time_options = ["30 seconds", "2 minutes", "3 minutes"]
    selected_time_option = 0
    global timer_duration

    # Load logo image
    logo_image = pygame.image.load("h2048.png")

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if start_game_button.collidepoint(mouse_pos):
                    return "gameplay"
                else:
                    x = (
                        wd
                        - sum([font.size(option)[0] for option in time_options])
                        - (len(time_options) - 1) * font.size("| ")[0]
                    ) // 2
                    y = he // 2 - 120 + 180
                    for i, option in enumerate(time_options):
                        option_width = font.size(option)[0]
                        option_rect = pygame.Rect(x, y, option_width, button_height)
                        if option_rect.collidepoint(mouse_pos):
                            selected_time_option = i
                            if selected_time_option == 0:
                                timer_duration = 30
                            elif selected_time_option == 1:
                                timer_duration = 2 * 60
                            elif selected_time_option == 2:
                                timer_duration = 3 * 60
                            break
                        x += option_width + font.size("| ")[0]

        sc.fill(WHITISH)
        logo_x = 300
        logo_y = 60
        sc.blit(logo_image, (logo_x, logo_y))

        if start_game_button.collidepoint(pygame.mouse.get_pos()):
            pygame.draw.rect(sc, CELL_COLORS[8], start_game_button)
        else:
            pygame.draw.rect(sc, CELL_COLORS[16], start_game_button)

        start_game_text = font.render("Start Game", True, (255, 255, 255))
        start_game_rect = start_game_text.get_rect(center=start_game_button.center)
        sc.blit(start_game_text, start_game_rect)

        x = (
            wd
            - sum([font.size(option)[0] for option in time_options])
            - (len(time_options) - 1) * font.size("| ")[0]
        ) // 2
        y = he // 2 + 60
        for i, option in enumerate(time_options):
            option_width = font.size(option)[0]
            option_rect = pygame.Rect(x, y, option_width, button_height)
            if i == selected_time_option:
                option_text = font.render(option, True, (0, 0, 0))
            else:
                option_text = font.render(option, True, (128, 128, 128))
            option_text_rect = option_text.get_rect(center=option_rect.center)
            sc.blit(option_text, option_text_rect)
            x += option_width + font.size("| ")[0]
            if i < len(time_options) - 1:
                separator_text = font.render("| ", True, (128, 128, 128))
                separator_rect = separator_text.get_rect(
                    midleft=(x, y + button_height // 2)
                )
                sc.blit(separator_text, separator_rect)
                x += separator_rect.width

        pygame.display.flip()
        clock.tick(60)


def mm():
    global score, ai_score, ti, draw
    sc = pygame.display.set_mode((wd, he))
    pygame.display.set_caption("Gameover")

    if len(sys.argv) > 1:
        score = int(sys.argv[1])

    clock = pygame.time.Clock()
    font = pygame.font.Font(None, 45)
    font2 = pygame.font.Font(None, 48)
    font3 = pygame.font.Font(None, 32)
    button_width, button_height = 200, 50

    game_over_x = (wd - button_width) // 2
    game_over_y = (he - button_height) // 2 - 50
    game_over_y2 = (he - button_height) // 2 - 80
    main_menu_x = (wd - button_width) // 2
    main_menu_y = (he - button_height) // 2 + 200
    print(draw)
    if remaining_time == 0:
        game_over_text2 = font.render("Timeout!!", True, (255, 0, 0))
    elif draw == True:
        game_over_text2 = font.render("No More Moves Available ", True, (255, 0, 0))
    elif lives == 0:
        game_over_text2 = font.render("All Life Exhausted ", True, (255, 0, 0))
    else:
        print("Good to Go")
    if lives == 0:
        game_over_text = font2.render("AI WON ", True, (255, 255, 255))
        avatar_img3 = pygame.image.load("ai2.png")
        avatar_img3 = pygame.transform.scale(avatar_img3, (wd, he))
    elif score > ai_score:
        game_over_text = font2.render("Human Won ", True, (255, 255, 255))
        avatar_img3 = pygame.image.load("hw.png")
        avatar_img3 = pygame.transform.scale(avatar_img3, (wd, he))

    elif score == ai_score:
        game_over_text = font2.render("Match Drawn", True, (0, 0, 0))
        avatar_img3 = pygame.image.load("drawn2.png")
        avatar_img3 = pygame.transform.scale(avatar_img3, (wd, he))

    else:
        game_over_text = font2.render("AI WON", True, (255, 255, 255))
        avatar_img3 = pygame.image.load("ai2.png")
        avatar_img3 = pygame.transform.scale(avatar_img3, (wd, he))

    game_over_rect = game_over_text.get_rect(center=(wd // 2, game_over_y + 50))
    game_over_rect2 = game_over_text2.get_rect(center=(wd // 2, game_over_y2 + 50))
    avatar_rect3 = avatar_img3.get_rect(left=0, top=0)

    avatar_surface = pygame.Surface(avatar_img3.get_size())
    avatar_surface.fill(WHITISH)
    avatar_surface.blit(avatar_img3, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)

    game_over_button = pygame.Rect(
        main_menu_x, main_menu_y, button_width, button_height
    )
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if game_over_button.collidepoint(mouse_pos):
                    draw = False
                    return "menu"

        sc.fill(WHITISH)
        sc.blit(avatar_surface, avatar_rect3)
        sc.blit(game_over_text, game_over_rect)
        sc.blit(game_over_text2, game_over_rect2)

        if game_over_button.collidepoint(pygame.mouse.get_pos()):
            pygame.draw.rect(sc, (255, 79, 55), game_over_button)
        else:
            pygame.draw.rect(sc, (255, 0, 0), game_over_button)

        main_menu_text = font3.render("Go to Main Menu", True, (255, 255, 255))
        main_menu_rect = main_menu_text.get_rect(center=game_over_button.center)
        sc.blit(main_menu_text, main_menu_rect)

        pygame.display.flip()
        clock.tick(60)


def stack():
    global board
    global height, width
    new_matrix = [[0] * width for _ in range(height)]
    for i in range(height):
        fill_position = 0
        for j in range(width):
            if board[i][j] != 0:
                new_matrix[i][fill_position] = board[i][j]
                fill_position += 1
    board = new_matrix


def combine():
    global board
    global score
    global ai_time
    global ai_score
    global height, width
    for i in range(height):
        for j in range(width - 1):
            if board[i][j] != 0 and board[i][j] == board[i][j + 1]:
                board[i][j] *= 2
                board[i][j + 1] = 0
                if ai_time:
                    ai_score += board[i][j]
                else:
                    score += board[i][j]


def reverse():
    global board
    global height, width
    new_matrix = []
    for i in range(height):
        new_matrix.append([])
        for j in range(width):
            new_matrix[i].append(board[i][width - 1 - j])
    board = new_matrix


def transpose():
    global board
    global height, width
    new_matrix = [[0] * width for _ in range(height)]
    for i in range(height):
        for j in range(width):
            new_matrix[i][j] = board[j][i]
    board = new_matrix


def left():
    stack()
    combine()
    stack()


def right():
    reverse()
    stack()
    combine()
    stack()
    reverse()


def up():
    transpose()
    stack()
    combine()
    stack()
    transpose()


def down():
    transpose()
    reverse()
    stack()
    combine()
    stack()
    reverse()
    transpose()


def take_turn(direction):
    global board
    if direction == "left":
        left()
    elif direction == "right":
        right()
    elif direction == "up":
        up()
    elif direction == "down":
        down()
    print("Human: ", score)
    print("AI: ", ai_score)
    board = draw_new(board)


running = True
draw_new_board = True

global remaining_time
while running:
    if game_state == "menu":
        a = mainmenu()
        draw = False
        start_time = pygame.time.get_ticks()
        last_move_time = pygame.time.get_ticks()
        board = [[0 for _ in range(width)] for _ in range(height)]
        draw_new_board = True
        init_count = 0
        score = 0
        ai_score = 0
        lives = 3
        game_state = a
    else:
        remaining_time = max(
            timer_duration - (pygame.time.get_ticks() - start_time) // 1000, 0
        )
        if lives == 0 or remaining_time == 0:
            a = mm()
            game_state = a
        if draw:
            a = mm()
            draw = False
            game_state = a
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT:
                    direction = "left"
                elif event.key == pygame.K_RIGHT:
                    direction = "right"
                elif event.key == pygame.K_DOWN:
                    direction = "down"
                elif event.key == pygame.K_UP:
                    direction = "up"

        if direction:
            current_player = (current_player + 1) % len(players)
        current_time = pygame.time.get_ticks()
        elapsed_time = (current_time - last_move_time) // 1000

        if draw_new_board or init_count < 2:
            board = draw_new(board)
            draw_new_board = False
            init_count += 1

        if ai_time:
            move = AI.main(board)
            print(move)
            # pygame.time.delay(1000)
            take_turn(direction=move)
            current_player = (current_player + 1) % len(players)
            ai_time = False
            last_move_time = pygame.time.get_ticks()
            if AI.check_draw(board):
                draw = True
            # draw_new_board = True

        if direction != "":
            take_turn(direction=direction)
            direction = ""
            last_move_time = pygame.time.get_ticks()
            ai_time = True
            moves_without_change = 0
            if AI.check_draw(board):
                draw = True

        if elapsed_time >= move_time_limit:
            if current_player == 0:
                lives -= 1
            current_player = (current_player + 1) % len(players)
            ai_time = True
            last_move_time = pygame.time.get_ticks()
        draw_board()
        draw_score_board(remaining_time, elapsed_time, lives)
        draw_tiles(board)
        pygame.display.flip()
        timer.tick(fps)
