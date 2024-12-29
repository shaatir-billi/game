import gym
from stable_baselines3 import PPO
from logic.marl_env import CatChaseEnv

print("Creating the environment...")

# Define initial positions
cat_position = [8, 3]
shopkeeper_position = [0, 2]
guard_positions = [[2, 3], [7, 4]]

# Create the environment with initial positions
env = CatChaseEnv(cat_position, shopkeeper_position, guard_positions)

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
