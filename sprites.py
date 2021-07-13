import pygame
from config import *
import math
import random
import sys
import time

MOVE_RIGHT = 'MOVE_RIGHT'
MOVE_LEFT = 'MOVE_LEFT'
MOVE_UP = 'MOVE_UP'
MOVE_DOWN = 'MOVE_DOWN'
QUESTION = 'QUESTION'
ASK = 'ASK'
ANSWER = 'ANSWER'


class Spritesheet:
    def __init__(self, file):
        self.sheet = pygame.image.load(file).convert()

    def get_sprite(self, x,y, width, height, colorkey):
        sprite = pygame.Surface([width, height])
        sprite.blit(self.sheet, (0,0), (x,y,width,height))
        sprite.set_colorkey(colorkey)
        return sprite

class Player(pygame.sprite.Sprite):
    def __init__(self,game, x, y):
        self.game = game
        self._layer = PLAYER_LAYER
        self.groups = self.game.all_sprites, self.game.players

        pygame.sprite.Sprite.__init__(self, self.groups)

        self.info = {}
        self.library_visits = 0
        self.questions_found = 0
        self.questions_answered = 0

        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.width = TILESIZE
        self.height = TILESIZE

        self.x_change = 0
        self.y_change = 0

        self.facing = 'down'


        self.image = self.game.character_spritesheet.get_sprite(0,0,self.width,self.height, LIME)

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

    def update(self):
        self.movement()
        self.collide_source()
        self.collide_library()

        self.rect.x += self.x_change
        self.collide_blocks('x')
        self.rect.y += self.y_change
        self.collide_blocks('y')

        self.x_change = 0
        self.y_change = 0

    def control(self, actions=None):
        '''
        control player movement
        '''
        if actions is None:
            actions = []
        self.sp.update(actions)

    def movement(self, actions=None):
        if actions is None:
            actions = []
        if MOVE_LEFT in actions:
            self.x_change -= PLAYER_SPEED
            self.facing = 'left'
        if MOVE_RIGHT in actions:
            self.x_change += PLAYER_SPEED
            self.facing = 'right'
        if MOVE_UP in actions:
            self.y_change -= PLAYER_SPEED
            self.facing = 'up'
        if MOVE_DOWN in actions:
            self.y_change += PLAYER_SPEED
            self.facing = 'down'
        if QUESTION in actions:
            print(self.info)

    def collide_source(self):
        hits = pygame.sprite.spritecollide(self,self.game.sources, False, False)
        for source in hits:
            if source.question not in self.info and self.questions_found < 1:
                self.questions_found += 1
                self.info[source.question] = ''
                print('\'' + source.question + '\' added')
            if source.question in self.info and self.info[source.question] != '' and self.questions_answered < 1:
                self.questions_answered += 1
                print("I know the answer to your question \'" + source.question + "\'")
                print('\''+ self.info[source.question] + '\'\n')
                print('reward + 1')

    def collide_library(self):
        hits = pygame.sprite.spritecollide(self,self.game.libraries, False, False)

        if hits and self.library_visits < 1:
            self.library_visits += 1

            for key in self.info:
                print('looking up answer to: \'' + key)
                toolbar_width = 40

                # setup toolbar
                sys.stdout.write("[%s]" % (" " * toolbar_width))
                sys.stdout.flush()
                sys.stdout.write("\b" * (toolbar_width + 1))  # return to start of line, after '['

                for i in range(toolbar_width):
                    time.sleep(0.1)  # do real work here
                    # update the bar
                    sys.stdout.write("-")
                    sys.stdout.flush()

                sys.stdout.write("]\n")  # this ends the progress bar
                self.info[key] = 'being out in the sun for too long'
                print("Answer: being out in the sun for too long.")





    def collide_blocks(self, direction):
        if direction == 'x':
            hits = pygame.sprite.spritecollide(self, self.game.blocks, False)
            if hits:
                if self.x_change > 0:
                    self.rect.x = hits[0].rect.left - self.rect.width
                if self.x_change < 0:
                    self.rect.x = hits[0].rect.right
        if direction == 'y':
            hits = pygame.sprite.spritecollide(self, self.game.blocks, False)
            if hits:
                if self.y_change > 0:
                    self.rect.y = hits[0].rect.top - self.rect.height
                if self.y_change < 0:
                    self.rect.y = hits[0].rect.bottom






class Block(pygame.sprite.Sprite):
    def __init__(self, game, x,y):
        self.game = game
        self._layer = BLOCK_LAYER
        self.groups = self.game.all_sprites, self.game.blocks
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.width = TILESIZE
        self.height = TILESIZE

        self.image = self.game.terrain_spritesheet.get_sprite(960,448,self.width,self.height, BLACK)

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

class Ground(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self.game = game
        self._layer = GROUND_LAYER
        self.groups = self.game.all_sprites
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.width = TILESIZE
        self.height = TILESIZE

        self.image = self.game.terrain_spritesheet.get_sprite(64, 352, self.width, self.height, BLACK)

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y


class Source(pygame.sprite.Sprite):
    def __init__(self, game, x,y):
        self.game = game
        self._layer = SOURCE_LAYER
        self.groups = self.game.all_sprites, self.game.sources
        pygame.sprite.Sprite.__init__(self,self.groups)

        self.question = "What are causes of skin cancer?"

        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.width = TILESIZE
        self.height = TILESIZE

        self.image = self.game.character_spritesheet.get_sprite(0, 165, self.width, self.height, LIME)

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

class Library(pygame.sprite.Sprite):
    def __init__(self, game, x,y):
        self.game = game
        self._layer = LIBRARY_LAYER
        self.groups = self.game.all_sprites, self.game.libraries
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.width = TILESIZE
        self.height = TILESIZE

        self.image = pygame.image.load('static/library.bmp')

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y


if __name__ == '__main__':
    p = Player(0,0)


