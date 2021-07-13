import pygame
import gym
from sprites import *
from config import *
from gym import spaces
import numpy as np
import sys
import os

#  = os.path.join('static', 'city.bmp')
# adventurer_sprites = os.path.join('static', 'sprites', 'adventurer')

class Game(gym.Env):
    worldx = 640
    worldy = 480

    def __init__(self, is_ml=False, max_sources = 2):
        self.max_sources = max_sources
        self.is_ml = is_ml
        self.initialize_values()
        observation_space_dct = {
            'player_x': spaces.Box(-1,1, shape=(1,)),
            'player_y': spaces.Box(-1, 1, shape=(1,)),
            'player_direction': spaces.Box(-1, 1, shape=(1,))
        }
       # for idx in range(self.max_sources):
            # add in source info as needed
        mins = np.array([x.low[0] for x in observation_space_dct.values()])
        maxs = np.array([x.high[0] for x in observation_space_dct.values()])

        self.observation_space = spaces.Box(mins, maxs, dtype=np.float32)

        self.action_space = spaces.MultiDiscrete([5,3])
        self.available_actions = [[None, MOVE_LEFT, MOVE_RIGHT, MOVE_UP, MOVE_DOWN], [None, ASK, ANSWER]]

        self.reward_range = (-float(5), float(5))


    def action_mapper(self, action_array):
        actions_to_return = []
        for idx, i in enumerate(action_array):
            if round >= i:
                actions_to_return.append(self.available_actions[idx][i])
        return actions_to_return

    def create_tilemap(self):
        for i, row in enumerate(tilemap):
            for j, column in enumerate(row):
                Ground(self,j,i)
                if column == 'B':
                    Block(self, j, i)
                if column == 'P':
                    Player(self, j, i)
                if column == 'S':
                    Source(self, j, i)
                if column == 'L':
                    Library(self, j, i)



    def initialize_values(self):
        pygame.init()
        pygame.font.init()

        self.loop = 0
        self.time = 60
        self.fps = 60
        self.clock = pygame.time.Clock()

        self.world = pygame.display.set_mode([self.worldx, self.worldy])


        self.character_spritesheet = Spritesheet('static/spy_sprite_sheet.bmp')
        self.terrain_spritesheet = Spritesheet('static/terrain_sprite_sheet.bmp')



        self.all_sprites = pygame.sprite.LayeredUpdates()
        self.blocks = pygame.sprite.LayeredUpdates()
        self.players = pygame.sprite.LayeredUpdates()
        self.sources = pygame.sprite.LayeredUpdates()
        self.libraries = pygame.sprite.LayeredUpdates()

        self.running = True

        self.create_tilemap()


    def get_actions(self):
        player_actions = []
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            player_actions.append(MOVE_LEFT)
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            player_actions.append(MOVE_RIGHT)
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            player_actions.append(MOVE_UP)
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            player_actions.append(MOVE_DOWN)
        if keys[pygame.K_SPACE]:
            player_actions.append(QUESTION)
        # if keys[pygame.K_x]:
        #     player_actions.append(ANSWER)
        return player_actions

    def render(self, custom_message=None, **kwargs):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                self.running = False
                sys.exit()

        for p in self.players:
            p.movement(actions=self.get_actions())

        self.all_sprites.update()

        self.world.fill(BLACK)
        self.all_sprites.draw(self.world)

        self.clock.tick(self.fps)
        pygame.display.update()




    def step(self, action):
        self.loop += 1
        reward = 0
        attained_score = 0
        if self.is_ml:
            action = self.action_mapper(action)

        if action is None:
            action = []
        self.actions = action

#        self.player.control(action)




if __name__ == '__main__':
    game = Game(is_ml=False)
    game.step(action=[])
    loop = 0
    while game.running:
        loop += 1
        actions = game.get_actions()
        game.step(action=actions)
        game.render()




