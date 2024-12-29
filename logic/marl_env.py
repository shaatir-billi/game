
import gym
from gym import spaces
import numpy as np
import pygame
import math

# Constants from the configuration
SCREEN_WIDTH = 1600
SCREEN_HEIGHT = 900
MAP_WIDTH = 4000
SKY_IMAGE_PATH = "assets/map/sky.jpeg"
ENABLE_GRAPH_VISUALIZATION = True

class CatChaseEnv(gym.Env):
    """
    Custom Environment for the Cat Chase scenario.
    """
    def __init__(self, cat_position, shopkeeper_position, guard_positions):
        super().__init__()

        # Initial positions
        self.initial_cat_position = cat_position
        self.initial_shopkeeper_position = shopkeeper_position
        self.initial_guard_positions = guard_positions

        # Current positions
        self.cat_position = list(cat_position)
        self.shopkeeper_position = list(shopkeeper_position)
        self.guard_positions = [list(pos) for pos in guard_positions]
        self.num_guards = len(guard_positions)
        
        # Initialize previous distance to cat for reward comparison
        self.previous_distance_to_cat = np.linalg.norm(np.array(self.shopkeeper_position) - np.array(self.cat_position))

        # Define observation and action spaces
        self.observation_space = spaces.Box(low=-MAP_WIDTH, high=MAP_WIDTH, shape=(4 + 2 * self.num_guards,), dtype=np.float32)
        self.action_space = spaces.MultiDiscrete([3] + [3] * self.num_guards)  # Shopkeeper: 3 actions, Guards: 3 actions

        # Initialize Pygame
        pygame.init()
        info = pygame.display.Info()
        screen_width = SCREEN_WIDTH  # Screen width as configured
        screen_height = SCREEN_HEIGHT  # Screen height as configured
        self.screen = pygame.display.set_mode((screen_width, screen_height))
        pygame.display.set_caption("Cat Chase Environment")
        self.clock = pygame.time.Clock()
        self.running = True

    def reset(self):
        """
        Reset the environment to the initial state.
        """
        self.cat_position = list(self.initial_cat_position)
        self.shopkeeper_position = list(self.initial_shopkeeper_position)
        self.guard_positions = [list(pos) for pos in self.initial_guard_positions]
        return self._get_obs()

    def step(self, actions):
        """
        Take a step in the environment based on the actions.
        """
        shopkeeper_action = actions[0]
        guard_actions = actions[1:]

        # Update the shopkeeper and guards
        self._update_shopkeeper(shopkeeper_action)
        for i, action in enumerate(guard_actions):
            self._update_guard(i, action)

        # Calculate rewards
        reward, done = self._calculate_rewards()
        return self._get_obs(), reward, done, {}

    def _get_obs(self):
        """
        Get the current observation of the environment.
        """
        obs = [
            self.cat_position[0], self.cat_position[1],
            self.shopkeeper_position[0], self.shopkeeper_position[1]
        ]
        for guard in self.guard_positions:
            obs.extend(guard)
        return np.array(obs, dtype=np.float32)

    # def _update_shopkeeper(self, action):
    #     """
    #     Update the shopkeeper's position based on the action.
    #     """
    #     # Calculate distance to the cat
    #     distance_to_cat = np.linalg.norm(
    #         np.array(self.shopkeeper_position) - np.array(self.cat_position)
    #     )

    #     # Adjust speed based on distance
    #     if distance_to_cat < MAP_WIDTH * 0.2:  # If within 5% of the map width
    #         speed = 8
    #     else:
    #         speed = 4

    #     # Update position based on action
    #     if action == 0:  # Move right
    #         self.shopkeeper_position[0] += speed
    #     elif action == 1:  # Maintain position
    #         pass
    #     elif action == 2:  # Move left
    #         self.shopkeeper_position[0] -= speed
    def _update_shopkeeper(self, action):
        """
        Update the shopkeeper's position based on the action predicted by PPO,
        with speed adjustment depending on the proximity to the cat.
        """
        # Calculate the distance to the cat
        distance_to_cat = np.linalg.norm(np.array(self.shopkeeper_position) - np.array(self.cat_position))

        # Adjust speed based on distance to cat
        if distance_to_cat < 600:  # If within 600 units of the cat, increase speed
            speed_multiplier = 2  # Move faster when close to the cat
        else:
            speed_multiplier = 1  # Normal speed when farther away
        
        # Map PPO action to basic speed level (ignoring direction here, since A* handles that)
        if action == 0:  # Move fast towards the cat
            speed = 4 * speed_multiplier  # Higher speed when close to cat
        elif action == 1:  # Maintain position or normal movement
            speed = 2 * speed_multiplier  # Normal movement when not in a rush
        else:  # Move slowly
            speed = 1 * speed_multiplier  # Slow movement
        
        # Update the shopkeeper's position based on the action and the calculated speed
        self.shopkeeper_position[0] += speed  # Direction will be handled by A*  # Move towards or away from the cat based on position


    def _update_guard(self, guard_idx, action):
        """
        Update the guard's position based on the action.
        """
        if action == 0:  # Patrol left
            self.guard_positions[guard_idx][0] -= 2
        elif action == 1:  # Patrol right
            self.guard_positions[guard_idx][0] += 2
        elif action == 2:  # Maintain position
            pass

    # def _calculate_rewards(self):
    #     """
    #     Calculate the rewards based on the current positions.
    #     """
    #     distance = np.linalg.norm(np.array(self.shopkeeper_position) - np.array(self.cat_position))
        
    #     # If the cat is caught, give maximum reward
    #     if distance < 10:
    #         return 100, True  # High reward for catching the cat
        
    #     # Reward decreases with distance, with penalty
    #     max_distance = MAP_WIDTH  # Max distance on the map
    #     reward = max(0, (max_distance - distance) / max_distance * 10)  # Gradually increase reward as shopkeeper gets closer
        
    #     return reward, False  # Return reward and continue the game

    def _calculate_rewards(self):
        """
        Calculate the rewards based on the shopkeeper's distance to the cat and speed.
        Rewards are increased when close to the cat, with additional incentives to move fast.
        """
        distance = np.linalg.norm(np.array(self.shopkeeper_position) - np.array(self.cat_position))
        
        # If the cat is caught, give maximum reward
        if distance < 10:
            return 100, True  # Maximum reward for catching the cat
        
        # Reward increases as distance decreases (approaching the cat)
        max_distance = MAP_WIDTH  # Max distance on the map
        reward = max(0, (max_distance - distance) / max_distance * 10)  # Larger reward for getting closer to the cat
        
        # Encourage faster movement when within 600 units of the cat
        if distance <= 600:
            reward += 5  # Reward for approaching the cat within 600 units
            
            # If close enough to cat, encourage faster movement
            if distance <= 300:
                reward += 5  # Boost reward for being very close to the cat
                
        # Penalize for moving too far from the cat
        if distance > 600:
            reward -= 3  # Penalize for being far from the cat (out of the 600 unit range)
        
        # Further reward when shopkeeper reduces distance compared to the last step
        # This helps encourage the shopkeeper to keep moving toward the cat rather than moving randomly
        previous_distance = self.previous_distance_to_cat  # Keep track of previous distance in the environment
        if distance < previous_distance:
            reward += 2  # Small reward for reducing distance
        else:
            reward -= 2  # Penalize for increasing distance
        
        # Update the previous distance to the current one for comparison in next step
        self.previous_distance_to_cat = distance
        
        return reward, False  # Return reward and continue the game


    def render(self, mode='human'):
        """
        Render the environment.
        """
        # Handle Pygame events to keep the window responsive
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                pygame.quit()
                return

        if not self.running:
            return

        # Clear the screen
        self.screen.fill((0, 0, 0))

        # Draw the cat
        pygame.draw.circle(self.screen, (0, 255, 0), (int(self.cat_position[0]), int(self.cat_position[1])), 10)

        # Draw the shopkeeper
        pygame.draw.rect(self.screen, (255, 0, 0), (*map(int, self.shopkeeper_position), 20, 20))

        # Draw the guards
        for guard_position in self.guard_positions:
            pygame.draw.rect(self.screen, (0, 0, 255), (*map(int, guard_position), 20, 20))

        # Update the display
        pygame.display.flip()

        # Cap the frame rate
        self.clock.tick(60)

    def close(self):
        """
        Close the Pygame window.
        """
        pygame.quit()