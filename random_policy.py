# this is a example code on how to use the environment.
# this code follow a random policy, means executes the random actions.


import numpy as np
import pandas as pd
import math
import pickle

# import the env class
from Paddle.paddle import Paddle

# create an object of env class
env = Paddle()
np.random.seed(0)

q_table = pd.DataFrame(0, columns=[0, 1, 2], index=["hit", "miss", "move_top_right_close", "move_top_left_close",
													"move_bot_right_close", "move_bot_left_close", "move_top_right_far",
													"move_top_left_far", "move_bot_right_far", "move_bot_left_far"])
gamma = 0.9
lr = 0.9
epsilon = 0.98
actions = [0, 1, 2]
print(q_table)


def decide_action(state):
	final_state = "hit"
	current_action = None
	curr_ball_dx = state[4]
	curr_ball_dy = state[3]
	curr_paddle_x = state[0]
	curr_ball_x = state[1]
	curr_ball_y = state[2]
	curr_state = state[5]
	if curr_state in q_table.index:
		pass

	return current_action


def choose_action(observation):
	# self.check_state_exist(observation)
	# Selection of the action - 90 % according to the epsilon == 0.9
	# Choosing the best action
	# print(observation)
	if np.random.uniform() < epsilon:
		state_action = q_table.loc[observation[-1], :]
		state_action = state_action.reindex(np.random.permutation(state_action.index))
		action = state_action.idxmax()
	else:
		# Choosing random action - left 10 % for choosing randomly
		action = np.random.choice(actions)
	return action


def learn(state, action, reward, next_state):
	q_predict = q_table.loc[state[-1], action]
	if next_state != 'miss':
		q_target = reward + gamma * q_table.loc[next_state[-1], :].max()
	else:
		q_target = reward
	q_table.loc[state[-1], action] += lr * (q_target - q_predict)
	return q_table.loc[state[-1], action]


def random_policy(episode):
	max_steps = 1000

	for e in range(episode):
		state = env.reset()
		score = 0

		while True:
			action = choose_action(state)
			# action = np.random.randint(action_space)
			reward, next_state, done, best = env.step(action)
			score += learn(state, action, reward, next_state)
			state = next_state
			if done:
				print("episode: {}/{}, score: {}".format(e, episode, score))
				break
		print(q_table)
		print("Current best score is: {}".format(best))


if __name__ == '__main__':
	random_policy(100000)
	q_table.to_pickle("q_table_final.pkl")
