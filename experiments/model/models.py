
import torch


from stable_baselines3.common.env_util import make_vec_env
from stable_baselines3.ppo import PPO

from model.feature_extraction import CustomFeatureExtractor
from callbacks import create_callbacks
from model.jax_models import create_jax_model
from model.base_config import BASE_EXPERIMENT_CONFIG
from model.make_env import make_env





def create_model(experiment_config={}):

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

def train_jax_model(experiment_config={}):

    ''' Trains a model with the given configuration. '''
    for i in BASE_EXPERIMENT_CONFIG.keys():
        if i not in experiment_config:
            experiment_config[i] = BASE_EXPERIMENT_CONFIG[i]

    callbacks = create_callbacks(experiment_config=experiment_config)            


    model, experiment_config = create_jax_model(experiment_config)
    import json
    with open(f"{experiment_config['save_state_dir']}/{experiment_config['experiment_name']}.json", "w") as f:
        json.dump(experiment_config, f, indent=4)
    model.learn(total_timesteps=experiment_config['ep_length'], log_interval=1, callback=callbacks, progress_bar=True)
    model.save(f"{experiment_config['save_state_dir']}/{experiment_config['experiment_name']}")



def train_model(experiment_config={}, epochs=10):

    ''' Trains a model with the given configuration. '''
    for i in BASE_EXPERIMENT_CONFIG.keys():
        if i not in experiment_config:
            experiment_config[i] = BASE_EXPERIMENT_CONFIG[i]

    callbacks = create_callbacks(experiment_config=experiment_config)            


    model, experiment_config = create_model(experiment_config)
    import json
    with open(f"{experiment_config['save_state_dir']}/{experiment_config['experiment_name']}.json", "w") as f:
        json.dump(experiment_config, f, indent=4)

    for i in range(epochs):
        model.learn(total_timesteps=experiment_config['ep_length'], log_interval=1, callback=callbacks, progress_bar=True)
        model.save(f"{experiment_config['save_state_dir']}/{experiment_config['experiment_name']}/{i+1}")

def train_from_existing_model(filename, experiment_config={}, ):

    ''' Trains a model from an existing model. '''
    for i in BASE_EXPERIMENT_CONFIG.keys():
        if i not in experiment_config:
            experiment_config[i] = BASE_EXPERIMENT_CONFIG[i]

    env = make_vec_env(make_env(env_config=experiment_config), n_envs=experiment_config['num_envs'], seed=0)
    callbacks = create_callbacks(experiment_config=experiment_config)            

    model = PPO.load(f"{experiment_config['save_state_dir']}/{filename}", env=env, tensorboard_log="logs")
    model.learn(total_timesteps=experiment_config['ep_length'], log_interval=1, callback=callbacks, progress_bar=True)
    model.save(f"{experiment_config['save_state_dir']}/{experiment_config['experiment_name']}")


def watch_model(filename):

    ''' Watches a model with the given filename. '''
    model = PPO.load(f"{BASE_EXPERIMENT_CONFIG['save_state_dir']}/{filename}")
    env = make_vec_env(make_env(env_config=BASE_EXPERIMENT_CONFIG), n_envs=1, seed=0)
    obs = env.reset()
    done = False
    while True:
        action, _states = model.predict(obs, deterministic=False)
        env.render()
        obs, rewards, done, info = env.step(action)
        if done:
            obs = env.reset()



