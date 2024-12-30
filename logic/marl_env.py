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
    def __init__(self, cat_position, shopkeeper_position, guard_positions, guard_platforms):
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

        # Initialize guard platforms
        self.guard_platforms = guard_platforms
        self.shopkeeper_speed = 0  # Initialize shopkeeper speed

    def seed(self, seed=None):
        """
        Set the seed for the environment's random number generator.
        """
        self.np_random, seed = gym.utils.seeding.np_random(seed)
        return [seed]

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
    
    def _update_shopkeeper(self, action):
        """
        Update the shopkeeper's position based on the action predicted by PPO,
        with speed adjustment depending on the proximity to the cat.
        """
        # Initialize shopkeeper speed if it is not already set
        if not hasattr(self, 'shopkeeper_speed') or self.shopkeeper_speed == 0:
            self.shopkeeper_speed = 3  # Start with the minimum speed

        # Calculate the distance to the cat
        distance_to_cat = np.linalg.norm(np.array(self.shopkeeper_position) - np.array(self.cat_position))

        # Speed increases continuously as the distance decreases
        max_speed = 6
        min_speed = 3
        max_distance = 1600
        
        # Calculate the speed based on distance
        speed = min_speed + (max_speed - min_speed) * (1 - distance_to_cat / max_distance)
        speed = max(min_speed, min(speed, max_speed))  # Clamp speed between 3 and 6 initially

        # Modify speed based on action
        if action == 0:  # Fast movement
            speed *= 1.5  # Increase speed
            speed = min(speed, 6)  # Allow up to 6 for fast movement
        elif action == 1:  # Normal movement
            speed *= 1.0
            speed = min(speed, 5)  # Cap at 5 for normal movement
        elif action == 2:  # Slow movement
            speed *= 0.5
            speed = max(speed, 3)  # Ensure minimum speed of 3 for slow movement

        # Smooth transition by damping abrupt changes
        self.shopkeeper_speed = (self.shopkeeper_speed + speed) / 2  # Average with previous speed

        # Update the shopkeeper's position
        self.shopkeeper_position[0] += self.shopkeeper_speed  # Movement in the x-direction

    
    def get_shopkeeper_speed(self):
        """
        Get the current speed of the shopkeeper.
        """
        return self.shopkeeper_speed

    def _update_guard(self, guard_idx, action):
        """
        Update the guard's position based on the action.
        The guard adjusts its movement based on the cat's position while staying on its platform.
        """
        # Get the guard's current position and platform boundaries
        guard_position = self.guard_positions[guard_idx]
        platform_start, platform_end = self.guard_platforms[guard_idx]  # Assuming platform boundaries are pre-defined

        # Determine the cat's position
        cat_x, cat_y = self.cat_position

        # Only update guard actions if the cat is on the same platform
        if platform_start <= cat_x <= platform_end:
            if action == 0:  # Move closer to the cat
                if cat_x < guard_position[0]:  # Cat is to the left
                    guard_position[0] -= 2  # Move left
                elif cat_x > guard_position[0]:  # Cat is to the right
                    guard_position[0] += 2  # Move right
            elif action == 1:  # Move to the cat's predicted position
               
                guard_position[0] += 2 if cat_x > guard_position[0] else -2
            elif action == 2:  # Stay near the middle of the cat's position
                midpoint = (platform_start + platform_end) // 2
                if guard_position[0] < midpoint:
                    guard_position[0] += 2
                elif guard_position[0] > midpoint:
                    guard_position[0] -= 2
        else:
            # Cat is not on the platform, maintain a normal patrolling behavior
            if action == 0:  # Patrol left
                guard_position[0] = max(platform_start, guard_position[0] - 2)
            elif action == 1:  # Patrol right
                guard_position[0] = min(platform_end, guard_position[0] + 2)
            elif action == 2:  # Maintain position
                pass

        # Ensure the guard stays within the platform boundaries
        guard_position[0] = max(platform_start, min(platform_end, guard_position[0]))

   
    def _calculate_rewards(self):
        """
        Calculate the rewards for the shopkeeper and guards based on their objectives.
        """
        # Shopkeeper reward logic
        distance = np.linalg.norm(np.array(self.shopkeeper_position) - np.array(self.cat_position))
        reward_shopkeeper = 0
        
        # Maximum reward for catching the cat
        if distance < 10:
            return 100, True  # End the game
        
        max_distance = MAP_WIDTH  # Max possible distance
        reward_shopkeeper = max(0, (max_distance - distance) / max_distance * 10)
        
        if distance <= 600:
            reward_shopkeeper += 5
            if distance <= 300:
                reward_shopkeeper += 5
        if distance > 600:
            reward_shopkeeper -= 3
        
        # Encourage reducing the distance
        if distance < self.previous_distance_to_cat:
            reward_shopkeeper += 2
        else:
            reward_shopkeeper -= 2
        
        # Update previous distance
        self.previous_distance_to_cat = distance
        
        # Guard-specific rewards
        reward_guards = 0
        for guard_idx, guard_position in enumerate(self.guard_positions):
            guard_distance = np.linalg.norm(np.array(guard_position) - np.array(self.cat_position))

            if guard_distance < 10:  # Guard catches the cat
                reward_guards += 20  # Incentive for guards catching the cat
            elif self.guard_platforms[guard_idx][0] <= self.cat_position[0] <= self.guard_platforms[guard_idx][1]:
                # Reward guards for effectively patrolling near the cat
                reward_guards += max(0, 10 - (guard_distance / 50))  # Scale with closeness

        # Combine rewards or return separately
        return reward_shopkeeper + reward_guards, False

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