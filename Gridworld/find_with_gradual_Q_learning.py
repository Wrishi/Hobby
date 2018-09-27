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
    "episodes": 100,
    "map_colors": [
        (40,40,40),
        (212,96,20),
        (96,212,20),
        (0,0,0)
    ],
    "agent_colors": {
        "current": (96,20,212),
        "past": (45,10,112)
    },
    "player_colors": {
        "current": (212,20,80),
        "past": (100,10,40)
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
        self.Q = self.init_Q()
        self.policy = self.get_policy()
        print("Agent initialized...")

    def init_Q(self):
        gridworld = self.gridworld.gridworld
        gridworld_x = len(gridworld)
        gridworld_y = len(gridworld[0])

        # random action values
        # Initialize Q arbitrarily
        Q = np.zeros((gridworld_x, gridworld_y , len(self.actions)))

        return Q

    def get_policy(self):
        print("Determining policy...")
        lr = self.learning_rate
        df = self.discount_factor
        actions = self.actions
        rewards = self.gridworld.rewards
        gridworld = self.gridworld.gridworld

        # For each episode
        for episode in range(self.episodes):
            i,j = self.position

            # For each episode
            while True:
                # choose a from s using policy derived from Q
                # e-greedy
                e = 0.4
                if np.random.uniform() > e:
                    action = np.argmax(self.Q[i,j])
                else:
                    action = np.random.randint(0,4)

                # Take action
                # Observe next state
                i_n, j_n = i+actions[action][0], j+actions[action][1]
                # Observe Reward
                reward = rewards[gridworld[i_n, j_n]]

                self.Q[i][j][action] = (1 - lr) * self.Q[i][j][action] + lr * (reward + df * np.max(self.Q[i_n, j_n]))

                i, j = i_n, j_n

                if gridworld[i,j] in [2,3]:
                    break;

        policy = np.argmax(self.Q, axis= 2)
        print("Policy determined...")
        return policy

    def draw_position(self, color):
        x,y = self.position
        dim = self.gridworld.tilesize
        win = self.gridworld.window
        pg.draw.rect(win, color, ((x+1) * dim, (y+1) * dim, dim, dim))
        pg.display.update()

    def move(self):
        run = True
        self.policy = self.get_policy()
        x,y = self.position
        action = self.policy[x,y]
        dx = self.actions[action][0]
        dy = self.actions[action][1]
        if self.gridworld.gridworld[x+dx,y+dy] == 1:
            return run
        x += dx
        y += dy
        self.position = (x,y)
        if self.gridworld.gridworld[x,y] in [2,3]:
            print("Out of the world.")
            run = False

        self.draw_position(self.colors["current"])

        return run



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
            text = file.read()
            if text[len(text)-1] == "\n":
                text = text[:len(text)-1]
            gridworld = [[int(digit) for digit in line.split(",")] for line in text.split("\n")]
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

class Player:
    def __init__(self, gridworld, position, colors=default["player_colors"] ):
        self.position = position
        self.gridworld = gridworld
        self.colors = colors
        self.draw_position(self.colors["current"])

    def draw_position(self, color):
        x,y = self.position
        dim = self.gridworld.tilesize
        win = self.gridworld.window
        pg.draw.rect(win, color, ((x+1) * dim, (y+1) * dim, dim, dim))
        pg.display.update()

    def move(self, dx, dy):
        run = True
        x,y = self.position
        if self.gridworld.gridworld[x+dx,y+dy] == 1:
            return run

        x += dx
        y += dy
        self.position = (x,y)

        if self.gridworld.gridworld[x,y] in [2,3]:
            print("Out of the world.")
            run = False

        self.draw_position(self.colors["current"])

        return run


class Game:
    def __init__(self):
        self.gw = Gridworld("./basemap.txt")
        self.agent = Agent(gridworld = self.gw, position = (1,1))
        self.player = Player(gridworld = self.gw, position = (1,2))

    def play(self):
        print("Playing moves from policy...")
        run = True
        while run:
            pg.time.delay(1)
            self.agent.draw_position(self.agent.colors["past"])

            for event in pg.event.get():
                if event.type == pg.QUIT:
                    run = False

            keys = pg.key.get_pressed()

            dx,dy = 0,0
            if keys[pg.K_LEFT]:
                dx -= 1
            if keys[pg.K_RIGHT]:
                dx += 1
            if keys[pg.K_UP]:
                dy -= 1
            if keys[pg.K_DOWN]:
                dy += 1

            run = self.player.move(dx,dy)
            run = self.agent.move()



        print("Game over...")


if __name__ == "__main__":
    g = Game()
    g.play()
    input()
    pg.quit()
