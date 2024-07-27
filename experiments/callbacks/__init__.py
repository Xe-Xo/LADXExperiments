from callbacks.hparams import HParamCallback
from callbacks.pygame_viewer import PygameViewer
from callbacks.tensorboard import TensorboardCallback
from stable_baselines3.common.callbacks import CheckpointCallback, CallbackList

def create_callbacks(experiment_config,use_wandb_logging=False, extra_callbacks=[]):
    
    callbacks = []
    callbacks.append(CheckpointCallback(save_freq=experiment_config['save_freq'], save_path=experiment_config['save_state_dir'], name_prefix="ladx"))
    callbacks.append(HParamCallback())
    #callbacks.append(PygameViewer(4,4)) # Use this to view the environment in a pygame window. Obviously comes with rendering overhead so only use this for debugging not long term training
    callbacks.append(TensorboardCallback())
    callbacks.extend(extra_callbacks)
    return CallbackList(callbacks)