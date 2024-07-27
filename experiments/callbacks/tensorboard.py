from stable_baselines3.common.callbacks import BaseCallback
from stable_baselines3.common.logger import Image

class TensorboardCallback(BaseCallback):

    ''' Callback that saves log information to tensorboard upon each reset of the environment '''

    def __init__(self, verbose=0):
        super().__init__()
        self.verbose = verbose
        self.last_episode_reward_dict = {}
        self.last_episode_reward_dict_scaled = {}
        self.last_episode_reward_dict_diff = {}
        self.last_episode_reward_dict_diff_scaled = {}

        self.reset_scaled_reward = 0
        self.reset_scaled_reward_diff = 0
        self.resets = 0

        self.best_reward = -10000
        self.best_reward_diff = -10000

        self.total_steps = 0
        
    def _on_step(self) -> bool:
        self.total_steps += 1
        done_env_indices = [i for i, done in enumerate(self.training_env.unwrapped.get_attr('done')) if done]

        if len(done_env_indices) == 0:
            return True
        

        self._on_reset(done_env_indices)

        return True
    
    def _on_reset(self, done_env_indices):


        reward_dict = self.training_env.unwrapped.get_attr("last_episode_reward_dict", indices=done_env_indices)
        reward_dict_scaled = self.training_env.unwrapped.env_method("last_episode_reward_dict_scaled", indices=done_env_indices)

        reward_dict_diff = self.training_env.unwrapped.get_attr("last_episode_reward_dict_diff", indices=done_env_indices)
        reward_dict_diff_scaled = self.training_env.unwrapped.env_method("last_episode_reward_dict_diff_scaled", indices=done_env_indices)

        scaled_reward = self.training_env.unwrapped.env_method("last_episode_reward",  indices=done_env_indices)
        scaled_reward_diff = self.training_env.unwrapped.env_method("last_episode_diff_reward", indices=done_env_indices)

        for i, en in enumerate(done_env_indices):
            for k, v in reward_dict[i].items():
                if k not in self.last_episode_reward_dict:
                    self.last_episode_reward_dict[k] = v
                else:
                    self.last_episode_reward_dict[k] += v

            for k, v in reward_dict_scaled[i].items():
                if k not in self.last_episode_reward_dict_scaled:
                    self.last_episode_reward_dict_scaled[k] = v
                else:
                    self.last_episode_reward_dict_scaled[k] += v

            for k, v in reward_dict_diff[i].items():
                if k not in self.last_episode_reward_dict_diff:
                    self.last_episode_reward_dict_diff[k] = v
                else:
                    self.last_episode_reward_dict_diff[k] += v

            for k, v in reward_dict_diff_scaled[i].items():
                if k not in self.last_episode_reward_dict_diff_scaled:
                    self.last_episode_reward_dict_diff_scaled[k] = v
                else:
                    self.last_episode_reward_dict_diff_scaled[k] += v

            self.resets += 1
            self.reset_scaled_reward += scaled_reward[i]
            self.reset_scaled_reward_diff += scaled_reward_diff[i]

            if scaled_reward[i] > self.best_reward:
                self.best_reward = scaled_reward[i]
                self.logger.record("best_reward_overall", self.best_reward)

            if scaled_reward_diff[i] > self.best_reward_diff:
                self.best_reward_diff = scaled_reward_diff[i]
                self.logger.record("best_reward_episode", self.best_reward_diff)

        for k in self.last_episode_reward_dict.keys():

            # Lifetime Progress
            self.logger.record(f"game_progress/{k}", self.last_episode_reward_dict[k])
            self.logger.record(f"game_progress_scaled/{k}", self.last_episode_reward_dict_scaled[k])
            self.logger.record(f"game_progress_diff/{k}", self.last_episode_reward_dict_diff[k])
            self.logger.record(f"game_progress_diff_scaled/{k}", self.last_episode_reward_dict_diff_scaled[k])
            
            # Progress per reset
            self.logger.record(f"game_progress_episode/{k}", self.last_episode_reward_dict[k] / self.resets)
            self.logger.record(f"game_progress_scaled_episode/{k}", self.last_episode_reward_dict_scaled[k] / self.resets)
            self.logger.record(f"game_progress_diff_episode/{k}", self.last_episode_reward_dict_diff[k] / self.resets)
            self.logger.record(f"game_progress_diff_scaled_episode/{k}", self.last_episode_reward_dict_diff_scaled[k] / self.resets)

            # Progress per step
            self.logger.record(f"game_progress_steps/{k}", self.last_episode_reward_dict[k] / self.total_steps)
            self.logger.record(f"game_progress_scaled_steps/{k}", self.last_episode_reward_dict_scaled[k] / self.total_steps)
            self.logger.record(f"game_progress_diff_steps/{k}", self.last_episode_reward_dict_diff[k] / self.total_steps)
            self.logger.record(f"game_progress_diff_scaled_steps/{k}", self.last_episode_reward_dict_diff_scaled[k] / self.total_steps)


    def _on_training_start(self) -> None:
        return super()._on_training_start()
    
    def _on_rollout_start(self) -> None:

        self.last_image = self.training_env.unwrapped.env_method('get_image', **{
            'include_seen': True,
            'include_reward': True,
        })

        for i, img in enumerate(self.last_image):
            self.logger.record(f"image/on_rollout/{i}", Image(img, "HWC"), exclude=("stdout", "log", "json", "csv"))
        
        return super()._on_rollout_start()
    
    def _on_rollout_end(self) -> None:

        self.last_episode_reward_dict = {}
        self.last_episode_reward_dict_scaled = {}
        self.last_episode_reward_dict_diff = {}
        self.last_episode_reward_dict_diff_scaled = {}

        self.reset_scaled_reward = 0
        self.reset_scaled_reward_diff = 0
        self.resets = 0

        self.best_reward = -10000
        self.best_reward_diff = -10000

        self.total_steps = 0

        return super()._on_rollout_end()


        



