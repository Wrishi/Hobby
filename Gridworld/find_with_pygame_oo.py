import numpy as np
import pygame as pg

default = {
    "tilesize": 10,
    "rewards": {
        0: -1,
        1: -10,
        2: 100,
        3: -50
    },
    "actions": [( 1,  0), (-1,  0), ( 0,  1), ( 0, -1), ( 1,  1), ( 1, -1), ( 1,  1), (-1,  1)],
    "learning_rate": 0.2,
    "discount_factor": 0.8,
    "episodes": 10000,
    "map_colors": [
        (40,40,40),
        (212,96,20),
        (96,212,20),
        (0,0,0)
    ],
    "agent_colors": {
        "current": (96,20,212),
        "past": (45,10,112)
    }
}

pg.init()
class Agent:
    def __init__(self, gridworld, position, actions = default["actions"], learning_rate = default["learning_rate"], 
                discount_factor = default["discount_factor"], episodes = default["episodes"], colors = default["agent_colors"]):
        print("Initializing agent...")
        self.gridworld = gridworld
        self.position = position
        self.actions = actions
        self.learning_rate = learning_rate
        self.discount_factor = discount_factor
        self.episodes = episodes
        self.colors = colors
        self.draw_position(self.colors["current"])
        self.policy = self.get_policy()
        print("Agent initialized...")

    def get_policy(self):
        print("Determining policy...")
        lr = self.learning_rate
        df = self.discount_factor
        actions = self.actions
        rewards = self.gridworld.rewards
        gridworld = self.gridworld.gridworld
        gridworld_x = len(gridworld)
        gridworld_y = len(gridworld[0])

        # random action values
        # Initialize Q arbitrarily
        Q = np.zeros((gridworld_x, gridworld_y , len(actions)))


        # For each episode
        for episode in range(10000):
            i,j = self.position

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
        print("Policy determined...")
        return policy

    def draw_position(self, color):
        x,y = self.position
        dim = self.gridworld.tilesize
        win = self.gridworld.window
        pg.draw.rect(win, color, ((x+1) * dim, (y+1) * dim, dim, dim))
        pg.display.update()

    def move(self):
        x,y = self.position
        action = self.policy[x,y]
        x += self.actions[action][0]
        y += self.actions[action][1]
        self.position = (x,y)


    def play(self):
        print("Playing moves from policy...")
        run = True
        while run:
            pg.time.delay(100)
            self.draw_position(self.colors["past"])

            for event in pg.event.get():
                if event.type == pg.QUIT:
                    run = False

            
            self.move()

            x,y = self.position
            if self.gridworld.gridworld[x,y] in [2,3]:
                print("Out of the world.")
                run = False

            self.draw_position(self.colors["current"])

        print("Game over...")


class Gridworld:
    def __init__(self, mapfilename, rewards = default["rewards"], tilesize=default["tilesize"], colors=default["map_colors"]):
        self.tilesize = tilesize
        self.colors = colors
        self.gridworld = self.readmap(mapfilename)
        self.window = self.drawmap()
        self.rewards = rewards
        print("Gridworld initialized...")

    def readmap(self, mapfilename):
        gridworld = None
        with open(mapfilename, 'r') as file:
            gridworld = [[int(digit) for digit in line.split(",")] for line in file.read().split("\n")]
        gridworld = np.array(gridworld)
        print("Map loaded...")
        return gridworld

    def drawmap(self):
        dim = self.tilesize
        gridworld_x = len(self.gridworld)
        gridworld_y = len(self.gridworld[0])

        win = pg.display.set_mode(((gridworld_x + 1) * dim,(gridworld_y + 1) * dim))
        pg.display.set_caption("Find path")
        print(self.colors)
        for i in range(gridworld_x):
            for j in range(gridworld_y):
                color = self.colors[self.gridworld[i,j]]

                size = ((i+1) * dim, (j+1) * dim, dim, dim)
                pg.draw.rect(win, color, size)
                pg.display.update()
        print("Map drawn...")
        return win


