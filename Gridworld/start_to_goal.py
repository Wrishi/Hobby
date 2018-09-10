import numpy as np

gridworld = [[3,3,3,3,3,3,3,3,3,3],
             [3,0,0,0,0,0,0,0,0,3],
             [3,0,0,0,0,0,0,0,0,3],
             [3,0,0,0,1,0,0,0,0,3],
             [3,0,0,0,1,0,0,0,0,3],
             [3,0,0,0,1,0,0,0,0,3],
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

# E, W, S, N
actions = [( 1,  0), (-1,  0), ( 0,  1), ( 0, -1)]
# a = list(actions.keys())

lr = 0.2
df = 0.8
# random action values
Q = np.random.rand(10, 10 ,4)

for i in range(10):
    for j in range(10):
        for a in actions:
            # a for which Q[i+x][j+y] is maximum
            r = rewards[gridworld[i][j]]
            Q[i][j][a] = (1 - lr) * Q[i][j][a] + lr * (r + df * np.max(Q[i+a[0]][j+a[1]]))

policy = np.max(Q)

x, y = 0, 0
gridworld[x][y] = "4"
for i in range(10):
    # action = np.random.choice(a)
    gridworld[x][y] = "3"

    x += actions[action][0]
    y += actions[action][1]

    if x > 9 or x < 0 or y > 9 or y < 0 or gridworld[x][y] == 2:
        print("Out of the world.")
        break;
    gridworld[x][y] = "4"

    print("Move: ", (i+1), ", Action: ", actions[action])
    print(gridworld.T)
