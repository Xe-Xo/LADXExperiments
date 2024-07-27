import uuid
from datetime import datetime
import torch

from stable_baselines3.common.utils import set_random_seed
from stable_baselines3.common.env_util import make_vec_env

# !pip install sbx-rl
from sbx import PPO
from model.feature_extraction import CustomFeatureExtractor
from callbacks import create_callbacks
from model.make_env import make_env
from model.base_config import BASE_EXPERIMENT_CONFIG


def create_jax_model(experiment_config={}):

    ''' Creates a model for the training process. '''

    for i in BASE_EXPERIMENT_CONFIG.keys():
        if i not in experiment_config:
            experiment_config[i] = BASE_EXPERIMENT_CONFIG[i]

    policy_kwargs = dict(
        features_extractor_class=CustomFeatureExtractor,
        share_features_extractor=True,
        net_arch=[1024, 1024], 
        activation_fn=torch.nn.ReLU,
        )

    env = make_vec_env(make_env(env_config=experiment_config), n_envs=experiment_config['num_envs'], seed=0)

    model = PPO(
            "MultiInputPolicy",
            env,
            verbose=1,
            n_steps=experiment_config['num_steps'],
            batch_size=experiment_config['batch_size'],
            tensorboard_log="logs",
            learning_rate=experiment_config['lr'],
            vf_coef=experiment_config['vf_coef'],
            ent_coef=experiment_config['ent_coef'],
            gamma=experiment_config['gamma'],
            policy_kwargs=policy_kwargs
        )
    
    return model, experiment_config


