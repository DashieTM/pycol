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
#
import torch
import pygame
import numpy as np
import random
from collections import deque
from game import PySnake, Move
from model import Linear_QNet, QTrainer

MAX_MEMORY = 100_000
BATCH_SIZE = 1000
LEARNINGRATE = 0.001


class Agent:

    def __init__(self) -> None:
        self.game_amount = 0
        self.epsilon = 0 # controls randomness
        self.gamma = 0.9 #discount
        self.memory = deque(maxlen=MAX_MEMORY)
        self.model = Linear_QNet(24, 256, 3)
        self.trainer = QTrainer(self.model, lr=LEARNINGRATE, gamma=self.gamma)
        # if memory exceeded automatically removes it on the left

    def get_state(self, game: PySnake):
        up = game.create_rect_from_vec2(pygame.Vector2(game.player_pos.x , game.player_pos.y + game.move_speed  ), game.player_size)
        up_right = game.create_rect_from_vec2(pygame.Vector2(game.player_pos.x + game.move_speed , game.player_pos.y + game.move_speed  ), game.player_size)
        up_left = game.create_rect_from_vec2(pygame.Vector2(game.player_pos.x - game.move_speed , game.player_pos.y + game.move_speed  ), game.player_size)
        right = game.create_rect_from_vec2(pygame.Vector2(game.player_pos.x + game.move_speed , game.player_pos.y ), game.player_size)
        down = game.create_rect_from_vec2(pygame.Vector2(game.player_pos.x , game.player_pos.y - game.move_speed  ), game.player_size)
        down_right = game.create_rect_from_vec2(pygame.Vector2(game.player_pos.x + game.move_speed , game.player_pos.y - game.move_speed  ), game.player_size)
        down_left = game.create_rect_from_vec2(pygame.Vector2(game.player_pos.x - game.move_speed , game.player_pos.y - game.move_speed  ), game.player_size)
        left = game.create_rect_from_vec2(pygame.Vector2(game.player_pos.x - game.move_speed , game.player_pos.y ), game.player_size)
        state = [
            game.check_wall_collision(up),
            game.check_wall_collision(up_right),
            game.check_wall_collision(up_left),
            game.check_wall_collision(right),
            game.check_wall_collision(down),
            game.check_wall_collision(down_right),
            game.check_wall_collision(down_left),
            game.check_wall_collision(left),

            game.check_food_collision(up),
            game.check_food_collision(up_right),
            game.check_food_collision(up_left),
            game.check_food_collision(right),
            game.check_food_collision(down),
            game.check_food_collision(down_right),
            game.check_food_collision(down_left),
            game.check_food_collision(left),

            game.check_poison_collision(up),
            game.check_poison_collision(up_right),
            game.check_poison_collision(up_left),
            game.check_poison_collision(right),
            game.check_poison_collision(down),
            game.check_poison_collision(down_right),
            game.check_poison_collision(down_left),
            game.check_poison_collision(left),
        ]
        return np.array(state, dtype=int)

    def remember(self,state,action,reward,next_state,done):
        self.memory.append((state, action, reward, next_state, done)) # popleft if MAX_MEMORY is reached

    def train_long_memory(self):
        if len(self.memory) > BATCH_SIZE:
            mini_sample = random.sample(self.memory, BATCH_SIZE) # list of tuples
        else:
            mini_sample = self.memory

        states, actions, rewards, next_states, dones = zip(*mini_sample)
        self.trainer.train_step(states, actions, rewards, next_states, dones)
        #for state, action, reward, nexrt_state, done in mini_sample:
        #    self.trainer.train_step(state, action, reward, next_state, done)

    def train_short_memory(self,state,action,reward,next_state,done):
        self.trainer.train_step(state, action, reward, next_state, done)
        pass

    def get_action(self, state) -> Move:
        self.epsilon = 80 - self.game_amount
        x = 0
        y = 0
        if random.randint(0, 200) < self.epsilon:
            x = random.randint(-1,1)
            y = random.randint(-1,1)
            return Move(x,y)
        else:
            predicted_move = [0,0,0,0,0,0]
            # 0 0 0 0 0 0 -> first 3 change of x
            # -1 0 1 
            current_state = torch.tensor(state, dtype=torch.float)
            prediction = self.model(current_state)
            # TODO how maek both direction?
            pred_x = torch.argmax(prediction).item()
            pred_y = torch.argmax(prediction).item()
            predicted_move[pred_x] = 1
            predicted_move[pred_y] = 1
            return to_move(list) 

def train():
    scores = []
    # mean_scores = []
    current_score = 0
    best_score = 0
    agent = Agent()
    game = PySnake() 
    while(True):
        # get old state
        current_state = agent.get_state(game)

        # get move
        move = agent.get_action(current_state)

        # perform move and get new state
        reward, done, score = game.ai_step(move)
        state_new = agent.get_state(game)

        # train short memory
        agent.train_short_memory(current_state, to_list(move), reward, state_new, done)

        # remember
        agent.remember(current_state, to_list(move), reward, state_new, done)

        if done:
            # train long memory, plot result
            # game.reset()
            game = PySnake()
            agent.game_amount += 1
            agent.train_long_memory()

            if score > best_score:
                best_score = score
                agent.model.save()

            print('Game', agent.game_amount, 'Score', score, 'Record:', best_score)

            scores.append(score)
            print('All scores', scores)
            current_score += score
            # mean_score = current_score / agent.game_amount
            # plot_mean_scores.append(mean_score)
            # plot(plot_scores, plot_mean_scores)

def to_move(list) -> Move:
    return Move(list[0], list[1])

def to_list(move: Move):
    x,y = move.get_pos()
    return [x,y]

if __name__ == '__main__':
    train()
