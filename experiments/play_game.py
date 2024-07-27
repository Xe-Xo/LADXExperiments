

from gym_env.link_awake_env import LinkAwakeningEnv
from util.gamepad import XboxController

import uuid

if __name__ == "__main__":
    
    xbox_controller = XboxController()
    env = LinkAwakeningEnv({"headless": False, "max_steps": 1000000, "render_all_frames": True})
    env.reset()
    env.pyboy.set_emulation_speed(2) # Game Runs a Little Slow on 1
    while True:

        try:

            # action => The action to be taken in the environment
            # request_reset => True if the user wants to reset the environment
            # request_save => True if the user wants to save a checkpoint

            action, request_reset, request_save = xbox_controller.read_action()
            if request_save:
                name = str(uuid.uuid4())[0:8]
                env.save_checkpoint(name, "eval")
                print(name)
                pass
            
            obs, new_reward, done, truncated, info = env.step(action)
            if done or request_reset:
                env.reset()

        except KeyboardInterrupt:
            break


    env.render()
    env.close()