gw = Gridworld("./basemap.txt")
agent = Agent(gridworld = gw, position = (1,1))
agent.play()

# run = True
# while run:
#     pg.time.delay(100)
#     pg.draw.rect(win, (10,10,100), ((x+1) * dim, (y+1) * dim, dim, dim))
#     pg.display.update()

#     for event in pg.event.get():
#         if event.type == pg.QUIT:
#             run = False

#     action = policy[x,y]
#     x += actions[action][0]
#     y += actions[action][1]

#     if gridworld[x,y] in [2,3]:
#         print("Out of the world.")
#         run = False

#     pg.draw.rect(win, (10,10,200), ((x+1) * dim, (y+1) * dim, dim, dim))
    
input()
pg.quit()

# with open('./basemap.txt', 'r') as file:
#     # print( file.read().split("\n")[0])
#     gridworld = [[int(digit) for digit in line.split(",")] for line in file.read().split("\n")]

# gridworld = np.array(gridworld)
# gridworld_x = len(gridworld)
# gridworld_y = len(gridworld[0])
# # print(gridworld)

# dim = 10
# pg.init()
# win = pg.display.set_mode(((gridworld_x + 1) * dim,(gridworld_y + 1) * dim))
# pg.display.set_caption("Find path")

# for i in range(gridworld_x):
#     for j in range(gridworld_y):
#         color = (0,0,0)
#         if gridworld[i,j] == 0:
#             color = (24,24,24)
#         elif gridworld[i,j] == 1:
#             color = (200,10,10)
#         elif gridworld[i,j] == 2:
#             color = (10,200,10)

#         size = ((i+1) * dim, (j+1) * dim, dim, dim)
#         pg.draw.rect(win, color, size)
#         pg.display.update()

# x, y = 1, 1
# pg.draw.rect(win, (10,10,200), ((x+1) * dim, (y+1) * dim, dim, dim))
# pg.display.update()

# rewards = {
#     0: -1,
#     1: -10,
#     2: 100,
#     3: -50
# }

# # E, W, S, N, SE, SW, NW, NE
# actions = [( 1,  0), (-1,  0), ( 0,  1), ( 0, -1),
# 		   ( 1,  1), ( 1, -1), ( 1,  1), (-1,  1)]
# # a = list(actions.keys())

# lr = 0.2
# df = 0.8

# # random action values
# # Initialize Q arbitrarily
# Q = np.zeros((gridworld_x, gridworld_y , len(actions)))


# # For each episode
# for episode in range(10000):
#     # Initialise s
#     # i = random.randint(1,9)
#     # j = random.randint(1,9)
#     i,j = 1,1

#     # For each episode
#     while True:
#         # choose a from s using policy derived from Q
#         # e-greedy
#         e = 0.1
#         if np.random.uniform() > e:
#             action = np.argmax(Q[i,j])
#         else:
#             action = np.random.randint(0,4)

#         # Take action
#         # Observe next state
#         i_n, j_n = i+actions[action][0], j+actions[action][1]
#         # Observe Reward
#         reward = rewards[gridworld[i_n, j_n]]

#         Q[i][j][action] = (1 - lr) * Q[i][j][action] + lr * (reward + df * np.max(Q[i_n, j_n]))

#         i, j = i_n, j_n

#         if gridworld[i,j] in [2,3]:
#             break;



# policy = np.argmax(Q, axis= 2)
# # print(policy.T)

# run = True
# while run:
#     pg.time.delay(100)
#     pg.draw.rect(win, (10,10,100), ((x+1) * dim, (y+1) * dim, dim, dim))
#     pg.display.update()

#     for event in pg.event.get():
#         if event.type == pg.QUIT:
#             run = False

#     action = policy[x,y]
#     x += actions[action][0]
#     y += actions[action][1]

#     if gridworld[x,y] in [2,3]:
#         print("Out of the world.")
#         run = False

#     pg.draw.rect(win, (10,10,200), ((x+1) * dim, (y+1) * dim, dim, dim))
    
input()
pg.quit()
