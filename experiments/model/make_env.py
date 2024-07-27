from gym_env.link_awake_env import LinkAwakeningEnv
from wrappers.stream_wrapper import StreamWrapper

from stable_baselines3.common.utils import set_random_seed

def make_env(env_config={}, seed=0):
    
    ''' Creates an environment for the training process. '''    
    def _init():

        env = LinkAwakeningEnv(env_config)
        if 'stream_wrapper' in env_config.keys():
            if env_config['stream_wrapper']:
                env = StreamWrapper(env,stream_metadata={"experiment_name": env_config["experiment_name"]})
        
        return env
    
    set_random_seed(seed)

    return _init