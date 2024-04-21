import pygame
pygame.init()

# Screen setup
width_sc = 1280
height_sc = 603
screen = pygame.display.set_mode((width_sc, height_sc))
pygame.display.set_caption('Gravitation')
game = True
done = True
game_end = 0

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
bg_3 = pygame.image.load('BG/bg3.jpg')
main_bg = bg_3
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


# Desk
desk = pygame.image.load('obstacle/desk.png')
desk_x , desk_y = 800 , 400
desk_vel = 3

#Chairs
chair_4 = pygame.image.load('obstacle/chair.png')
chair_4_x , chair_4_y = 200 , 370
chair_4_vel = 5
chair_5 = pygame.image.load('obstacle/chair.png')
chair_5_x , chair_5_y = 500 , 10
chair_5_vel = 8
# SyStem Block
sb_1 = pygame.image.load('obstacle/sysblock.png')
sb_1_x , sb_1_y = 350 , 370
sb_1_vel = 10
sb_2 = pygame.image.load('obstacle/sysblock.png')
sb_2_x , sb_2_y = 650 , 370
sb_2_vel = 70

# Generator
gen_on = pygame.image.load('obstacle/gen_on.png')
gen_off = pygame.image.load('obstacle/generator.png')
gen_x , gen_y = 1030 , 300
gen_now = gen_on

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
    screen.blit(desk,(desk_x,desk_y))
    screen.blit(chair_4,(chair_4_x,chair_4_y))
    screen.blit(chair_5,(chair_5_x,chair_5_y))
    screen.blit(sb_1,(sb_1_x,sb_1_y))
    screen.blit(sb_2,(sb_2_x,sb_2_y))
    screen.blit(gen_now,(gen_x,gen_y))
    screen.blit(switcher,(switcher_x,switcher_y))
    if game :
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
                if event.key == pygame.K_o:
                    switch = True
        
        # Apply gravity and handle jumping
        y, jump_vel, jumping = apply_gravity_and_jump(y, jump_vel, jumping, gravity)

        # Handle player movements
        x, y, is_left, is_right, walk_count = move_player(x, y, is_left, is_right, walk_count)
        
        # Chairs motion        
        # Chair 4
        if chair_4_y <= 10:
            chair_4_vel = 5
        elif chair_4_y >= 370:
            chair_4_vel = -5
        chair_4_y += chair_4_vel
        # Chair 5
        if chair_5_y <= 10:
            chair_5_vel = 7
        elif chair_5_y >= 370:
            chair_5_vel = -7
        chair_5_y += chair_5_vel
        # Collision detection between player and chairs
        player_head = pygame.Rect(x, y, player.get_width() - 70, player.get_height() // 2)
        chair_4_rect = pygame.Rect(chair_4_x, chair_4_y, chair_4.get_width() - 50, chair_4.get_height() - 30)
        chair_5_rect = pygame.Rect(chair_5_x, chair_5_y, chair_5.get_width() - 50, chair_5.get_height() - 30)
        if player_head.colliderect(chair_4_rect) or player_head.colliderect(chair_5_rect):
            game_over()
        
        # System Blocks motion        
        # Sb 1
        if sb_1_y <= 10:
            sb_1_vel = 10
        elif sb_1_y >= 400:
            sb_1_vel = -10
        sb_1_y += sb_1_vel
        # Collision detection between player and Sb`s
        player_head = pygame.Rect(x, y, player.get_width() - 70, player.get_height() // 2)
        sb_1_rect = pygame.Rect(sb_1_x, sb_1_y, sb_1.get_width() - 70, sb_1.get_height() - 30)
        if player_head.colliderect(sb_1_rect):
            game_over()
            
        # Sb 2
        if sb_2_y <= 10:
            sb_2_vel = 7
        elif sb_2_y >= 400:
            sb_2_vel = -7
        sb_2_y += sb_2_vel
        # Collision detection between player and Sb`s
        player_head = pygame.Rect(x, y, player.get_width() - 70, player.get_height() // 2)
        sb_1_rect = pygame.Rect(sb_2_x, sb_2_y, sb_2.get_width() - 70, sb_2.get_height() - 30)
        if player_head.colliderect(sb_1_rect):
            game_over()
        
        # If vending cupboard is in range, move it up
        if abs(x - desk_x) <= 200 and desk_y >= 100:
            desk_y -= 3
        if abs(x - desk_x) > 100 and desk_y <= 400:
            desk_y += 3
        
        # Switch motion
        if desk_y <= 120 and switcher_y < 480:
            switcher_y += 5

        # Switcher pick
        player_rect = pygame.Rect(x, y, player.get_width() - 80, player.get_height() - 30)
        switcher_rect = pygame.Rect(switcher_x, switcher_y, switcher.get_width(), switcher.get_height())
        if player_rect.colliderect(switcher_rect):
            switcher_count += 1
            switcher_y = 1100

        # Switcher usage
        if switch and switcher_count == 1 :
            gen_now = gen_off
        else:
            gen_now = gen_on  
            
        # Game End
        if x > 1180 and switcher_count == 1 :
            room += 1
              
    elif game and room == 2:
        screen.fill('black')   
    pygame.display.update()
    clock.tick(FPS)
