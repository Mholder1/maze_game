import pygame
import pygame_menu
import pathlib
import re
import random

PATH = pathlib.PurePath(__file__).parent

class player_t:
    def __init__(self, player_image):
        # Set starting position for player
        self.player_rect = player_image.get_rect()
        self.player_rect.x = 270
        self.player_rect.y = 50
        self.player = player_image

class menu_t:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Maze Game")
        self.in_menu = True
        while self.in_menu:
            self.surface = pygame.display.set_mode((600, 400))

            self.menu = pygame_menu.Menu('Welcome', 600, 400,
                            theme=pygame_menu.themes.THEME_ORANGE)

            self.menu.add.text_input('Name :', default='John Doe')
            self.menu.add.selector('Difficulty :', [('Easy', 1), ('Medium', 2), ('Hard', 3)], 
                                onchange=self.set_difficulty)
            self.menu.add.button('Play', self.start_the_game)
            self.menu.add.button('Quit', pygame_menu.events.EXIT)
            try:
                self.menu.mainloop(self.surface)
            except Exception as e:
                print(e)
                pygame_menu.events.EXIT
    
    def set_difficulty(self, value, difficulty):
        self.level = difficulty
        return self.level

    def start_the_game(self):
        try:
            diff = self.level
        except Exception as e:
            diff = 1
        game_t(diff)
        self.in_menu = False
    


class game_t:
    def __init__(self, level):
        # Initialize Pygame
        self.level = level
        self.setup_maze(self.level, 1)
    
    def check_move_valid(self, x_pos, y_pos, btn):
        if x_pos >= (self.screen_w - 32) and btn == "RIGHT":
            return False
        if x_pos <= 0 and btn == "LEFT":
            return False
        if y_pos >= (self.screen_h - 32) and btn == "DOWN":
            return False
        if y_pos <= 0 and btn == "UP":
            return False
        return True

    def setup_maze(self, level, room):
        if level == 1:
            room_1 = open(f"{PATH}/../levels/level_1/room_1")
            room_2 = open(f"{PATH}/../levels/level_1/room_2")
            room_3 = open(f"{PATH}/../levels/level_1/room_3")
        elif level == 2:
            room_1 = open(f"{PATH}/../levels/level_2/room_1")
            room_2 = open(f"{PATH}/../levels/level_2/room_2")
            room_3 = open(f"{PATH}/../levels/level_2/room_3")
        elif level == 3:
            room_1 = open(f"{PATH}/../levels/level_3/room_1")
            room_2 = open(f"{PATH}/../levels/level_3/room_2")
            room_3 = open(f"{PATH}/../levels/level_3/room_3")

        self.room_1 = room_1.readlines()
        self.room_2 = room_2.readlines()
        self.room_3 = room_3.readlines()

        self.screen_w = len(self.room_1[0].split())*64
        self.screen_h = len(self.room_1)*64
        self.draw_maze(room)


    def draw_maze(self, room):
        # Set screen size and title
        self.screen = pygame.display.set_mode((self.screen_w, self.screen_h))
        pygame.display.set_caption("Maze Game")
        # Set the clock to control game speed
        self.clock = pygame.time.Clock()
        # Load the player and block images
        self.block_image = pygame.image.load(f"{PATH}/../images/brick-wall.png").convert()
        player_image = pygame.image.load(f"{PATH}/../images/player.png").convert()
        self.door_image = pygame.image.load(f"{PATH}/../images/door.png").convert()
        self.player = player_t(player_image)

        bx = 0
        by = 0
        self.block_rects = []
        self.door_rects = []
        if room == 1:
            self.current_room = self.room_1
        if room == 2:
            self.current_room = self.room_2
        if room == 3:
            self.current_room = self.room_3
        for i in self.current_room:
            symbols = re.findall(r'\S+|[^\S ]+', i)
            for s in symbols:
                if s == 'XX':
                    self.block_rects.append(pygame.Rect(bx*64, by*64, 64, 64))
                if s == 'rP':
                    self.door_rects.append(pygame.Rect(bx*64, by*64, 64, 64))
                bx += 1
                if s == '\n':
                    bx = 0
                    by = by + 1
        self.run_game()
    
    def run_game(self):         
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
                if self.check_move_valid(self.player.player_rect.x, 
                                         self.player.player_rect.y,
                                         "UP"):
                    self.player.player_rect.y -= 5
            if keys[pygame.K_DOWN]:
                if self.check_move_valid(self.player.player_rect.x, 
                                         self.player.player_rect.y,
                                         "DOWN"):
                    self.player.player_rect.y += 5
            if keys[pygame.K_LEFT]:
                if self.check_move_valid(self.player.player_rect.x, 
                                         self.player.player_rect.y,
                                         "LEFT"):
                    self.player.player_rect.x -= 5
            if keys[pygame.K_RIGHT]:
                if self.check_move_valid(self.player.player_rect.x, 
                                         self.player.player_rect.y,
                                         "RIGHT"):
                    self.player.player_rect.x += 5

            if self.player.player_rect.collidelistall(self.block_rects):
                if keys[pygame.K_UP]:
                    self.player.player_rect.y += 5
                if keys[pygame.K_DOWN]:
                    self.player.player_rect.y -= 5
                if keys[pygame.K_LEFT]:
                    self.player.player_rect.x += 5
                if keys[pygame.K_RIGHT]:
                    self.player.player_rect.x -= 5
            
            if self.player.player_rect.collidelistall(self.door_rects):
                if self.current_room == self.room_1:
                    self.draw_maze(2)
                elif self.current_room == self.room_2:
                    self.draw_maze(3)
                elif self.current_room == self.room_3:
                    self.draw_maze(1)

            # Clear screen and draw player and blocks
            self.screen.fill((234, 210, 168))
            self.screen.blit(self.player.player, self.player.player_rect)
            for block_rect in self.block_rects:
                self.screen.blit(self.block_image, block_rect)
            for door in self.door_rects:
                self.screen.blit(self.door_image, door)

            # Update screen
            pygame.display.update()
            self.clock.tick(60)
        self.quit_application()
    
    def quit_application(self):
        pygame.quit()



if __name__ == '__main__':
    menu_t()
