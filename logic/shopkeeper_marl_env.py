import gym
from gym import spaces
import numpy as np

class ShopkeeperEnv(gym.Env):
    def __init__(self):
        super().__init__()
        # Observation space: [distance_to_cat, current_speed]
        self.observation_space = spaces.Box(low=0, high=1600, shape=(2,), dtype=np.float32)
        # Action space: [-1 (decrease speed), 0 (maintain speed), 1 (increase speed)]
        self.action_space = spaces.Discrete(3)
        # Initialize environment variables
        self.distance_to_cat = np.random.uniform(1200, 1600)  # Initial distance
        self.current_speed = 3.0  # Starting speed
        self.time_step = 0

    def step(self, action):
        # Update speed based on action
        if action == 0:  # Maintain speed
            pass
        elif action == 1:  # Increase swgpeed
            self.current_speed += 0.2
        elif action == 2:  # Decrease speed
            self.current_speed -= 0.2
        self.current_speed = np.clip(self.current_speed, 3.0, 6.0)  # Limit speed range

        # Adjust speed more aggressively as distance decreases
        if self.distance_to_cat < 1000:
            self.current_speed = min(self.current_speed + 0.1, 6.0)
        if self.distance_to_cat < 600:
            self.current_speed = min(self.current_speed + 0.2, 6.0)

        # Update distance based on current speed
        self.distance_to_cat -= self.current_speed
        self.time_step += 1

        # Calculate reward
        if self.distance_to_cat <= 0:
            reward = 100  # Large reward for catching the cat
        else:
            reward = -self.distance_to_cat  # Penalize remaining distance

        # Done if the shopkeeper reaches the cat
        done = self.distance_to_cat <= 0 or self.time_step >= 200

        # Observation: [distance_to_cat, current_speed]
        state = np.array([self.distance_to_cat, self.current_speed], dtype=np.float32)

        return state, reward, done, {}

    def reset(self):
        self.distance_to_cat = np.random.uniform(1200, 1600)
        self.current_speed = 3.0
        self.time_step = 0
        return np.array([self.distance_to_cat, self.current_speed], dtype=np.float32)

    def render(self, mode="human"):
        print(f"Distance to cat: {self.distance_to_cat:.2f}, Current speed: {self.current_speed:.2f}")
