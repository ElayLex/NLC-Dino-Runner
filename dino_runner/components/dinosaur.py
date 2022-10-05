import pygame

from pygame.sprite import Sprite
from sre_constants import JUMP
from dino_runner.utils.constants import RUNNING 
from dino_runner.utils.constants import JUMPING
from dino_runner.utils.constants import DUCKING 

class Dinosaur(Sprite):
    X_POS = 80
    Y_POS = 310
    Y_POS_DUCK = 350
    JUMP_VEL = 8.5
    DUCK_VEL = 8.5
    
    def __init__(self):
        self.image = RUNNING[0]
        self.dino_rect = self.image.get_rect()
        self.dino_rect.x = self.X_POS
        self.dino_rect.y = self.Y_POS
        self.step_index = 0
        self.dino_run = True
        self.dino_jum = False
        self.jump_vel = self.JUMP_VEL
        self.dino_duck = False
        self.duck_vel = self.DUCK_VEL
        self.actions = self.actions

    def actions(self):
        if self.dino_run:
            self.run()
        elif self.dino_jum:
            self.jump()
        elif self.dino_duck:
            self.duck()

    def update(self, user_imput):
        self.actions()
        # if self.dino_run:
        #     self.run()
        # elif self.dino_jum:
        #     self.jump()
        # elif self.dino_duck:
        #     self.duck()

        if user_imput[pygame.K_UP] and not self.dino_jum:
            self.dino_jum = True
            self.dino_run = False
            self.dino_duck = False
        elif not self.dino_jum:
            self.dino_jum = False
            self.dino_run = True
            self.dino_duck = False

        if user_imput[pygame.K_DOWN] and not self.dino_duck:
            self.dino_duck = True
            self.dino_run = False
        elif not self.dino_duck:
            self.dino_duck = False
            self.dinno_run = True

        if self.step_index >= 10:
            self.step_index = 0

    def jump(self):
        self.image = JUMPING
        if self.dino_jum:
            self.dino_rect.y -= self.jump_vel * 4
            self.jump_vel -= 0.8

        
        if self.jump_vel < -self.JUMP_VEL:
            self.dino_rect.y = self.Y_POS
            self.dino_jum = False
            self.jump_vel = self.JUMP_VEL

    def run(self):
        self.image = RUNNING[0] if self.step_index < 5 else RUNNING[1]
        self.dino_rect = self.image.get_rect()
        self.dino_rect.x = self.X_POS
        self.dino_rect.y = self.Y_POS
        self.step_index += 1

    def duck(self):
        self.image = DUCKING[0] if self.step_index == pygame.K_DOWN else DUCKING[1]
        self.dino_rect = self.image.get_rect()
        self.dino_rect.x = self.X_POS
        self.dino_rect.y = self.Y_POS_DUCK
        self.step_index += 1

    def draw(self, screen: pygame.Surface):
        screen.blit(self.image, (self.dino_rect.x, self.dino_rect.y))
