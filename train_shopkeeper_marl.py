from stable_baselines3 import PPO

from logic.shopkeeper_marl_env import ShopkeeperEnv

# Create the environment
env = ShopkeeperEnv()

# Initialize the PPO model
model = PPO("MlpPolicy", env, verbose=1)

# Train the model
model.learn(total_timesteps=10000)

# Test the model
obs = env.reset()
for _ in range(100):
    action, _ = model.predict(obs)
    obs, reward, done, _ = env.step(action)
    env.render()
    if done:
        break
