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
LEARNINGRATE = 0.1


class Agent:

    def __init__(self) -> None:
        self.game_amount = 0
        self.epsilon = 0.5 # controls randomness
        self.gamma = 0.8 #discount rate
        self.memory = deque(maxlen=MAX_MEMORY)
        self.model = Linear_QNet(8, 256, 4)
        self.trainer = QTrainer(self.model, lr=LEARNINGRATE, gamma=self.gamma)
        # if memory exceeded automatically removes it on the left

    def get_state(self, game: PySnake):
        upvec = pygame.Vector2(game.player_pos.x , game.player_pos.y - game.move_speed  )
        rightvec = pygame.Vector2(game.player_pos.x + game.move_speed , game.player_pos.y )
        downvec = pygame.Vector2(game.player_pos.x , game.player_pos.y + game.move_speed  )
        leftvec = pygame.Vector2(game.player_pos.x - game.move_speed , game.player_pos.y )
        up = game.create_rect_from_vec2(upvec, game.player_size)
        right = game.create_rect_from_vec2(rightvec, game.player_size)
        down = game.create_rect_from_vec2(downvec, game.player_size)
        left = game.create_rect_from_vec2(leftvec, game.player_size)
        state = [
            game.check_wall_collision(up),
            game.check_wall_collision(right),
            game.check_wall_collision(down),
            game.check_wall_collision(left),

            # game.check_food_collision(up),
            # game.check_food_collision(right),
            # game.check_food_collision(down),
            # game.check_food_collision(left),

            # game.check_poison_collision(up),
            # game.check_poison_collision(right),
            # game.check_poison_collision(down),
            # game.check_poison_collision(left),

            # game.player_pos.x,
            # game.player_pos.y,
            # game.food_pos.x,
            # game.food_pos.y,
            # game.player_pos.distance_to(game.food_pos),

            game.player_pos.x < game.food_pos.x,
            game.player_pos.x > game.food_pos.x,
            game.player_pos.y < game.food_pos.y,
            game.player_pos.y > game.food_pos.y,
        ] # all bools
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

    def get_action(self, state, game: PySnake) -> list[int]:
        predicted_move = [0,0,0,0]
        # 0 0 0 0 -> 1 0 0 0 up -> 0 1 0 0 -> right 0 0 1 0 -> down 0 0 0 1 -> left 
        if random.randint(0 , 100) < int(100 * self.epsilon):
            # x = game.best_action 
            # this would make the ai actually good lol
            x = random.randint(0,3)
            if x == 0:
                predicted_move[0] = 1
            elif x == 1:
                predicted_move[1] = 1
            elif x == 2:
                predicted_move[2] = 1
            elif x == 3:
                predicted_move[3] = 1
        else:
            current_state = torch.tensor(state, dtype=torch.float)
            prediction = self.model(current_state)
            pred_x = torch.argmax(prediction).item()
            predicted_move[pred_x] = 1
        return predicted_move 

def train():
    scores = []
    total_reward = 0
    best_score = 0
    agent = Agent()
    game = PySnake()
    while(True):
        # get old state
        current_state = agent.get_state(game)

        # get move
        move = agent.get_action(current_state, game)

        # perform move and get new state
        reward, done, score = game.ai_step(move)

        next_state = agent.get_state(game)

        total_reward += reward

        # train short memory
        agent.train_short_memory(current_state, move, reward, next_state, done)

        # remember
        agent.remember(current_state, move, reward, next_state, done)

        if done:
            # train long memory, plot result
            game.reset()
            agent.game_amount += 1
            agent.train_long_memory()
            
            score -= 10

            if score > best_score:
                best_score = score
                agent.model.save()

            print('Game', agent.game_amount,'Reward', total_reward,'Epsilon', agent.epsilon, 'Score', score, 'Record:', best_score)

            scores.append(score)
            print('All scores', scores)
            total_reward = 0
            if agent.epsilon >= 0.001:
                agent.epsilon -= 0.01
            else: 
                agent.epsilon = 0

if __name__ == '__main__':
    train()
