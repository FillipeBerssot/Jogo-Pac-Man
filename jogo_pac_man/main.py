import sys
import pygame
import levels
import os


HEROPATH = os.path.join(os.getcwd(), 'resources/images/pacman.png')
BlinkyPATH = os.path.join(os.getcwd(), 'resources/images/Blinky.png')
ClydePATH = os.path.join(os.getcwd(), 'resources/images/Clyde.png')
InkyPATH = os.path.join(os.getcwd(), 'resources/images/Inky.png')
PinkyPATH = os.path.join(os.getcwd(), 'resources/images/Pinky.png')
FONTPATH = os.path.join(os.getcwd(), 'resources/font/ALGER.TTF')
SOUNDPATH = os.path.join(os.getcwd(), 'resources/sounds/bg.mp3')
LOGOPATH = os.path.join(os.getcwd(), 'resources/images/pacman-logo-1.png')

def show_game_over_screen(screen, score, font):
    screen.fill((0, 0, 0))

    large_font = pygame.font.Font(None, 65)
    score_text = large_font.render(f'Score: {score}', True, (255, 255, 255))
    score_rect = score_text.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2))
    screen.blit(score_text, score_rect)

    small_font = pygame.font.Font(None, 26)
    msg_text = small_font.render("Pressione qualquer tecla para voltar ao menu", True, (255, 255, 255))
    msg_rect = msg_text.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2 + 100))
    screen.blit(msg_text, msg_rect)

    pygame.display.flip()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                return


def startGame(level, screen, font):
    clock = pygame.time.Clock()
    wall_sprites = level.setupWalls((0, 128, 0))
    gate_sprites = level.setupGate((255, 255, 255))

    hero_sprites, ghost_sprites = level.setupPlayers(HEROPATH, [BlinkyPATH, ClydePATH, InkyPATH, PinkyPATH])
    food_sprites = level.setupFood((255, 255, 0), (255, 255, 255))
    SCORE = 0

    move_speed = 1

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    for hero in hero_sprites:
                        hero.changeSpeed([-move_speed, 0])
                        hero.is_move = True

                elif event.key == pygame.K_RIGHT:
                    for hero in hero_sprites:
                        hero.changeSpeed([move_speed, 0])
                        hero.is_move = True

                elif event.key == pygame.K_UP:
                    for hero in hero_sprites:
                        hero.changeSpeed([0, -move_speed])
                        hero.is_move = True

                elif event.key == pygame.K_DOWN:
                    for hero in hero_sprites:
                        hero.changeSpeed([0, move_speed])
                        hero.is_move = True

        screen.fill((0, 0, 0))

        for hero in hero_sprites:
            hero.update(wall_sprites, gate_sprites)

            if pygame.sprite.spritecollide(hero, wall_sprites, False):
                hero.changeSpeed([0, 0])

        hero_sprites.draw(screen)

        for hero in hero_sprites:
            food_eaten = pygame.sprite.spritecollide(hero, food_sprites, True)

        SCORE += len(food_eaten)

        wall_sprites.draw(screen)
        gate_sprites.draw(screen)
        food_sprites.draw(screen)

        for ghost in ghost_sprites:
            if ghost.tracks_loc[1] < ghost.tracks[ghost.tracks_loc[0]][2]:
                ghost.changeSpeed(ghost.tracks[ghost.tracks_loc[0]][0:2])
                ghost.tracks_loc[1] += 1
            else:
                if ghost.tracks_loc[0] < len(ghost.tracks) - 1:
                    ghost.tracks_loc[0] += 1

                else:
                    ghost.tracks_loc[0] = 0

                ghost.tracks_loc[1] = 0

            if ghost.tracks_loc[1] < ghost.tracks[ghost.tracks_loc[0]][2]:
                ghost.changeSpeed(ghost.tracks[ghost.tracks_loc[0]][0:2])

            else:
                if ghost.tracks_loc[0] < len(ghost.tracks) - 1:
                    loc0 = ghost.tracks_loc[0] + 1

                else:
                    loc0 = 0

                ghost.changeSpeed(ghost.tracks[loc0][0: 2])

            ghost.update(wall_sprites, None)

        ghost_sprites.draw(screen)

        score_text = font.render('Score: %s' %SCORE, True, (255, 0, 0))
        screen.blit(score_text, [10, 10])

        if pygame.sprite.groupcollide(hero_sprites, ghost_sprites, False, False):
            break

        pygame.display.flip()
        clock.tick(10)

    show_game_over_screen(screen, SCORE, font)

    return

def menu(screen):
    pygame.mixer.music.stop()
    pygame.mixer.music.play(-1, 0.0)

    logo = pygame.image.load(LOGOPATH)
    logo = pygame.transform.scale(logo, (400, 200))

    while True:
        screen.fill((0, 0, 0))
        screen.blit(logo, (screen.get_width() // 2 - 200, screen.get_height() // 3))

        font = pygame.font.Font(None, 36)
        text = font.render('Pressione qualquer tecla para iniciar', True, (255, 255, 255))
        text_rect = text.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2 + 150))
        screen.blit(text, text_rect)

        smaller_font = pygame.font.Font(None, 24)
        text_dev = smaller_font.render('Desenvolvido por Fillipe Berssot', True, (255, 255, 255))
        text_dev_rect = text_dev.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2 + 280))
        screen.blit(text_dev, text_dev_rect)

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit(-1)
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                return


def initialize():
    pygame.init()
    screen = pygame.display.set_mode([606, 606])
    pygame.display.set_caption('PAC-MAN')

    return screen


def main(screen):
    pygame.mixer.init()
    pygame.mixer.music.load(SOUNDPATH)
    pygame.mixer.music.play(-1, 0.0)

    font = pygame.font.Font(FONTPATH, 18)
    
    while True:
        menu(screen)

        for num_level in range(1, levels.NUMLEVELS+1):
            if num_level == 1:
                level = levels.Level1()
                startGame(level, screen, font)


if __name__ == "__main__":
    main(initialize())