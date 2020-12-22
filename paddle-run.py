from Paddle.paddle import Paddle
from agent import Agent


def update():
	# Resulted list for the plotting Episodes via Steps
	steps = []

	# Summed costs for all episodes in resulted list
	all_costs = []

	for episode in range(1000):
		# Initial Observation
		observation = env.reset()

		# Updating number of Steps for each Episode
		i = 0

		# Updating the cost for each episode
		cost = 0

		while True:
			# Refreshing environment
			env.render()

			# RL chooses action based on observation
			action = RL.choose_action(str(observation))

			# RL takes an action and get the next observation and reward
			observation_, reward, done = env.step(action)

			# RL learns from this transition and calculating the cost
			cost += RL.learn(str(observation), action, reward, str(observation_))

			# Swapping the observations - current and next
			observation = observation_

			# Calculating number of Steps in the current Episode
			i += 1

			# Break while loop when it is the end of current Episode
			# When agent reached the goal or obstacle
			if done:
				steps += [i]
				all_costs += [cost]
				break

	# Showing the final route
	env.final()

	# Showing the Q-table with values for each action
	RL.print_q_table()

	# Plotting the results
	RL.plot_results(steps, all_costs)


# Commands to be implemented after running this file
if __name__ == "__main__":
	# Calling for the environment
	env = Paddle()
	# Calling for the main algorithm
	RL = Agent(actions=list(range(3)), states=list(range(3)))
	# Running the main loop with Episodes by calling the function update()
	episode = 10
	max_steps = 1000
	for e in range(episode):
		observation = env.reset()
		score = 0

		for i in range(max_steps):
			action = RL.choose_action(observation)
			reward, next_state, done = env.step(action)
			score += reward
			state = next_state
			if done:
				print("episode: {}/{}, score: {}".format(e, episode, score))
				break
