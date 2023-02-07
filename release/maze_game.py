from pygame.locals import *
import pygame as pg

class player_t:
    x = 64
    y = 64
    speed = 1
    
    def move_right(self):
        self.x = self.x + self.speed
    
    def move_left(self):
        self.x = self.x - self.speed
        
    def move_up(self):
        self.y = self.y - self.speed
    
    def move_down(self):
        self.y = self.y + self.speed

class maze_t:
    def __init__(self):
        self.m = 10
        self.n = 8
        self.maze = [1,1,1,1,1,1,1,1,1,1,
                     1,0,0,0,0,0,0,0,0,1,
                     1,0,0,0,0,0,0,0,0,1,
                     1,0,1,1,1,1,1,1,0,1,
                     1,0,1,0,0,0,0,0,0,1,
                     1,0,1,0,1,1,1,1,0,1,
                     1,0,0,0,0,0,0,0,0,1,
                     1,1,1,1,1,1,1,1,1,1,]
        
    def draw(self, canvas, image_surf):
        bx = 0
        by = 0
        for i in range(0, self.m*self.n):
            if self.maze[ bx + (by*self.m) ] == 1:
                canvas.blit(image_surf, ( bx * 64, by * 64 ))
            
            bx = bx + 1
            if bx > self.m-1:
                bx = 0
                by = by + 1
                
class game_t:
    window_width  = 750
    window_height = 500
    player = 0
    
    def __init__(self):
        self._running = True
        self.canvas = None
        self._image_surf = None
        self.player = player_t()
        self.bg_color = (234, 210, 168)
        self.maze = maze_t()
    
    def on_init(self):
        pg.init()
        self.canvas = pg.display.set_mode(
                      (self.window_width,self.window_height))
        pg.display.set_caption("Maze Game")
        self._running = True
        self._image_surf = pg.image.load("../images/adventurer.png").convert()
        self._block_surf = pg.image.load("../images/brick-wall.png").convert()
    
    def on_event(self, event):
        if event.type == QUIT:
            self._running = False
    
    def on_loop(self):
        pass
        
    def on_render(self):
        self.canvas.fill(self.bg_color)
        self.canvas.blit(self._image_surf,
                         (self.player.x, self.player.y))
        self.maze.draw(self.canvas, self._block_surf)
        pg.display.flip()
    
    def on_cleanup(self):
        pg.quit()
    
    
    def on_execute(self):
        if self.on_init() == False:
            self._running = False
        
        while(self._running):
            pg.event.pump()
            keys = pg.key.get_pressed()
            
            if (keys[K_RIGHT]):
                self.player.move_right()
            
            if (keys[K_LEFT]):
                self.player.move_left()
            
            if (keys[K_UP]):
                self.player.move_up()
            
            if (keys[K_DOWN]):
                self.player.move_down()
            
            if (keys[K_ESCAPE]):
                self._running = False
            
            self.on_loop()
            self.on_render()
        self.on_cleanup()

if __name__ == "__main__":
    the_game = game_t()
    the_game.on_execute()

