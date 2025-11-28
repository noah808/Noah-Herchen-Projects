import pandas as pd
from tensorflow.keras.models import Sequential, load_model
from tensorflow.keras.layers import Dense, Flatten
import tensorflow.keras
import rl
from rl.agents import DQNAgent
from rl.policy import BoltzmannQPolicy
from rl.memory import SequentialMemory

import tensorflow as tf
from sklearn.metrics import accuracy_score
import cv2 as cv
import os
import numpy as np
import gym
import random

env = gym.make("CartPole-v1")

states = env.observation_space.shape[0]
actions = env.action_space.n

model = Sequential()
model.add(Flatten(input_shape = (1, states)))
model.add(Dense(24, activation = "relu"))
model.add(Dense(24, activation = "relu"))
model.add(Dense(2, activation = "linear"))

agent = DQNAgent(
    model = model,
    memory = SequentialMemory(50000, window_length = 1), 
    policy = BoltzmannQPolicy(), 
    nb_actions = actions, 
    nb_steps_warmup = 10, 
    target_model_update = 0.01
)

agent.compile(tf.keras.optimizers.legacy.Adam(lr = 0.001), metrics = ["mae"])
agent.fit(env, nb_steps = 40000, visualize = False, verbose=1)

results = agent.test(env, nb_episodes = 10, visualize = True)
print(np.mean(results.history["episode_reward"]))

env.close()


#episodes = 10

#for episode in range(1, episodes+1):
#    state = env.reset()
#    done = False
#    score = 0
#    while not done:
#        action = random.choice([0, 1])
#        _, reward, done, _ =env.step(action)
#        score+=reward
#        env.render()
#    print(f"Episode {episode}, Score: {score}")

#env.close()
