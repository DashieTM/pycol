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

# import torch
# print(torch.cuda.is_available())
# x = torch.rand(5, 3)
# print(x)
import pygame
import random

# pygame setup
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

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    screen.fill("black")

    walls = [] 
    walls.append(pygame.draw.line(screen, "red", (0,screen_height) , (screen_width,screen_height),5))
    walls.append(pygame.draw.line(screen, "red", (0,0) , (0,screen_height),5))
    walls.append(pygame.draw.line(screen, "red", (0,0) , (screen_width,0),5))
    walls.append(pygame.draw.line(screen, "red", (screen_width,0) , (screen_width,screen_height),5))

    
    player = pygame.draw.circle(screen, "blue", player_pos, player_size)

    food = None
    if has_food:
        food = pygame.draw.circle(screen, "green", food_pos, 20)
    
    poison = None
    if has_poison:
        poison = pygame.draw.circle(screen, "red", poison_pos, 20)

    if player.collidelist(walls) != -1:
        pygame.quit()

    if has_food and player.collideobjects([food]) != None:
        player_size += 5
        has_food = False

    if not has_food:
        food_pos = pygame.Vector2(random.randint(0,screen.get_width()), random.randint(0,screen.get_height()))
        has_food = True

    if has_poison and player.collideobjects([poison]) != None:
        player_size -= 5
        if player_size < 0:
            pygame.quit()
        has_poison = False

    if not has_poison:
        poison_pos = pygame.Vector2(random.randint(0,screen.get_width()), random.randint(0,screen.get_height()))
        has_poison = True

    keys = pygame.key.get_pressed()
    if keys[pygame.K_w]:
        player_pos.y -= 10 * dt
    if keys[pygame.K_s]:
        player_pos.y += 10 * dt
    if keys[pygame.K_a]:
        player_pos.x -= 10 * dt
    if keys[pygame.K_d]:
        player_pos.x += 10 * dt

    pygame.display.flip()

    clock.tick(180)

pygame.quit()
