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

# Level 2 Obstacle
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

# Level 3 Obstacle
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
gen_x , gen_y = 1030 , 300
gen_off = pygame.image.load('obstacle/generator.png')
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

    # Room 2
    elif game and room == 2:
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
            gl_rect = pygame.Rect(gl[0], gl[1], Glasses_down.get_width() - 120, Glasses_down.get_height() - 70)
            player_rect = pygame.Rect(x, y, player.get_width() - 120, player.get_height() - 70)
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
            gl_rect = pygame.Rect(gl[0], gl[1], Glasses_down.get_width() - 120 , Glasses_down.get_height() - 70)
            player_rect = pygame.Rect(x, y, player.get_width() - 120 , player.get_height() - 70)
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
            gl_rect = pygame.Rect(gl[0], gl[1], Glasses_left.get_width() - 120, Glasses_left.get_height() - 70)
            player_rect = pygame.Rect(x, y, player.get_width() - 120, player.get_height() - 70)
            if gl_rect.colliderect(player_rect):
                game_over()
        # If vending machine is in range, move it up
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
            
        if x >= 1180 and battery_count == 2:
            screen.fill('black')
            room += 1
            main_bg = bg_3
            x, y = 50, 370
    
    # Room 3
    elif game and room == 3:
        screen.blit(main_bg, (0, 0)) 
        screen.blit(desk,(desk_x,desk_y))
        screen.blit(chair_4,(chair_4_x,chair_4_y))
        screen.blit(chair_5,(chair_5_x,chair_5_y))
        screen.blit(sb_1,(sb_1_x,sb_1_y))
        screen.blit(sb_2,(sb_2_x,sb_2_y))
        screen.blit(gen_now,(gen_x,gen_y))
        screen.blit(switcher,(switcher_x,switcher_y))
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
                elif event.key == pygame.K_o:
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
    elif game and room == 4:
        screen.fill('black')
        font = pygame.font.SysFont('comicsans', 60)
        game_over_text = font.render('Congratulations, you save university!!! ', 1, ('white'))
        screen.blit(game_over_text, (width_sc/2 - game_over_text.get_width()/2, height_sc/2 - game_over_text.get_height()/2))         

    pygame.display.update()
    clock.tick(FPS)
