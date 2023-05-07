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

pygame.init()

class Move:
    # 0 means no change
    # 1 means positive change -> up or right
    # -1 means negative change -> down or left
    x = 0
    y = 0

    def __init__(self,new_x = 0,new_y = 0):
        self.x = new_x
        self.y = new_y

    def get_pos(self):
        return (self.x,self.y)

class PySnake:
    # pygame.init()
    def __init__(self):
        self.screen = pygame.display.set_mode((1920, 1080))
        self.clock = pygame.time.Clock()
        self.dt = 1
        self.screen_width = self.screen.get_width()
        self.screen_height = self.screen.get_height()
        self.move_speed = 7
        self.reset()
    
    def reset(self):
        self.player_pos = pygame.Vector2(self.screen_width / 2, self.screen_height / 2)
        self.food_pos = pygame.Vector2(0,0)
        self.poison_pos = pygame.Vector2(0,0)
        self.reward = 0
        self.walls = [] 
        self.food = None
        self.poison = None
        self.running = True
        self.player_size = 10
        self.has_food = False
        self.has_poison = False
        self.game_over = False


    def game_loop(self, human = False, move: list[int] = [0,0,0,0,0,0]):
        # pygame setup
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

            self.update_screen()
            wall_col = self.check_wall_collision(self.player)
            self.check_food_collision(self.player)
            self.check_poison_collision(self.player)
            self.reset_interacts()
            if human:
                self.human_input()
            else: 
                self.ai_input(move)
            if wall_col and human:
                pygame.quit()
                quit()
            if not human:
                return
        pygame.quit()
        quit()


    def human_input(self): 
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            self.player_pos.y -= self.move_speed * self.dt
        if keys[pygame.K_s]:
            self.player_pos.y += self.move_speed * self.dt
        if keys[pygame.K_a]:
            self.player_pos.x -= self.move_speed * self.dt
        if keys[pygame.K_d]:
            self.player_pos.x += self.move_speed * self.dt
        
        pygame.display.flip()
        
        self.clock.tick(60)
        

    def ai_input(self,move: list[int]):
        if move[0] == 1:
            self.player_pos.x -= float(self.move_speed * self.dt)
        elif move[1] == 1:
            return
        elif move[2] == 1:
            self.player_pos.x += float(self.move_speed * self.dt)
        elif move[3] == 1:
            self.player_pos.y -= float(self.move_speed * self.dt)
        elif move[4] == 1:
            return
        elif move[5] == 1:
            self.player_pos.y += float(self.move_speed * self.dt)

    def ai_step(self, move: list[int]):
        self.reward = 0
        self.game_loop(False,move)

        return (self.reward, self.game_over, self.player_size)

    def check_wall_collision(self, rect: pygame.Rect):
        if rect.collidelist(self.walls) != -1:
            self.game_over = True
            self.reward = -1000
            return True
        return False

    def check_food_collision(self, rect: pygame.Rect):   
        if self.has_food and self.food != None and rect.collideobjects([self.food]) != None:
            self.player_size += 5
            self.reward = 10
            self.has_food = False
            return True
        return False
        
    def check_poison_collision(self, rect: pygame.Rect):   
        if self.has_poison and self.poison != None and rect.collideobjects([self.poison]) != None:
            self.player_size -= 5
            self.reward = -10
            if self.player_size < 0:
                pygame.quit()
            self.has_poison = False
            return True
        return False

    def create_rect_from_vec2(self, vec: pygame.Vector2, size):
        return pygame.Rect(vec.x,vec.y,size,size)

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


