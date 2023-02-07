from pygame.locals import *
import pygame as pg

class player_t:
    def __init__(self, image):
        self.player_rect = image.get_rect()
        self.player_rect.x = 32
        self.player_rect.y = 32
        self.speed = 1
    
    def move_right(self):
        self.player_rect.x = self.player_rect.x + self.speed
    
    def move_left(self):
        self.player_rect.x = self.player_rect.x - self.speed
        
    def move_up(self):
        self.player_rect.y = self.player_rect.y - self.speed
    
    def move_down(self):
        self.player_rect.y = self.player_rect.y + self.speed

class maze_t:
    def __init__(self):
        self.m = 10
        self.n = 8
        self.maze = [0,0,1,1,1,1,1,1,1,1,
                     1,0,0,0,0,0,0,0,0,1,
                     1,0,0,0,0,0,0,0,0,1,
                     1,0,1,1,1,1,1,1,0,1,
                     1,0,1,0,0,0,0,0,0,1,
                     1,0,1,0,1,1,1,1,0,1,
                     1,0,0,0,0,0,0,0,0,1,
                     1,1,1,1,1,1,1,1,1,1,]
                     
    def draw(self, canvas, image_surf):
        self.bx=0
        self.by=0
        self.list_of_x_blocks = []
        self.list_of_y_blocks = []
        self.block_rects = []
        for i in range(0, self.m*self.n):
            if self.maze[ self.bx + (self.by*self.m) ] == 1:
                block = canvas.blit(image_surf, ( self.bx * 64, self.by * 64 ))
                self.list_of_x_blocks.append(self.bx * 64)
                self.list_of_y_blocks.append(self.by * 64)
                self.block_rects.append(block)
            
            self.bx = self.bx + 1
            if self.bx > self.m-1:
                self.bx = 0
                self.by = self.by + 1
                
class game_t:
    window_width  = 640
    window_height = 500
    player = 0
    
    def __init__(self):
        self._running = True
        self.canvas = None
        self._image_surf = None
        self.bg_color = (234, 210, 168)
        self.maze = maze_t()
    
    def on_init(self):
        pg.init()
        self.canvas = pg.display.set_mode(
                      (self.window_width,self.window_height))
        pg.display.set_caption("Maze Game")
        self._running = True
        self._block_surf = pg.image.load("../images/brick-wall.png").convert()
        self._image_surf = pg.image.load("../images/player.png").convert()
        self.player = player_t(self._image_surf)
    
    def on_event(self, event):
        if event.type == QUIT:
            self._running = False
    
    def on_loop(self):
        pass
        
    def on_render(self):
        self.canvas.fill(self.bg_color)

        self.maze.draw(self.canvas, self._block_surf)
        self.canvas.blit(self._image_surf,
                         (self.player.player_rect.x, self.player.player_rect.y))
        pg.display.flip()
    
    def on_cleanup(self):
        pg.quit()
    
    def check_pos_is_valid(self, x_pos, y_pos, player):
        if x_pos >= (self.window_width - 64):
            return False
        if x_pos <= 0:
            return False
        if y_pos >= (self.window_height - 64):
            return False
        if y_pos <= 0:
            return False

        return not len(self.player.player_rect.collidelistall(self.maze.block_rects))

    def check_move_right(self):
        new_x_pos = self.player.x + self.player.speed
        new_y_pos = self.player.y
        return self.check_pos_is_valid(new_x_pos, new_y_pos, self.player) and self.check_pos_is_valid(new_x_pos, new_y_pos - 32, self.player)
    
    def check_move_left(self):
        new_x_pos = self.player.x - self.player.speed - 32
        new_y_pos = self.player.y
        return self.check_pos_is_valid(new_x_pos - 32, new_y_pos, self.player) and self.check_pos_is_valid(new_x_pos - 32, new_y_pos - 32, self.player)

    def check_move_down(self):
        new_x_pos = self.player.x
        new_y_pos = self.player.y + self.player.speed
        return self.check_pos_is_valid(new_x_pos, new_y_pos, self.player) and self.check_pos_is_valid(new_x_pos - 32, new_y_pos, self.player)

    def check_move_up(self):
        new_x_pos = self.player.x
        new_y_pos = self.player.y - self.player.speed - 32
        return self.check_pos_is_valid(new_x_pos, new_y_pos - 32, self.player) and self.check_pos_is_valid(new_x_pos - 32, new_y_pos - 32, self.player)
        
    def on_execute(self):
        if self.on_init() == False:
            self._running = False
        
        while(self._running):
            pg.event.pump()
            keys = pg.key.get_pressed()
            
            if (keys[K_RIGHT]):
                self.player.player_rect.x += 5
            
            if (keys[K_LEFT]):
                self.player.player_rect.x -= 5

            if (keys[K_UP]):
                self.player.player_rect.y -= 5

            if (keys[K_DOWN]):
                self.player.player_rect.y += 5
            
            if (keys[K_ESCAPE]):
                self._running = False
            
            self.on_loop()
            self.on_render()
        self.on_cleanup()

if __name__ == "__main__":
    the_game = game_t()
    the_game.on_execute()

