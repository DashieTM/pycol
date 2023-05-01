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
dt = 1
player_pos = pygame.Vector2(screen.get_width() / 2, screen.get_height() / 2)
food_pos = pygame.Vector2(0,0)

while running:
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    # fill the screen with a color to wipe away anything from last frame
    screen.fill("purple")

    # walls = [pygame.Vector2(0,0)]
    # walls.append(pygame.draw.line(screen, "red", (0,0) , (100,100),1))
    # walls.append(pygame.draw.line(screen, "red", (0,0) , (0,100),1))
    # walls.append(pygame.draw.line(screen, "red", (0,0) , (100,0),1))
    # walls.append(pygame.draw.line(screen, "red", (100,0) , (100,100),1))

    

    pygame.draw.circle(screen, "red", player_pos, player_size)
    pygame.draw.circle(screen, "green", food_pos, 20)
    
    if not has_food:
        food_pos = pygame.Vector2(random.randint(0,screen.get_width()), random.randint(0,screen.get_height()))
        has_food = True

    distance = (food_pos - player_pos).length()
    if distance - player_size < 1: 
        player_size += 5
        has_food = False
   
    # distance_wall = 40
    # for i in range(0,3):
    #     current_distance_wall = (walls[i] - player_pos).length()
    #     if current_distance_wall < distance_wall:
    #         distance_wall = current_distance_wall
    #     if distance_wall - player_size <5:
    #         pygame.quit()
    #
    #
    # if distance_wall - player_size < 5:
    #     pygame.quit()

    keys = pygame.key.get_pressed()
    if keys[pygame.K_w]:
        player_pos.y -= 10 * dt
    if keys[pygame.K_s]:
        player_pos.y += 10 * dt
    if keys[pygame.K_a]:
        player_pos.x -= 10 * dt
    if keys[pygame.K_d]:
        player_pos.x += 10 * dt

    # RENDER YOUR GAME HERE

    # flip() the display to put your work on screen
    pygame.display.flip()

    clock.tick(60)  # limits FPS to 60

pygame.quit()
