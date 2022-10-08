import pygame

from pygame.sprite import Sprite
from dino_runner.utils.constants import RUNNING, DUCKING , DEFAULT_TYPE, SHIELD_TYPE, RUNNING_SHIELD, DUCKING_SHIELD, JUMPING_SHIELD, HAMMER_TYPE, RUNNING_HAMMER, DUCKING_HAMMER, JUMPING_HAMMER
from dino_runner.utils.constants import JUMPING
from dino_runner.utils.constants import HAMMER

DUCK_IMG = {DEFAULT_TYPE: DUCKING, SHIELD_TYPE: DUCKING_SHIELD, HAMMER_TYPE: DUCKING_HAMMER}
JUMP_IMG = {DEFAULT_TYPE: JUMPING, SHIELD_TYPE: JUMPING_SHIELD, HAMMER_TYPE: JUMPING_HAMMER}
RUN_IMG = {DEFAULT_TYPE: RUNNING, SHIELD_TYPE: RUNNING_SHIELD, HAMMER_TYPE: RUNNING_HAMMER}
HAMMER_IMG = {DEFAULT_TYPE: RUNNING, SHIELD_TYPE: RUNNING, HAMMER_TYPE: RUNNING}
THROW_HAMMER = {HAMMER}

FONT_STYLE = 'freesansbold.ttf'


class Dinosaur(Sprite):
    X_POS = 80
    Y_POS = 310
    Y_POS_DUCK = 350
    JUMP_VEL = 8.5
    
    def __init__(self):
        self.type = DEFAULT_TYPE
        self.image = RUN_IMG[self.type][0]
        self.dino_rect = self.image.get_rect()
        self.dino_rect.x = self.X_POS
        self.dino_rect.y = self.Y_POS
        self.image = HAMMER
        self.hammer_rect = self.image.get_rect()
        self.hammer_rect.x = 600
        self.hammer_rect.y = 400
        self.step_index = 0
        self.dino_run = True
        self.dino_duck = False
        self.dino_jum = False
        self.dino_hammer = False
        self.jump_vel = self.JUMP_VEL
        self.setup_state()

        # self.sound = pygame.mixer.Sound('Descargas/1.mp3')

    def setup_state(self):
        self.has_power_up = False
        self.shield = False
        self.hammer = False
        self.show_text = False
        self.shield_time_up = 0

    def events(self):
        if self.dino_run:
            self.run()
        elif self.dino_jum:
            self.jump()
        elif self.dino_duck:
            self.duck()
        elif self.dino_hammer:
            self.hammmer()

    def update(self, user_imput):
        self.events()

        if user_imput[pygame.K_UP] and not self.dino_jum:
            self.dino_jum = True
            self.dino_run = False
            self.dino_duck = False
            self.dino_hammer = False
        elif user_imput[pygame.K_DOWN] and not self.dino_jum:
            self.dino_duck = True
            self.dino_run = False
            self.dino_jum = False
            self.dino_hammer = False
        elif user_imput[pygame.K_RIGHT]:
            self.dino_duck = False
            self.dino_run = False
            self.dino_jum = False
            self.dino_hammer = True

        elif not self.dino_jum:
            self.dino_jum = False
            self.dino_run = True
            self.dino_duck = False

        if self.step_index >= 10:
            self.step_index = 0

    def jump(self):
        self.image = JUMP_IMG[self.type]
        if self.dino_jum:
            self.dino_rect.y -= self.jump_vel * 4
            self.jump_vel -= 0.8
            
            # self.sound.play()

        if self.jump_vel < -self.JUMP_VEL:
            self.dino_rect.y = self.Y_POS
            self.dino_jum = False
            self.jump_vel = self.JUMP_VEL

    def run(self):
        self.image = RUN_IMG[self.type][self.step_index // 5]
        self.dino_rect = self.image.get_rect()
        self.dino_rect.x = self.X_POS
        self.dino_rect.y = self.Y_POS
        self.step_index += 1

    def duck(self):
        self.image = DUCK_IMG[self.type][self.step_index // 5]
        self.dino_rect = self.image.get_rect()
        self.dino_rect.x = self.X_POS
        self.dino_rect.y = self.Y_POS_DUCK
        self.step_index += 1
    
    def hammmer(self):
        self.image = HAMMER_IMG[self.type][self.step_index // 5]
        self.hammer_rect = self.image.get_rect()
        self.hammer_rect.x = self.X_POS
        self.hammer_rect.y = self.Y_POS
        self.step_index += 1
        # self.image = THROW_HAMMER
        # if self.dino_hammer:
        #     self.hammer_rect.x += self.jump_vel * 4
        #     self.jump_vel += 0.8

    def draw(self, screen: pygame.Surface):
        screen.blit(self.image, (self.dino_rect.x, self.dino_rect.y))
        if self.dino_hammer == True:
            screen.blit(HAMMER, (self.hammer_rect.x, self.hammer_rect.y))

    def check_invicibility(self, screen):
        if self.shield == True:
            time_to_show = round((self.shield_time_up - pygame.time.get_ticks()) / 100, 2)
            if time_to_show >= 0 and self.show_text:   
            # mostrar este tiempo en el juego
                font = pygame.font.Font(FONT_STYLE, 25)
                text = font.render(f"Remaining special power time: {time_to_show}", True, (2, 65, 35))
                text_rect = text.get_rect()
                text_rect.center = (550, 50)
                screen.blit(text, text_rect)
            else:
                self.shield = False
                self.type = DEFAULT_TYPE 
  