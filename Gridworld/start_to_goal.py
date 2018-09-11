import numpy as np

gridworld = [[3,3,3,3,3,3,3,3,3,3],
             [3,0,0,0,0,0,0,0,0,3],
             [3,0,0,0,0,0,0,0,0,3],
             [3,0,0,0,1,0,0,0,0,3],
             [3,0,0,0,1,0,0,0,0,3],
             [3,0,1,1,1,1,1,0,0,3],
             [3,0,0,0,1,0,0,0,0,3],
             [3,0,0,0,1,0,0,0,0,3],
             [3,0,0,0,0,0,0,0,2,3],
             [3,3,3,3,3,3,3,3,3,3]]
gridworld = np.array(gridworld)

rewards = {
    0: -1,
    1: -10,
    2: 100,
    3: -50
}

# E, W, S, N, SE, SW, NW, NE
actions = [( 1,  0), (-1,  0), ( 0,  1), ( 0, -1),
		   ( 1,  1), ( 1, -1), ( 1,  1), (-1,  1)]
# a = list(actions.keys())

lr = 0.2
df = 0.8

# random action values
# Initialize Q arbitrarily
Q = np.zeros((10, 10 ,8))


# For each episode
for episode in range(10000):
    # Initialise s
    # i = random.randint(1,9)
    # j = random.randint(1,9)
    i,j = 1,1

    # For each episode
    while True:
        # choose a from s using policy derived from Q
        # e-greedy
        e = 0.1
        if np.random.uniform() > e:
            action = np.argmax(Q[i,j])
        else:
            action = np.random.randint(0,4)

        # Take action
        # Observe next state
        i_n, j_n = i+actions[action][0], j+actions[action][1]
        # Observe Reward
        reward = rewards[gridworld[i_n, j_n]]

        Q[i][j][action] = (1 - lr) * Q[i][j][action] + lr * (reward + df * np.max(Q[i_n, j_n]))

        i, j = i_n, j_n

        if gridworld[i,j] in [2,3]:
            break;



policy = np.argmax(Q, axis= 2)
print(policy.T)

x, y = 1, 1
gridworld[x][y] = "9"
while True:
    action = policy[x,y]
    gridworld[x,y] = "8"

    x += actions[action][0]
    y += actions[action][1]

    if gridworld[x,y] in [2,3]:
        print("Out of the world.")
        break;
    gridworld[x,y] = "9"


print("Move: ", (i+1), ", Action: ", actions[action])
print(gridworld.T)
