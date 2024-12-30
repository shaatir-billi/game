import gym
from stable_baselines3 import PPO
from stable_baselines3.common.env_util import make_vec_env
from logic.marl_env import CatChaseEnv

print("Creating the environment...")

# Define initial positions for the cat, shopkeeper, and guards
cat_position = [100, 100]
shopkeeper_position = [200, 200]
guard_positions = [[300, 300], [400, 400]]

# Define the platform boundaries for the guards
guard_platforms = [
    (1500, 2000),  # Platform boundaries for guard 0
    (3000, 3500)   # Platform boundaries for guard 1
]

# Initialize guard directions (1 for right, -1 for left)
guard_directions = [1, -1]

# Create the environment
env = CatChaseEnv(cat_position, shopkeeper_position, guard_positions, guard_platforms, guard_directions)

# Wrap the environment
env = make_vec_env(lambda: env, n_envs=1)

print("Defining the model...")
# Define the model
model = PPO("MlpPolicy", env, verbose=1)

print("Starting training...")
# Train the model
model.learn(total_timesteps=100000)

print("Saving the model...")
# Save the model
model.save("marl_model")

print("Loading the model for inference...")
# Load the model (for inference)
model = PPO.load("marl_model")

print("Testing the trained model...")
# Test the trained model
obs = env.reset()
for _ in range(1000):
    action, _states = model.predict(obs)
    obs, rewards, dones, info = env.step(action)
    env.render()
print("Training and testing completed.")


