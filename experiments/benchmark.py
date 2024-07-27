from gym_env.link_awake_env import LinkAwakeningEnv

if __name__ == "__main__":
    import random

    env = LinkAwakeningEnv({"headless": True, "max_steps": 1000000, "initial_state": 'ladx.gbc.state'})
    
    env.reset()
    i = 0
    env.pyboy.set_emulation_speed(0)
    import time
    start_time = time.time()
    while True:
        i += 1
        action = env.action_space.sample()
        #print(action)
        state, reward, done, trunc, info = env.step(action)
        if i % 16000 == 0:
            print(i, reward, done, info)
            print(env.seen_map)
            print(env.saved_map_count)
            break
        if done:
            print("Done")
            break
        
    end_time = time.time()

    print("Time taken: ", end_time - start_time)

    print(f"{16000/(end_time - start_time)} FPS")