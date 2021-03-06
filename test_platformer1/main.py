# platform game
import pygame as pg
import random
from settings import *
from sprites import *


class Game:
    def __init__(self):
        # initialize game windows
        pg.init()
        pg.mixer.init()
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        pg.display.set_caption(TITLE)
        self.clock = pg.time.Clock()
        self.running = True
    
    def new(self):
        # start a new game
        self.all_sprites = pg.sprite.Group()
        self.platforms = pg.sprite.Group()
        self.player = Player(self)
        self.all_sprites.add(self.player)
        for plat in PLATFORM_LIST:
            p = Platform(*plat)
            self.all_sprites.add(p)
            self.platforms.add(p)
        self.run()
        
        
    def run(self):
        # Game loop
        self.playing = True
        while self.playing:
            self.clock.tick(FPS)
            self.events()
            self.update()
            self.draw()
    
    def update(self):
        # Game loop - update
            # Update
        self.all_sprites.update()
        # check if player hits a platform - only if falling
        if self.player.vel.y > 0:
            hits = pg.sprite.spritecollide(self.player,self.platforms,False)
            if hits:
                self.player.pos.y = hits[0].rect.top
                self.player.vel.y = 0       
        # if player reaches top 1/4 of screen
        if self.player.rect.top <= HEIGHT / 4:
            # get player down
            self.player.pos.y += abs(self.player.vel.y)
            for plat in self.platforms:
                # get all platforms down
                plat.rect.y += abs(self.player.vel.y)
                # kill all down screen platforms
                if plat.rect.top >= HEIGHT:
                    plat.kill()
        # spawn new platforms to keep same average number
        while len(self.platforms) < 6:
            width = random.randrange(50, 100)
            p = Platform(random.randrange(0, WIDTH - width),
                         random.randrange(-75, -30),
                         width, 20)
            self.platforms.add(p)
            self.all_sprites.add(p)
            

    def events(self):
        # Game loop - events
            # Process input (events)
        for event in pg.event.get():
            # check for closing window
            if event.type == pg.QUIT:
                if self.playing:
                    self.playing = False
                self.running = False
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_SPACE:
                    self.player.jump()

        
    def draw(self):
        # Game loop - draw
            # Draw / render
        self.screen.fill(BLACK)
        self.all_sprites.draw(self.screen)
            # *after* drawing everything, flip the display
        pg.display.flip()


    def show_start_screen(self):
        # game splash/start screen
        pass
    
    def show_go_screen(self):
        # game over/continue
        pass

    
g = Game()
g.show_start_screen()
while g.running :
    g.new()
    g.show_go_screen()

pg.quit()