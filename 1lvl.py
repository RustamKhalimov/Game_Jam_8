import pygame
pygame.init()

# Screen setup
width_sc = 1280
height_sc = 599
screen = pygame.display.set_mode((width_sc, height_sc))
pygame.display.set_caption('Gravitation')
game = True
done = True

#Sounds
background_music = 'Sounds/bg_sound.mp3'
pygame.mixer.music.load(background_music)
pygame.mixer.music.play(-1)  
game_over_sound = pygame.mixer.Sound('Sounds/game-over.mp3')

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



# Backgrounds
bg_1 = pygame.image.load('BG/bg1.png')
bg_2 = pygame.image.load('BG/bg2.png')
bg_3 = pygame.image.load('BG/bg3.jpg')
main_bg = bg_1
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
        if x < 1190:
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
jump_vel = -12
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

# Obstacle images and their pos
# Level 1 Obstacle
vend_1 = pygame.image.load('obstacle/vend_right.png')
vend_1_x, vend_1_y = 1000, 300
vend_2 = pygame.image.load('obstacle/vend_left.png')
vend_2_x, vend_2_y = 100, 100
Soda = pygame.image.load('obstacle/soda.png')


sofa = pygame.image.load('obstacle/sofa.png')
sofa_x, sofa_y = 500, 300
sofa_vel = 5

# Generation of soda
soda_1_list = []
soda_2_list = []
s1_start_time1 = pygame.time.get_ticks()
s1_start_time2 = pygame.time.get_ticks()
s2_start_time1 = pygame.time.get_ticks()
s2_start_time2 = pygame.time.get_ticks()

# Switcher parts
battery_1 = pygame.image.load('Switcher Parts/battery.png')
battery_1_x , battery_1_y = 1050 , 280
battery_2 = pygame.image.load('Switcher Parts/battery.png')
battery_2_x , battery_2_y = 1050 , 340
switcher =  pygame.image.load('Switcher Parts/controlbox.png')
switcher_x , switcher_y = 850 , 130
switch = False
battery_count = 0
switcher_count = 0

clock = pygame.time.Clock()
FPS = 60


while done: 
    screen.blit(main_bg, (0, 0)) 
    # Room 1
    if game and room == 1:
        screen.blit(sofa, (sofa_x, sofa_y))
        screen.blit(vend_1, (vend_1_x, vend_1_y))
        screen.blit(vend_2, (vend_2_x, vend_2_y))
        if battery_1_y >= 280:
            screen.blit(battery_1, (battery_1_x, battery_1_y))
        # Handle jumping when space is pressed
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
        # Vend 1
        if pygame.time.get_ticks() - s1_start_time1 > 3350:
            soda_1_list.append([vend_1_x + 20, vend_1_y + 15])
            s1_start_time1 = pygame.time.get_ticks()
        if pygame.time.get_ticks() - s1_start_time2 > 4655:
            soda_1_list.append([vend_1_x + 20, vend_1_y + 95])
            s1_start_time2 = pygame.time.get_ticks()
        for soda_1 in soda_1_list:
            screen.blit(Soda, (soda_1[0], soda_1[1]))
            soda_1[0] -= 10
        for soda in soda_1_list[:]:
            soda_rect = pygame.Rect(soda[0], soda[1], Soda.get_width() - 50, Soda.get_height() - 30)
            player_rect = pygame.Rect(x, y, player.get_width() - 80, player.get_height() - 30)
            if soda_rect.colliderect(player_rect):
                game_over()

        # Vend 2
        if pygame.time.get_ticks() - s2_start_time1 > 2200:
            soda_2_list.append([vend_2_x + 20, vend_2_y + 15])
            s2_start_time1 = pygame.time.get_ticks()
        if pygame.time.get_ticks() - s2_start_time2 > 5500:
            soda_2_list.append([vend_2_x + 20, vend_2_y + 95])
            s2_start_time2 = pygame.time.get_ticks()
        for soda_2 in soda_2_list:
            screen.blit(Soda, (soda_2[0], soda_2[1]))
            soda_2[0] += 10
        for soda in soda_2_list[:]:
            soda_rect = pygame.Rect(soda[0], soda[1], Soda.get_width() - 10 , Soda.get_height() - 50)
            player_rect = pygame.Rect(x, y, player.get_width() - 160 , player.get_height() - 50)
            if soda_rect.colliderect(player_rect):
                game_over()

        # If vending machine is in range, move it up
        if abs(x - vend_1_x) <= 200 and vend_1_y >= 100:
            vend_1_y -= 1
        if abs(x - vend_1_x) > 100 and vend_1_y <= 300:
            vend_1_y += 1
        if abs(x - vend_2_x) <= 200 and vend_2_y >= 100:
            vend_2_y -= 1
        if abs(x - vend_2_x) > 100 and vend_2_y <= 300:
            vend_2_y += 1

        # Handle battery interaction
        if vend_1_y <= 280 and battery_1_y < 480:
            battery_1_y += 2

        # Collision detection between player and battery_1
        player_rect = pygame.Rect(x, y, player.get_width() - 80, player.get_height() - 30)
        battery_1_rect = pygame.Rect(battery_1_x, battery_1_y, battery_1.get_width(), battery_1.get_height())
        if player_rect.colliderect(battery_1_rect):
            battery_count += 1
            battery_1_y = -100 

        # Sofa
        # Move sofa up and down
        if sofa_y <= 80:
            sofa_vel = 5
        elif sofa_y >= 300:
            sofa_vel = -5

        sofa_y += sofa_vel

        # Collision detection between player and sofa
        player_head = pygame.Rect(x, y, player.get_width() - 70, player.get_height() // 2)
        sofa_rect = pygame.Rect(sofa_x, sofa_y, sofa.get_width() - 50, sofa.get_height() - 60)
        if player_head.colliderect(sofa_rect):
            game_over()

        if x >= 1180 and battery_count == 1:
            screen.fill('black')
            room += 1
            main_bg = bg_2
            x, y = 50, 370         

    pygame.display.update()
    clock.tick(FPS)
