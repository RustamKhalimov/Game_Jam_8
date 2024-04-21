import pygame
pygame.init()

# Screen setup
width_sc = 1280
height_sc = 599
screen = pygame.display.set_mode((width_sc, height_sc))
pygame.display.set_caption('Gravitation')
game = True
done = True

def game_over():
        global game
        game = False
        pygame.mixer.music.stop()
        game_over_sound.play()
        screen.fill('black')
        font = pygame.font.SysFont('comicsans', 80)
        game_over_text = font.render('Game Over', 1, (255, 0, 0))
        screen.blit(game_over_text, (width_sc/2 - game_over_text.get_width()/2, height_sc/2 - game_over_text.get_height()/2))
        pygame.display.update()

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return

#Sounds
background_music = 'Sounds/bg_sound.mp3'
pygame.mixer.music.load(background_music)
pygame.mixer.music.play(-1)  
game_over_sound = pygame.mixer.Sound('Sounds/game-over.mp3')

# Backgrounds
bg_2 = pygame.image.load('BG/bg2.png')
main_bg = bg_2
room = 1

# Player
player = pygame.image.load('Player/Right/player_look_right.png')
walk_right = [pygame.image.load(f'Player/Right/player_right_{i}.png') for i in range(1, 9)]
walk_left = [pygame.image.load(f'Player/left/player_left_{i}.png') for i in range(1, 9)]

x, y = 10, 370
walk_count = 0
is_left = False
is_right = False

