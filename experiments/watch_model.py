
import uuid
from datetime import datetime

from os.path import exists
from pathlib import Path

import gymnasium as gym
import numpy as np
import torch as th

from pathlib import Path

from stable_baselines3.common.monitor import Monitor
from stable_baselines3.common.env_checker import check_env
from stable_baselines3 import PPO
from stable_baselines3.common.vec_env import DummyVecEnv, SubprocVecEnv
from stable_baselines3.common.env_util import make_vec_env
from stable_baselines3.common.callbacks import CheckpointCallback, CallbackList, EvalCallback

from experiments.callbacks.old import GameProgressCallback, HParamCallback


from experiments.linkawakeenv.link_awake_env import LinkAwakeningEnv
from experiments.old_training import make_env

import mediapy as media

import numpy as np
from stable_baselines3.common.policies import obs_as_tensor



ACTIONS_ARROW = ["NONE","UP", "DOWN", "LEFT", "RIGHT",] 
ACTIONS_BUTTON = ["NONE","A", "B", "SWITCH"]

def predict_proba(model, state):
    obs = obs_as_tensor(state, model.policy.device)
    dis = model.policy.get_distribution(obs)
    probs0 = dis.distribution[0].probs
    probs1 = dis.distribution[1].probs
    probs_np0 = probs0.detach().numpy()
    probs_np1 = probs1.detach().numpy()
    actions_dict = {"buttons": {}, "arrows": {}}
    for i in range(0,5):
        actions_dict["buttons"][ACTIONS_ARROW[i]] = probs_np0[0,i]
    for i in range(0,4):
        actions_dict["arrows"][ACTIONS_BUTTON[i]] = probs_np1[0,i]
    return probs_np0, probs_np1


def run_model(file_name):

    path = Path("saved_models",f"{file_name}.zip") 
    assert path.exists(), f"Model {path}"

    experiment_kwargs = {
        "experiment_name": "test_run",
        "headless": False,
        "max_steps": 2048,
        "emulation_speed": 20,
        #"init_state": "saved_rooms\\00_02_15.state",
    }

    current_time = datetime.now().strftime('%Y_%m_%d_%H_%M_%S')
    
    #full_frame_writer = media.VideoWriter(f"recordings/{current_time}.mp4", (480, 1296), fps=60)
    #full_frame_writer.__enter__()

    steps = 0
    env = make_vec_env(make_env(env_conf=experiment_kwargs), n_envs=1, seed=0)
    model = PPO.load(path)

    
    obs = env.reset()
    done = False
    while True:
        action, _states = model.predict(obs, deterministic=False)
        predict_proba(model,obs)
        env.unwrapped.env_method("save_image", "last_image")[0]
        #env.set_attr("predictions",predict_proba(model,obs))
        obs, rewards, done, info = env.step(action)
        #full_frame_writer.add_image(env.unwrapped.env_method("get_image")[0])
        #print(env.unwrapped.get_attr("seen_entities")[0])

        
        print(env.unwrapped.get_attr("last_reward_dict")[0])

        steps += 1
        if done:
            env.reset()
        if steps > 40000:
            break

    env.close()
    #full_frame_writer.close()



if __name__ == "__main__":

    run_model("ladx_8943616_steps")