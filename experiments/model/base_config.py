

import uuid
from datetime import datetime
from gym_env.link_awake_env import BASE_CONFIG

CPU_MULTIPLIER = 2

BASE_EXPERIMENT_CONFIG = {
    "experiment_name": str(uuid.uuid4())[0:8],
    "experiment_start": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    "environment": "LinkAwakeningEnv",
    "ep_length": 10 * 1024 * 1000,
    "num_envs": int(32 * CPU_MULTIPLIER),
    "save_freq": max(102_400 // int(32 * CPU_MULTIPLIER), 1),
    "num_steps": int(512 // CPU_MULTIPLIER),
    "num_epochs": 1,
    "batch_size": 1024,
    "lr": 0.00003,
    "vf_coef": 0.5,
    "ent_coef": 0.01,
    "gamma": 0.996,
    "save_state_dir": "saved_models",
    "stream_wrapper": False

}

for i in BASE_CONFIG.keys():
    if i not in BASE_EXPERIMENT_CONFIG:
        BASE_EXPERIMENT_CONFIG[i] = BASE_CONFIG[i]