# Player movement
def move_player(x, y, is_left, is_right, walk_count):
    keys = pygame.key.get_pressed()
    if keys[pygame.K_d]:
        if x < 1240:
            x += 10
            is_right = True
            is_left = False
    elif keys[pygame.K_a]:
        if x >= -10:
            x -= 10
            is_right = False
            is_left = True
    else:
        is_right = False
        is_left = False

    if is_left:
        screen.blit(walk_left[walk_count // 3], (x, y))
    elif is_right:
        screen.blit(walk_right[walk_count // 3], (x, y))
    else:
        screen.blit(player, (x, y))
    walk_count += 1
    if walk_count >= 24:
        walk_count = 0

    return x, y, is_left, is_right, walk_count

# Gravity and jump velocity
gravity = 0.5
jump_vel = -10
jumping = False

# Player jumping
def apply_gravity_and_jump(y, jump_vel, jumping, gravity):
    if jumping:
        y += jump_vel
        jump_vel += gravity
        if y >= 370: 
            jumping = False
            y = 370
    return y, jump_vel, jumping

# Switcher parts
battery_1 = pygame.image.load('Switcher Parts/battery.png')
battery_1_x , battery_1_y = 1050 , 280
battery_2 = pygame.image.load('Switcher Parts/battery.png')
battery_2_x , battery_2_y = 1050 , 340
switcher =  pygame.image.load('Switcher Parts/controlbox.png')

battery_count = 0
switcher_count = 0
# Obstacle images and pos


#Cupboards
cupboard_1 = pygame.image.load('obstacle/cupboard.png')
cupboard_1_x , cupboard_1_y = 300 , -20
cupboard_2 = pygame.image.load('obstacle/cupboard.png')
cupboard_2_x , cupboard_2_y = 600 , -20
cupboard_3 = pygame.image.load('obstacle/cupboard_left.png')
cupboard_3_x , cupboard_3_y = 1000 , 320

#Chairs
chair_1 = pygame.image.load('obstacle/chair.png')
chair_1_x , chair_1_y = 200 , 370
chair_1_vel = 5
chair_2 = pygame.image.load('obstacle/chair.png')
chair_2_x , chair_2_y = 500 , 10
chair_2_vel = 8
chair_3 = pygame.image.load('obstacle/chair.png')
chair_3_x , chair_3_y = 800 , 370
chair_3_vel = 5
# Generation of glasses
Glasses_down = pygame.image.load('obstacle/bottle.png')
Glasses_left = pygame.image.load('obstacle/bottle2.png')
gl_1_list = []
gl_2_list = []
gl_3_list = []
g1_start_time1 = pygame.time.get_ticks()
g1_start_time2 = pygame.time.get_ticks()
g2_start_time1 = pygame.time.get_ticks()
g2_start_time2 = pygame.time.get_ticks()
g3_start_time1 = pygame.time.get_ticks()
g3_start_time2 = pygame.time.get_ticks()

clock = pygame.time.Clock()
FPS = 60

while done:
 
    screen.blit(main_bg, (0, 0)) 
    # Room 2
    if game :
        screen.blit(battery_2, (battery_2_x,battery_2_y))
        screen.blit(cupboard_1, (cupboard_1_x,cupboard_1_y))
        screen.blit(cupboard_2, (cupboard_2_x,cupboard_2_y))
        screen.blit(cupboard_3,(cupboard_3_x,cupboard_3_y))
        screen.blit(chair_1, (chair_1_x,chair_1_y))
        screen.blit(chair_2, (chair_2_x,chair_2_y))
        screen.blit(chair_3, (chair_3_x,chair_3_y))
        keys = pygame.key.get_pressed()
        for event in pygame.event.get(): 
            if event.type == pygame.QUIT:
                done = False
                pygame.quit() 
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    if not jumping:
                        jump_vel = -13 
                        jumping = True

        # Apply gravity and handle jumping
        y, jump_vel, jumping = apply_gravity_and_jump(y, jump_vel, jumping, gravity)

        # Handle player movements
        x, y, is_left, is_right, walk_count = move_player(x, y, is_left, is_right, walk_count)
        
        # Handle obstacles
        # Cupboard 1
        if pygame.time.get_ticks() - g1_start_time1 > 2800:
            gl_1_list.append([cupboard_1_x + 20, cupboard_1_y + 95])
            g1_start_time1 = pygame.time.get_ticks()
        if pygame.time.get_ticks() - g1_start_time2 > 1849:
            gl_1_list.append([cupboard_1_x + 70, cupboard_1_y + 95])
            g1_start_time2 = pygame.time.get_ticks()
        for gl_1 in gl_1_list:
            screen.blit(Glasses_down, (gl_1[0], gl_1[1]))
            gl_1[1] += 9
        for gl in gl_1_list[:]:
            gl_rect = pygame.Rect(gl[0], gl[1], Glasses_down.get_width() - 120, Glasses_down.get_height() - 60)
            player_rect = pygame.Rect(x, y, player.get_width() - 120, player.get_height() - 60)
            if gl_rect.colliderect(player_rect):
                game_over()

        # Cupboard 2
        if pygame.time.get_ticks() - g2_start_time1 > 1600:
            gl_2_list.append([cupboard_2_x + 20, cupboard_2_y + 95])
            g2_start_time1 = pygame.time.get_ticks()
        if pygame.time.get_ticks() - g2_start_time2 > 2900:
            gl_2_list.append([cupboard_2_x + 70, cupboard_2_y + 95])
            g2_start_time2 = pygame.time.get_ticks()
        for gl_2 in gl_2_list:
            screen.blit(Glasses_down, (gl_2[0], gl_2[1]))
            gl_2[1] += 9
        for gl in gl_2_list[:]:
            gl_rect = pygame.Rect(gl[0], gl[1], Glasses_down.get_width() - 100 , Glasses_down.get_height() - 50)
            player_rect = pygame.Rect(x, y, player.get_width() - 100 , player.get_height() - 50)
            if gl_rect.colliderect(player_rect):
                game_over()
                
        # Cupboard 3
        if pygame.time.get_ticks() - g3_start_time1 > 4861:
            gl_3_list.append([cupboard_3_x + 20 , cupboard_3_y + 20])
            g3_start_time1 = pygame.time.get_ticks()
        if pygame.time.get_ticks() - g3_start_time2 > 5783:
            gl_3_list.append([cupboard_3_x + 20 , cupboard_3_y + 70])
            g3_start_time2 = pygame.time.get_ticks()
        for gl_3 in gl_3_list:
            screen.blit(Glasses_left, (gl_3[0], gl_3[1]))
            gl_3[0] -= 9
        for gl in gl_3_list[:]:
            gl_rect = pygame.Rect(gl[0], gl[1], Glasses_left.get_width() - 120, Glasses_left.get_height() - 60)
            player_rect = pygame.Rect(x, y, player.get_width() - 120, player.get_height() - 60)
            if gl_rect.colliderect(player_rect):
                game_over()
        # If vending cupboard is in range, move it up
        if abs(x - cupboard_3_x) <= 200 and cupboard_3_y >= 100:
            cupboard_3_y -= 1
        if abs(x - cupboard_3_x) > 100 and cupboard_3_y <= 300:
            cupboard_3_y += 1
                
        # Chairs motion        
        # Chair 1
        if chair_1_y <= 10:
            chair_1_vel = 5
        elif chair_1_y >= 370:
            chair_1_vel = -5
        chair_1_y += chair_1_vel
        # Chair 2
        if chair_2_y <= 10:
            chair_2_vel = 8
        elif chair_2_y >= 370:
            chair_2_vel = -8
        chair_2_y += chair_2_vel
         # Chair 3
        if chair_3_y <= 10:
            chair_3_vel = 5
        elif chair_3_y >= 370:
            chair_3_vel = -5
        chair_3_y += chair_3_vel
        # Collision detection between player and chairs
        player_head = pygame.Rect(x, y, player.get_width() - 70, player.get_height() // 2)
        chair_1_rect = pygame.Rect(chair_1_x, chair_1_y, chair_1.get_width() - 50, chair_1.get_height() - 30)
        chair_2_rect = pygame.Rect(chair_2_x, chair_2_y, chair_2.get_width() - 50, chair_2.get_height() - 30)
        chair_3_rect = pygame.Rect(chair_3_x, chair_3_y, chair_3.get_width() - 50, chair_3.get_height() - 30)
        if player_head.colliderect(chair_1_rect) or player_head.colliderect(chair_2_rect) or player_head.colliderect(chair_3_rect):
            game_over()
            
        # Handle battery interaction
        if cupboard_3_y <= 280 and battery_2_y < 480:
            battery_2_y += 2

        # Collision detection between player and battery_1
        player_rect = pygame.Rect(x, y, player.get_width() - 80, player.get_height() - 30)
        battery_2_rect = pygame.Rect(battery_2_x, battery_2_y, battery_2.get_width(), battery_2.get_height())
        if player_rect.colliderect(battery_2_rect):
            battery_count += 1
            battery_2_y = 1100
    pygame.display.update()
    clock.tick(FPS)
