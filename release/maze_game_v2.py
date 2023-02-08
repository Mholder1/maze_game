import pygame
import pygame_menu
import pathlib
import re
import random
import os

PATH = pathlib.PurePath(__file__).parent

class player_t:
    def __init__(self, player_image):
        # Set starting position for player
        self.player_rect = player_image.get_rect()
        self.player_rect.x = 0
        self.player_rect.y = 0
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

            self.menu.add.text_input('Name :')
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

class game_t:
    def __init__(self, level):
        # Initialize Pygame
        self.level = level
        self.wealth = 0
        self.enemy_count = 3
        self.monster_killed = []
        self.gold_collected = []
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

        self.screen_h = len(self.room_1)*64
        self.screen_w = len(self.room_1[0].split())*64
        self.draw_maze(self.level, 2)


    def draw_maze(self, level, room):
        monster_exists = True
        gold_exists = True
        print(f"Room: {room}")
        # Set screen size and title
        self.screen = pygame.display.set_mode((self.screen_w, self.screen_h+128))
        pygame.display.set_caption("Maze Game")
        # Set the clock to control game speed
        self.clock = pygame.time.Clock()
        # Load the player and block images
        self.block_image = pygame.image.load(f"{PATH}/../images/brick-wall.png").convert()
        player_image = pygame.image.load(f"{PATH}/../images/player.png").convert()
        self.door_image = pygame.image.load(f"{PATH}/../images/door.png").convert()
        self.treas_img = pygame.image.load(f"{PATH}/../images/treasure.png").convert()
        self.enemy_img = pygame.image.load(f"{PATH}/../images/goblin.png").convert()
        self.exit_img = pygame.image.load(f"{PATH}/../images/exit.png").convert()
        self.player = player_t(player_image)

        bx = 0
        by = 0
        self.block_rects = []
        self.door_rects = []
        self.player_rects = []
        self.treasure_rects = []
        self.enemy_rects = []
        self.complete_game_rect = []
        if room == 1:
            self.current_room = self.room_1
            if self.room_1 in self.monster_killed:
                monster_exists = False
            if self.room_1 in self.gold_collected:
                gold_exists = False
        if room == 2:
            self.current_room = self.room_2
            if self.room_2 in self.monster_killed:
                monster_exists = False
            if self.room_2 in self.gold_collected:
                gold_exists = False
        if room == 3:
            self.current_room = self.room_3
            if self.room_3 in self.monster_killed:
                monster_exists = False
            if self.room_3 in self.gold_collected:
                gold_exists = False
        for i in self.current_room:
            symbols = re.findall(r'\S+|[^\S ]+', i)
            for s in symbols:
                if s == 'XX':
                    self.block_rects.append(pygame.Rect(bx*64, by*64, 64, 64))
                if s == 'rP' or s == 'rE':
                    self.door_rects.append(pygame.Rect(bx*64, by*64, 64, 64))
                if s == 'rE':
                    self.player_rects.append(pygame.Rect(bx*64, by*64, 32, 32))
                if s == 'rT' and gold_exists:
                    self.treasure_rects.append(pygame.Rect(bx*64, by*64, 32, 32))
                if s == 'rD' and monster_exists:
                    self.enemy_rects.append(pygame.Rect(bx*64, by*64, 32, 32))
                if s == 'rL':
                    self.complete_game_rect.append(pygame.Rect(bx*64, by*64, 64, 64))
                bx += 1
                if s == '\n':
                    bx = 0
                    by = by + 1
        
        y_pos = self.player_rects[0][1]
        x_pos = self.player_rects[0][0]
        if x_pos >= (self.screen_w - 64) and y_pos >= (self.screen_h - 64):
            self.player.player_rect.x = x_pos - 64
            self.player.player_rect.y = y_pos - 64
        elif y_pos >= (self.screen_h - 64):
            self.player.player_rect.x = x_pos
            self.player.player_rect.y = y_pos - 64
        elif x_pos == 0 and y_pos == 0:
            self.player.player_rect.x = x_pos
            self.player.player_rect.y = y_pos + 64
        elif x_pos > (self.screen_w - 64):
            self.player.player_rect.x = x_pos - 64
            self.player.player_rect.y = y_pos
        elif y_pos == 0:
            self.player.player_rect.x = x_pos
            self.player.player_rect.y = y_pos + 64
        elif x_pos == 0:
            self.player.player_rect.x = x_pos + 64
            self.player.player_rect.y = y_pos
        elif level == 3:
            self.player.player_rect.x = x_pos - 64
            self.player.player_rect.y = y_pos
        elif level == 1:
            self.player.player_rect.x = x_pos
            self.player.player_rect.y = y_pos
        self.run_game()
    
    def show_text(self, msg, count):
        font = pygame.font.SysFont(None, 25)
        text = font.render(msg, True, (0,0,255))
        self.screen.blit(text, (10, self.screen_h + count))

    def completed_game(self, wealth):
        self.screen = pygame.display.set_mode((self.screen_w, self.screen_h+128))
        pygame.display.set_caption("Maze Game")
        self.show_text("Wealth Found", 0)
        
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
                    self.draw_maze(self.level, 2)
                elif self.current_room == self.room_2:
                    self.draw_maze(self.level, 3)
                elif self.current_room == self.room_3:
                    self.draw_maze(self.level, 1)
            
            if self.player.player_rect.collidelistall(self.treasure_rects):
                self.wealth += 100
                self.treasure_rects.remove(self.treasure_rects[0])
                self.gold_collected.append(self.current_room)
            
            if self.player.player_rect.collidelistall(self.enemy_rects):
                self.enemy_count -= 1
                self.enemy_rects.remove(self.enemy_rects[0])
                self.monster_killed.append(self.current_room)

            if self.player.player_rect.collidelistall(self.complete_game_rect):
                if self.enemy_count == 0:
                    self.show_text(f"All enemies must be defeated before you leave.", 60)
                    self.completed_game(self.wealth)

            # Clear screen and draw player and blocks
            self.screen.fill((234, 210, 168))
            for block_rect in self.block_rects:
                self.screen.blit(self.block_image, block_rect)
            for door in self.door_rects:
                self.screen.blit(self.door_image, door)
            for treas in self.treasure_rects:
                self.screen.blit(self.treas_img, treas)
            for enemy in self.enemy_rects:
                self.screen.blit(self.enemy_img, enemy)
            for exit in self.complete_game_rect:
                self.screen.blit(self.exit_img, exit)
            self.screen.blit(self.player.player, self.player.player_rect)
            self.show_text(f"Wealth: {self.wealth}g", 10)
            self.show_text(f"Enemies remaining: {self.enemy_count}", 30)
            # Update screen
            pygame.display.update()
            self.clock.tick(60)
        self.quit_application()
    
    def quit_application(self):
        exit()

if __name__ == '__main__':
    menu_t()
