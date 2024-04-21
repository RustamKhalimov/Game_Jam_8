import pygame
pygame.init()

#music
background_music = 'music/bg_sound.mp3'
pygame.mixer.music.load(background_music)  # Загружаем музыкальный файл
pygame.mixer.music.play(-1)  # -1 означает, что музыка будет проигрываться в бесконечном цикле

while done: 
    def game_over():
        global game
        game = False
        pygame.mixer.music.stop()  # Остановка воспроизведения фоновой музыки

        game_over_sound.play()
        screen.fill((0, 0, 0))
        font = pygame.font.SysFont('comicsans', 80)
        game_over_text = font.render('Game Over', 1, (255, 0, 0))
        screen.blit(game_over_text, (width_sc/2 - game_over_text.get_width()/2, height_sc/2 - game_over_text.get_height()/2))
        pygame.display.update()

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return
