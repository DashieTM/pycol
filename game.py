# Copyright © 2023 Kaj Habegger, Fabio Lenherr
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

import pygame
import random
from actor import Move

class PySnake:
    pygame.init()
    screen = pygame.display.set_mode((1280, 720))
    clock = pygame.time.Clock()
    running = True
    player_size = 10
    has_food = False
    has_poison = False
    dt = 1
    screen_width = screen.get_width()
    screen_height = screen.get_height()
    player_pos = pygame.Vector2(screen_width / 2, screen_height / 2)
    food_pos = pygame.Vector2(0,0)
    poison_pos = pygame.Vector2(0,0)

    def game_loop(self, human = False):
        # pygame setup
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

                self.update_screen()
                self.check_collision()
                self.reset_interacts()

                if (human == True):
                    self.human_input()

        pygame.quit()


    def human_input(self): 
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            self.player_pos.y -= 10 * self.dt
        if keys[pygame.K_s]:
            self.player_pos.y += 10 * self.dt
        if keys[pygame.K_a]:
            self.player_pos.x -= 10 * self.dt
        if keys[pygame.K_d]:
            self.player_pos.x += 10 * self.dt
        
        pygame.display.flip()
        
        self.clock.tick(180)
        

    def ai_input(self,move: Move):
        x,y = move.get_pos()
        self.player_pos.y += y * 10 *self.dt
        self.player_pos.x += x * 10 *self.dt

    def check_collision(self):
        if self.player.collidelist(self.walls) != -1:
            pygame.quit()
        
        if self.has_food and self.player.collideobjects([self.food]) != None:
            self.player_size += 5
            self.has_food = False
        
        if self.has_poison and self.player.collideobjects([self.poison]) != None:
            self.player_size -= 5
            if self.player_size < 0:
                pygame.quit()
            self.has_poison = False

    def update_screen(self):
        self.screen.fill("black")

        self.walls = [] 
        self.walls.append(pygame.draw.line(self.screen, "red", (0,self.screen_height) , (self.screen_width,self.screen_height),5))
        self.walls.append(pygame.draw.line(self.screen, "red", (0,0) , (0,self.screen_height),5))
        self.walls.append(pygame.draw.line(self.screen, "red", (0,0) , (self.screen_width,0),5))
        self.walls.append(pygame.draw.line(self.screen, "red", (self.screen_width,0) , (self.screen_width,self.screen_height),5))
        
        
        self.player = pygame.draw.circle(self.screen, "blue", self.player_pos, self.player_size)
        
        self.food = None
        if self.has_food:
            self.food = pygame.draw.circle(self.screen, "green", self.food_pos, 20)
        
        self.poison = None
        if self.has_poison:
            self.poison = pygame.draw.circle(self.screen, "red", self.poison_pos, 20)
 

    def reset_interacts(self):
        if not self.has_food:
            self.food_pos = pygame.Vector2(random.randint(0,self.screen.get_width()), random.randint(0,self.screen.get_height()))
            self.has_food = True

        if not self.has_poison:
            self.poison_pos = pygame.Vector2(random.randint(0,self.screen.get_width()), random.randint(0,self.screen.get_height()))
            self.has_poison = True


