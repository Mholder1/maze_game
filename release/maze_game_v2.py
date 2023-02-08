import pygame
import pathlib
import re

PATH = pathlib.PurePath(__file__).parent

class player_t:
    def __init__(self, player_image):
        # Set starting position for player
        self.player_rect = player_image.get_rect()
        self.player_rect.x = 270
        self.player_rect.y = 50
        self.player = player_image


class game_t:
    def __init__(self):
        # Initialize Pygame
        pygame.init()
        f = open(f"{PATH}/../levels/level_3/room_3")
        self.room = f.readlines()
        screen_w = len(self.room[0].split())
        screen_h = len(self.room)
        # Set screen size and title
        self.screen = pygame.display.set_mode((screen_w*64, screen_h*64))
        pygame.display.set_caption("Maze Game")
        # Set the clock to control game speed
        self.clock = pygame.time.Clock()
        # Load the player and block images
        self.block_image = pygame.image.load(f"{PATH}/../images/brick-wall.png").convert()
        player_image = pygame.image.load(f"{PATH}/../images/player.png").convert()
        self.player = player_t(player_image)
        self.run_game()

    def run_game(self):
        #Create rect object if wall symbol in config file
        bx = 0
        by = 0
        block_rects = []
        v = 0
        for i in self.room:
            symbols = re.findall(r'\S+|[^\S ]+', i)
            for s in symbols:
                if s == 'XX':
                    block_rects.append(pygame.Rect(bx*64, by*64, 64, 64))
                bx += 1
                if s == '\n':
                    bx = 0
                    by = by + 1
                
        # Define game loop
        running = True
        while running:
            # Handle events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            # Handle player movement
            keys = pygame.key.get_pressed()
            if keys[pygame.K_UP]:
                self.player.player_rect.y -= 5
            if keys[pygame.K_DOWN]:
                self.player.player_rect.y += 5
            if keys[pygame.K_LEFT]:
                self.player.player_rect.x -= 5
            if keys[pygame.K_RIGHT]:
                self.player.player_rect.x += 5

            if self.player.player_rect.collidelistall(block_rects):
                if keys[pygame.K_UP]:
                    self.player.player_rect.y += 5
                if keys[pygame.K_DOWN]:
                    self.player.player_rect.y -= 5
                if keys[pygame.K_LEFT]:
                    self.player.player_rect.x += 5
                if keys[pygame.K_RIGHT]:
                    self.player.player_rect.x -= 5

            # Clear screen and draw player and blocks
            self.screen.fill((234, 210, 168))
            self.screen.blit(self.player.player, self.player.player_rect)
            for block_rect in block_rects:
                self.screen.blit(self.block_image, block_rect)

            # Update screen
            pygame.display.update()
            self.clock.tick(60)

# Quit Pygame
pygame.quit()


if __name__ == '__main__':
    game_t()
