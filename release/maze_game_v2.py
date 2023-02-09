import pygame
import pygame_menu
import pathlib
import re
import random
import os
from pgu import gui
import time
import pyautogui
import pygame_widgets
from pygame_widgets.button import Button

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
            self.menu.add.selector('Difficulty :', [('Easy', 1), ('Medium', 2), ('Hard', 3)], 
                                onchange=self.set_difficulty)
            self.menu.add.button('Play', self.start_the_game)
            self.menu.add.button('Quit', pygame_menu.events.EXIT)

            self.menu.mainloop(self.surface)

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
        self.text_pos_and_time = []
        self.pop_up_seconds = 1
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
        self.room_one_coins = []
        self.room_two_coins = []
        self.room_three_coins = []
        self.draw_maze(self.level, 1)


    def draw_maze(self, level, room):
        ran = random.randrange(0, 6)
        monster_exists = True
        gold_exists = True
        print(f"Room: {room}")
        # Set screen size and title
        self.screen = pygame.display.set_mode((self.screen_w, self.screen_h+128))
        self.button = Button(self.screen,
                            self.screen_w - 150, self.screen_h + 10,
                            125, 50,
                            text="Restart Game", fontSize=25,
                            inactiveColour=(200, 50, 0),
                            hoverColour=(150, 0, 0),
                            pressedColour=(0, 200, 20),
                            radius=20,
                            onClick=self.restart_game)
        pygame.display.set_caption("Maze Game")
        # Set the clock to control game speed
        self.clock = pygame.time.Clock()
        # Load the player and block images
        self.block_image = pygame.image.load(f"{PATH}/../images/brick-wall.png").convert()
        player_image = pygame.image.load(f"{PATH}/../images/char.png").convert()
        self.door_image = pygame.image.load(f"{PATH}/../images/door.png").convert()
        self.treas_img = pygame.image.load(f"{PATH}/../images/treasure.png").convert()
        self.enemy_img = pygame.image.load(f"{PATH}/../images/goblin.png").convert()
        self.exit_img = pygame.image.load(f"{PATH}/../images/exit.png").convert()
        self.coin_img = pygame.image.load(f"{PATH}/../images/coin.png").convert()
        self.player = player_t(player_image)
        
        bx = 0
        by = 0
        self.block_rects = []
        self.room_one_rects = []
        self.room_two_rects = []
        self.room_three_rects = []
        self.player_rects = []
        self.treasure_rects = []
        self.enemy_rects = []
        self.complete_game_rect = []
        self.fake_door_rects = []

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
                if s == 'r1':
                    self.room_one_rects.append(pygame.Rect(bx*64, by*64, 64, 64))
                if s == 'r2':
                    self.room_two_rects.append(pygame.Rect(bx*64, by*64, 64, 64))
                if s == 'r3':
                    self.room_three_rects.append(pygame.Rect(bx*64, by*64, 64, 64))
                if s == 'rN':
                    self.fake_door_rects.append(pygame.Rect(bx*64, by*64, 64, 64))
                if s == '++':
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
        
        y_pos = self.player_rects[ran][1]
        x_pos = self.player_rects[ran][0]
        self.player.player_rect.x = x_pos
        self.player.player_rect.y = y_pos
        self.run_game()
    
    def restart_game(self):
        self._running = False
        game_t(self.level)

    def pop_up_message(self):
        pyautogui.alert("you have done this")
    
    def show_text(self, msg, count):
        font = pygame.font.SysFont(None, 25)
        text = font.render(msg, True, (0,0,255))
        self.screen.blit(text, (10, self.screen_h + count))
    
    def render_text(self, msg, font_size):
        font = pygame.font.SysFont(None, font_size)
        return font.render(msg, True, (0,0,255))

    def enemy_encounter(self):
        self.fight_screen = pygame.display.set_mode((self.screen_w, self.screen_h + 128))
        self.fight_screen.fill((234, 210, 168))
        pygame.display.set_caption("Enemy Found")
        self.fight_screen.blit(self.enemy_img, (self.screen_w / 2, self.screen_h / 2))
        self.fight_screen.blit(self.player.player, (self.screen_w / 3, self.screen_h / 2))
        timer = pygame.time.get_ticks()
        counter = 0
        while pygame.time.get_ticks()-timer<7000:
            if self.level == 1:
                self.fight_screen.blit(self.render_text("Press left mouse key as fast as you can!", 28), 
                                    (0, 40))
            if self.level == 2:
                self.fight_screen.blit(self.render_text("Press left mouse key as fast as you can!", 30), 
                                    (self.screen_w / 10, 40))
            if self.level == 3:
                self.fight_screen.blit(self.render_text("Press left mouse key as fast as you can!", 45), 
                                    (self.screen_w / 4, 40))
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    counter += 1
                    print(counter)
            if counter == 10:
                return True
            pygame.display.update()
        return False

    def enemy_defeated(self, defeated):
        timer = pygame.time.get_ticks()
        while pygame.time.get_ticks()-timer<1000:
            if defeated == True:
                self.show_text(f"The goblin falls!", 60)
            else:
                self.show_text(f"The goblin knocks you back!", 60)
            pygame.display.update()
        
    def door_not_open(self):
        timer = pygame.time.get_ticks()
        while pygame.time.get_ticks()-timer<1000:
            self.show_text(f"The door doesn't open.", 60)
            pygame.display.update()

    def completed_game(self, wealth):
        screen = pygame.display.set_mode((600, 400))
        pygame.display.set_caption("Maze Game")
        summary = pygame_menu.Menu(f"Congratulations!", 600, 400,
                        theme=pygame_menu.themes.THEME_ORANGE)
        summary.add.label(title=f"You finished the maze with {wealth} gold.")
        summary.add.button('Play Again', menu_t)
        summary.add.button('Quit', pygame_menu.events.EXIT)
        pygame.display.update()
        try:
            summary.mainloop(screen)
        except Exception as e:
            print("in completed game error: ", e)
            pygame_menu.events.EXIT
        
    def run_game(self):         
        # Define game loop
        self._running = True
        while self._running:
            # Handle events
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    self._running = False
                if event.type == pygame.KEYUP and self.wealth > 0:
                    if event.key == pygame.K_c and self.current_room == self.room_1:
                        self.room_one_coins.append(pygame.Rect(self.player.player_rect.x, 
                                                    self.player.player_rect.y, 32, 32))
                        self.wealth -= 1
                    if event.key == pygame.K_c and self.current_room == self.room_2:
                        self.room_two_coins.append(pygame.Rect(self.player.player_rect.x, 
                                                    self.player.player_rect.y, 32, 32))
                        self.wealth -= 1
                    if event.key == pygame.K_c and self.current_room == self.room_3:
                        self.room_three_coins.append(pygame.Rect(self.player.player_rect.x, 
                                                    self.player.player_rect.y, 32, 32))
                        self.wealth -= 1
                
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

            
            if self.player.player_rect.collidelistall(self.room_one_rects):
                if keys[pygame.K_SPACE] and self.room_2 in self.monster_killed:
                    self.draw_maze(self.level, 1)

            if self.player.player_rect.collidelistall(self.room_two_rects):
                if keys[pygame.K_SPACE] and self.room_1 in self.monster_killed:
                    self.draw_maze(self.level, 2)

            if self.player.player_rect.collidelistall(self.room_three_rects):
                if keys[pygame.K_SPACE] and self.room_2 in self.monster_killed:
                    self.draw_maze(self.level, 3)
            
            if self.player.player_rect.collidelistall(self.fake_door_rects):
                if keys[pygame.K_SPACE]:
                    self.door_not_open()
            
            if self.player.player_rect.collidelistall(self.treasure_rects):
                self.wealth += 100
                self.treasure_rects.remove(self.treasure_rects[0])
                self.gold_collected.append(self.current_room)
            
            #if user encounters an enemy
            if self.player.player_rect.collidelistall(self.enemy_rects):
                if keys[pygame.K_SPACE]:
                    if self.enemy_encounter():
                        self.enemy_count -= 1
                        self.enemy_rects.remove(self.enemy_rects[0])
                        self.monster_killed.append(self.current_room)
                        self.enemy_defeated(True)
                    else:
                        self.enemy_defeated(False)
                

            #if user enters exit door
            if self.player.player_rect.collidelistall(self.complete_game_rect):
                if keys[pygame.K_SPACE]:
                    if self.enemy_count == 0:
                        self.completed_game(self.wealth)
                    else:
                        self.door_not_open()

            # Clear screen and draw player and blocks
            self.screen.fill((234, 210, 168))
            for block_rect in self.block_rects:
                self.screen.blit(self.block_image, block_rect)
            for door in self.fake_door_rects:
                self.screen.blit(self.door_image, door)
            for door in self.room_one_rects:
                self.screen.blit(self.door_image, door)
            for door in self.room_two_rects:
                self.screen.blit(self.door_image, door)
            for door in self.room_three_rects:
                self.screen.blit(self.door_image, door)
            for treas in self.treasure_rects:
                self.screen.blit(self.treas_img, treas)
            for enemy in self.enemy_rects:
                self.screen.blit(self.enemy_img, enemy)
            for exit_d in self.complete_game_rect:
                self.screen.blit(self.exit_img, exit_d)
            if self.current_room == self.room_1:
                for coin in self.room_one_coins:
                    self.screen.blit(self.coin_img, coin)
            if self.current_room == self.room_2:
                for coin in self.room_two_coins:
                    self.screen.blit(self.coin_img, coin)
            if self.current_room == self.room_3:
                for coin in self.room_three_coins:
                    self.screen.blit(self.coin_img, coin)
            self.screen.blit(self.player.player, self.player.player_rect)
            self.show_text(f"Wealth: {self.wealth}g", 10)
            self.show_text(f"Enemies remaining: {self.enemy_count}", 30)
            # Update screen
            pygame_widgets.update(events)
            pygame.display.update()
            self.clock.tick(60)
        exit()

if __name__ == '__main__':
    menu_t()
