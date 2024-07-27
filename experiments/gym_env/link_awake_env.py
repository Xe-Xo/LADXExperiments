
# PIL for various image transformations
import PIL.Image
import PIL.ImageDraw
from PIL import ImageFont
from skimage.transform import rescale
from skimage.color import rgb2gray
import math

# numpy for various array operations
import numpy as np

# pyboy for the emulator
from pyboy import PyBoy
from pyboy.utils import WindowEvent

# gym for the environment
from gymnasium import Env, spaces

import uuid
import random
from datetime import datetime

from os.path import exists



# Importing the various classes and functions from the other files

from gym_env.link_awake_state import LinkAwakeningData
from gym_env.const.entities import ENTITY_TYPE_LOOKUP
from gym_env.const.objects import OverworldObjects,TRANSLATE_PHYSICS_FLAGS, lookup_object_id, lookup_object_physics, CustomPhysicsFlags, PhysicsFlags
from gym_env.const.maps import Map, MapType, MapLevel
from gym_env.const.inventory import Inventory, INVENTORY_CYCLE
from gym_env.const.layouts import lookup_world_map_coords
from gym_env.memory import RamAddress, Registers


BASE_CONFIG = {
    "gb_path": "ladx.gbc",
    "headless": True,
    "emulation_speed": 0, 
    "init_state": "ladx.gbc.state",
    "init_seed": None, 
    "max_steps": 2048, 
    "save_video": False,
    "render_all_frames": False,
    "lock_checkpoint_room": False,
    "lock_start_checkpoint": None, #"0_14_0_20",  #
    "reward_weights": {
        
        # Exploration
        "unique_positions_visited": 0.1, # this should be on the exploration reward (len(unique_positions_found))
        "unique_rooms_visited": 0.25, # this should be the number of unique rooms link has visited
        "unique_objects_seen": 0, # this should be the number of unique objects link has seen
        "unique_entities_seen": 0.005, # this should be the number of unique entities link has seen
        "dialog_steps": -0.001, # Try and stop link from talking when not needed
        "time": -0.001, # this should be the number of frames passed to encourage speed
        "collided": -0.000001, # this happens when link moves against a solid object using the register of ApplyCollisionWithSolid in Bank 2

        # Game Progress
        "game_progress": 100, # this should be the progress reward (game progress bytes)
        
        # Combat
        "health": 1, # this should be the health reward (current health/ max health)
        "max_health": 10, # this should be the max health reward (max health)
        "deaths": 0, # this should be the link dead reward
        "sword_hits": 0.0001, # this should be the number of sword collissions link has made (enemies killed)
        "push": 0.005, # this should be the number of pushes link has made (pushes made)
        "blocked": 0.01, # this should be the number of blocks link has made (blocks made)
        "kills": 0.05, # this should be the number of kills link has made (kills made)

        # PickUps
        "total_rupees": 0.001,  # this should be the number of rupees link has collected off the ground
        #"total_hearts": 0.001, # this should be the number of hearts link has collected off the ground
    }

}

MOVEMENT_ACTION_NAMES = ["NONE","UP","DOWN","LEFT","RIGHT"]
BUTTON_ACTION_NAMES = ["NONE","A","B","INVENTORY"]
ACTION_NAMES = [MOVEMENT_ACTION_NAMES,BUTTON_ACTION_NAMES]


class LinkAwakeningEnv(Env):

    def __eq__(self, other):
        return self.uuid == other.uuid


    # Start of Episode Rewards (Checkpoint)

    def start_episode_reward(self):
        return sum(v*self.config['reward_weights'][k] for k,v in self.start_episode_reward_dict.items())
    
    def start_episode_reward_dict_scaled(self):
        return {k: v*self.config['reward_weights'][k] for k,v in self.start_episode_reward_dict.items()}

    # Reward after running last step
    def last_step_reward(self):
        return sum(v*self.config['reward_weights'][k] for k,v in self.last_step_reward_dict.items())

    def last_step_reward_dict_scaled(self):
        return {k: v*self.config['reward_weights'][k] for k,v in self.last_step_reward_dict.items()}

    # Rewards after the envionment has been reset for tensorboard logging
    def last_episode_reward(self):
        return sum(v*self.config['reward_weights'][k] for k,v in self.last_episode_reward_dict.items())
    
    def last_episode_reward_dict_scaled(self):
        return {k: v*self.config['reward_weights'][k] for k,v in self.last_episode_reward_dict.items()}

    # Rewards after the envionment has been reset for tensorboard logging (diff from the starting state)
    def last_episode_diff_reward(self):
        return sum(v*self.config['reward_weights'][k] for k,v in self.last_episode_reward_dict_diff.items())

    def last_episode_reward_dict_diff_scaled(self):
        return {k: v*self.config['reward_weights'][k] for k,v in self.last_episode_reward_dict_diff.items()}


    # Standard Gymnasium Environment Methods

    def __init__(self,config=None):

        if config is None:
            self.config = BASE_CONFIG.copy()
        else:
            self.config = config

        for i in BASE_CONFIG.keys():
            if i not in self.config:
                self.config[i] = BASE_CONFIG[i]

        if self.config['init_seed'] is None:
            self.uuid = str(uuid.uuid4())[0:8]
        else:
            self.uuid = self.config['init_seed']


        # Initial config stuff

        self.headless = self.config['headless']
        self.init_state = self.config['init_state']        
        head = 'null' if self.headless else 'SDL2'
        
        # pyboy emulator
        self.pyboy = PyBoy(self.config['gb_path'], window=head)
        if not self.config['headless']:
            self.pyboy.set_emulation_speed(self.config["emulation_speed"])

        # environment actions
        self.valid_actions = (
            (
                WindowEvent.PRESS_ARROW_UP,
                WindowEvent.PRESS_ARROW_DOWN,
                WindowEvent.PRESS_ARROW_LEFT,
                WindowEvent.PRESS_ARROW_RIGHT
            )
            ,
            (
                WindowEvent.PRESS_BUTTON_A,
                WindowEvent.PRESS_BUTTON_B,
            )
        )
        self.release_actions = (
            (
                WindowEvent.RELEASE_ARROW_UP,
                WindowEvent.RELEASE_ARROW_DOWN,
                WindowEvent.RELEASE_ARROW_LEFT,
                WindowEvent.RELEASE_ARROW_RIGHT
            )
            ,
            (
                WindowEvent.RELEASE_BUTTON_A,
                WindowEvent.RELEASE_BUTTON_B,
            )
        )
        self.all_keys = (
            (WindowEvent.PRESS_ARROW_UP,WindowEvent.RELEASE_ARROW_UP),
            (WindowEvent.PRESS_ARROW_DOWN,WindowEvent.RELEASE_ARROW_DOWN),
            (WindowEvent.PRESS_ARROW_LEFT,WindowEvent.RELEASE_ARROW_LEFT),
            (WindowEvent.PRESS_ARROW_RIGHT,WindowEvent.RELEASE_ARROW_RIGHT),
            (WindowEvent.PRESS_BUTTON_A,WindowEvent.RELEASE_BUTTON_A),
            (WindowEvent.PRESS_BUTTON_B,WindowEvent.RELEASE_BUTTON_B),
        )

        self.action_space = spaces.MultiDiscrete((5,4))
        self.observation_space = spaces.Dict({
            "screen": spaces.Box(low=0, high=1, shape=(3,14,16), dtype=np.float32),
            "entity_type": spaces.Box(low=0, high=1, shape=(16,), dtype=np.int32),
            "entity_info": spaces.Box(low=0, high=1, shape=(16,4), dtype=np.float32), 
            "vector": spaces.Box(low=0, high=1, shape=(89,), dtype=np.float32), 
            "minimap_object":  spaces.Box(low=0, high=255, shape=(11,11), dtype=np.uint8),
            "minimap_info": spaces.Box(low=0, high=1, shape=(11,11,10), dtype=np.float32),
        })

        # Environment Observations Variables
        
        ## screen image history
        self.screen_image_history = np.zeros((3,14,16)) # 3 frames of 14x16 floats in grayscale
        ## object_info world map
        self.object_info_history = np.zeros((128,160,14), dtype=np.uint16) 

        # Environment Rewards Variables
        ## Tracking Total Steps Taken
        self.total_steps = 0
        ## Tracking Total Number of Unique Positions Visited
        self.seen_pos = set()
        self.saved_pos_count = 0
        ## Tracking Total Number of Unique Maps Visited
        self.seen_map = set()
        self.saved_map_count = 0
        ## Tracking Total Number of Unique Objects (Tiles) Seen
        self.seen_objects = set()
        self.saved_objects_count = 0   
        ## Tracking Total Number of Unique Entities (Sprites) Seen
        self.seen_entities = set()
        self.saved_entities_count = 0
        ## Tracking Total Number of Enemies Killed
        self.total_enemy_kills = 0
        self.last_pop_kill_count = 0 # We track this to see if we have killed an enemy. it is wPieceofPowerKillCount last step
        ## Tracking Total Number of Steps with Dialog Box Open
        self.total_dialog_steps = 0
        ## Game Progress
        self.last_game_progress_val = 0

        # Logging Information
        # Reward Dictionary at the Start of the Environment (Not Always Zero as it can be loaded from a checkpoint)
        self.start_episode_reward_dict = {}

        # Reward Dictionary at the end of the last episode (diff after removing the start reward)
        self.last_episode_reward_dict = {}
        self.last_episode_reward_dict_diff = {}

        # Reward Dictionary at the end of the last step
        self.last_step_reward_dict = {}
        for i in self.config["reward_weights"].keys():
            self.last_step_reward_dict[i] = 0
            self.start_episode_reward_dict[i] = 0
            self.last_episode_reward_dict[i] = 0
            self.last_episode_reward_dict_diff[i] = 0

        self.last_map_pos = None

        self.done = False
        self.not_reset = True

        # Register Callbacks
        # and counting for the registers
        # This happens multiple times a step(sometime multiple times a frame)
        # so its important to keep track of the count seperately
        self.block_sfx = False
        self.block_sfx_registered = False
        self.count_block_sfx = 0
        self.block_reward = False

        self.push_sfx = False
        self.push_sfx_registered = False
        self.count_push_sfx = 0
        self.push_reward = False

        self.collided_object = False
        self.collided_object_registered = False
        self.count_collided_object = 0
        self.collided_reward = False

        self.sword_dmg = False
        self.sword_dmg_registered = False
        self.count_sword_dmg = 0
        self.sword_dmg_reward = False

        self.kill_reward = False

        self.checkpoint_loaded = False
        self.checkpoint = None

    def reset(self,seed=None):

        # Deregister any callbacks while resetting
        self.deregister_block_sfx() # Shield Block 'Ting'
        self.deregister_sword_dmg() # Sword Collides with Enemy
        self.deregister_collision() # Colliding with Wall
        self.deregister_push_sfx()  # SFX of Pushing Urchin

        # Save down the Rewards at the end of the last episode
        if self.not_reset == True:
            # No Starting Reward so skip this
            pass
        else:
            self.upon_reset()

        #self.set_seed()
        
        # Setup the Environment
        ## Load the initial state

        if self.load_random_checkpoint():
            pass
        else:
            with open(self.init_state, "rb") as f:
                self.pyboy.load_state(f)

        # reset the rewards
        self.post_state_load()
        self.not_reset = False

        
        
        return self.get_observation(), {}

    def step(self, action=None):

        try:
            self.run_action_on_emulator(action)

            obs = self.get_observation()
            net_reward, net_reward_dict = self.get_net_reward()
            self.done = self.get_health_reward() == 0
            if self.total_steps >= self.config["max_steps"]     :
                print("Truncated due to max steps")
                self.done = True
                truncated = True
            else:
                truncated = False

            x,y,z = self.get_map_pos()
            if (x,y,z) != self.last_map_pos:

                self.save_checkpoint(f'{x}_{y}_{z}_{int(self.get_game_progress_reward()*10)}')
            self.last_map_pos = (x,y,z)

            if self.checkpoint_loaded and self.config["lock_checkpoint_room"]:
                cx, cy, cz, _ = tuple(self.checkpoint[1].split("_"))
                if (x,y,z) != (int(cx),int(cy),int(cz)):
                    #print((x,y,z), (int(cx),int(cy),int(cz)))
                    truncated = True
                    
            self.done = self.done or truncated

            return obs, net_reward, self.done, truncated, {"new_reward": net_reward,"reward": net_reward_dict}
        
        except:
            self.save_image("error")
            return self.get_observation(), 0, True, True, {"new_reward": 0,"reward": {}}

    def render(self):
        return 

    def close(self):
        #self.full_frame_writer.close()
        self.deregister_collision() # Colliding with Wall
        #self.deregister_push_sfx() # SFX of Pushing Urchin
        self.deregister_block_sfx() # Shield Block 'Ting'
        self.deregister_sword_dmg() # Sword Collides with Enemy
        self.pyboy.stop()

    ### Observations and Rewards are generated here

    def get_reward_dict(self):

        ''' This function is used to get the reward dictionary for the environment at the current state '''

        return {
            #"dialog_steps": self.get_dialog_steps_reward(),
            "unique_positions_visited": self.get_unique_positions_reward(),
            "unique_rooms_visited": self.get_unique_rooms_reward(),
            "unique_objects_seen": self.get_unique_object_reward(),
            "unique_entities_seen": self.get_unique_entity_reward(),
            "collided": self.get_collision_reward(),
            "blocked": self.get_block_reward(),
            "sword_hits": self.get_sword_reward(),
            "push": self.get_push_reward(),
            "time": self.get_step_count_reward(),
            "game_progress": self.get_game_progress_reward(),
            "health": self.get_health_reward(),
            "kills": self.get_kills_reward(),
        }

    def get_observation(self):

        # Update the object info map
        self.update_last_seen_object_map()
        #self.update_last_seen_warp_map()

        gpa = list(self.get_game_progress_array())
        entity_obs = self.get_entities_obs()

        vector_list = [

            INVENTORY_CYCLE.index(RamAddress.wInventoryItems_BSlot.read_memory(self.pyboy)) / 14, # Inventory Item
            
            self.get_room_pos()[0] / 10,
            self.get_room_pos()[1] / 8,

            self.get_map_pos()[0] / 16,
            self.get_map_pos()[1] / 16,
            self.get_map_pos()[2] / 14,

            self.get_health_reward(),
            self.get_max_health_reward() / 16,
            (self.get_rupee_count() // 255) / 255,
            (self.get_rupee_count() % 255) / 255,

        ]

        vector_list.extend(gpa)


        return {
            "screen": self.get_screen_obs(),  # Shape (14,16,3)
            "entity_type": entity_obs["type"], # Shape (16,) "type"
            "entity_info": entity_obs["info"], # Shape (16,4)
            "vector": np.array(vector_list, dtype=np.float32), # Shape (89,)
            "minimap_object": self.get_minimap_object_obs(5,5), # Shape (7,7) -> (21,21)
            "minimap_info": self.get_minimap_info_obs(5,5), # Shape (7,7,10) -> (21,21,10)
        }

    ### Resetting Enivronment

    def reset_obs(self):

         ## screen image history
        self.screen_image_history = np.zeros((3,14,16)) # 3 frames of 14x16 floats in grayscale
        ## object_info world map
        self.object_info_history = np.zeros((128,160,14), dtype=np.uint16) 

        # Environment Rewards Variables
        ## Tracking Total Steps Taken
        self.total_steps = 0

        if self.checkpoint_loaded == False:
            ## Tracking Total Number of Unique Positions Visited
            self.seen_pos = set()
            self.saved_pos_count = 0
            ## Tracking Total Number of Unique Maps Visited
            self.seen_map = set()
            self.saved_map_count = 0
            ## Tracking Total Number of Unique Objects (Tiles) Seen
            self.seen_objects = set()
            self.saved_objects_count = 0   
            ## Tracking Total Number of Unique Entities (Sprites) Seen
            self.seen_entities = set()
            self.saved_entities_count = 0
        
        
        ## Tracking Total Number of Enemies Killed
        self.total_enemy_kills = 0
        self.last_pop_kill_count = 0 # We track this to see if we have killed an enemy. it is wPieceofPowerKillCount last step
        ## Tracking Total Number of Steps with Dialog Box Open
        self.total_dialog_steps = 0
        ## Game Progress
        ## Needed to not add extra seen stuff
        game_progress = self.get_game_progress_dict()
        game_progress_val = 0
        for k,v in game_progress.items():
            game_progress_val += sum(v.values())

        self.last_game_progress_val = game_progress_val

        # Register Callbacks
        # and counting for the registers
        # This happens multiple times a step(sometime multiple times a frame)
        # so its important to keep track of the count seperately
        self.block_sfx = False
        self.block_sfx_registered = False
        self.count_block_sfx = 0
        self.block_reward = False

        self.push_sfx = False
        self.push_sfx_registered = False
        self.count_push_sfx = 0
        self.push_reward = False

        self.collided_object = False
        self.collided_object_registered = False
        self.count_collided_object = 0
        self.collided_reward = False

        self.sword_dmg = False
        self.sword_dmg_registered = False
        self.count_sword_dmg = 0
        self.sword_dmg_reward = False

        self.kill_reward = False
        self.last_action = (0,0)
    
        self.not_reset = True

    def upon_reset(self):

        ''' This function is called at the end of an episode to perform the necessary logging before the next episode starts '''

        # Save down the Rewards at the end of the last episode
        reward_dict = self.get_reward_dict()

        for i in reward_dict.keys():
            self.last_episode_reward_dict_diff[i] = reward_dict[i] - self.start_episode_reward_dict[i]
            self.last_episode_reward_dict[i] = reward_dict[i]

        self.last_map_pos = self.get_map_pos()

        self.save_checkpoint_result()

    def post_state_load(self):

        ''' This function is called after pyboy loads a state to clear observations and release keys '''

        ## Reset Observations
        self.reset_obs()
        
        # make sure all the inputs are released
        for i in self.all_keys:
            self.pyboy.send_input(i[1])

        self.start_episode_reward_dict = self.get_reward_dict()
        self.last_step_reward_dict = self.start_episode_reward_dict.copy()

    def load_game_state(self, path):

        ''' This function is used to load a game state from a file '''
        ''' Loads Pyboy and Loads the Initial Variables from a file '''
        
        self.reset()
        LinkAwakeningData.load(path, self.pyboy)
        self.post_state_load()

    def set_seed(self):

        np.random.seed(int(self.uuid, 16))
        random.seed(int(self.uuid, 16))

    ### Performing A Step

    def release_keys(self):

        for i in range(0,4):
            self.pyboy.send_input(self.release_actions[0][i])

        for i in range(0,2):
            self.pyboy.send_input(self.release_actions[1][i])     


    def run_action_on_emulator(self, action):

        ''' This function is used to run an action on the emulator '''
            
        
        if action is not None:
            
            #print(action, self.last_action)
            if action[0] != self.last_action[0]:
                
                # Releasing Last Movement Key
                if self.last_action[0] != 0:
                    #print(f"Releasing {ACTION_NAMES[0][self.last_action[0]]} {self.release_actions[0][self.last_action[0]-1]}")
                    self.pyboy.send_input(self.release_actions[0][self.last_action[0]-1])

                # Nothing to Do
                if action[0] == 0:
                    pass

                elif action[0] < 5:
                    #print(f"Pressing {ACTION_NAMES[0][action[0]]} {self.release_actions[0][action[0]-1]}")  
                    self.pyboy.send_input(self.valid_actions[0][action[0]-1])
                

            if action[1] != self.last_action[1]:
                if self.last_action[1] != 0 and self.last_action[1] != 3:
                    #print(f"Releasing {ACTION_NAMES[1][self.last_action[1]]} {self.release_actions[1][self.last_action[1]-1]}")
                    self.pyboy.send_input(self.release_actions[1][self.last_action[1]-1])

                if action[1] == 0:
                    pass

                elif action[1] < 3:

                    #print(action[1], RamAddress.wInventoryItems_BSlot.read_memory(self.pyboy), RamAddress.wHasToadstool.read_memory(self.pyboy))

                    #if action[1] == 2 and RamAddress.wInventoryItems_BSlot.read_memory(self.pyboy) == Inventory.MAGIC_POWDER.value and RamAddress.wHasToadstool.read_memory(self.pyboy) == 1:
                        # skipping action as we have the toadstool in the slot
                        #print("skip")
                        #return

                    #print(f"Pressing {ACTION_NAMES[1][action[1]]} {self.release_actions[1][action[1]-1]}")  
                    self.pyboy.send_input(self.valid_actions[1][action[1]-1])
                
                # Switch Inventory - Special Action
                elif action[1] == 3:
                    self.switch_inventory()


        else:
            print("No Action?")

        self.register_push_sfx()
        self.register_block_sfx()
        self.register_collision()
        self.register_sword_dmg()

        self.pyboy.tick(count=9, render=self.config["render_all_frames"])
        
        self.deregister_push_sfx()
        self.deregister_block_sfx()
        self.deregister_collision()
        self.deregister_sword_dmg()


        #first = True
        #if self.get_dialog_value() != 0:
        #    count = 0
        #    while self.get_dialog_value() != 0:
        #        count += 1

        #        if self.get_dialog_value() == 9 or self.get_dialog_value() == 12:
        #            self.pyboy.button_press('a')
        #            self.pyboy.tick(10, render=False)
        #        else:
        #            self.pyboy.button_release('a')
        #            self.pyboy.tick(10, render=False)

        #        self.pyboy.tick(10,render=False)

        #        if count > 240:
        #            print("Got to 180")
        #            break
        #    self.total_dialog_steps += 1

        if self.get_movement_value() != 0:
            count = 0
            #print("Movement not allowed")
            while self.get_movement_value() != 0:
                count += 1
                self.pyboy.tick(render=self.config["render_all_frames"])

                if count > 60:
                    break
            #self.pyboy.tick(1,render=True)

        if self.get_screen_transition():   
            self.pyboy.tick(40,render=self.config["render_all_frames"])

        if self.get_warp_transition():
            self.pyboy.tick(60,render=self.config["render_all_frames"])

        self.push_reward = False

        if self.push_sfx:
            print("Push SFX Detected")
            #this shouldnt ever be a loop as its based on a callback
            # link moves really SlooooW so we need to tick a few times and check if the position has changed to encourage movement rather than pushin against a wall forever
            prev_push = self.get_room_pos()
            self.pyboy.tick(60,render=self.config["render_all_frames"])
            new_push = self.get_room_pos()
            if new_push[0] != prev_push[0] or new_push[1] != prev_push[1]:
                self.push_reward = True
            else:
                self.push_reward = False
        self.push_sfx = False

        
        #max_hearts = int(RamAddress.wMaxHearts.read_memory(self.pyboy) * 0x8)
        #RamAddress.wHealth.write_memory(self.pyboy, max_hearts) 
        
        
        self.script_give_magic_powder()

        # only render the final frame to speed up the environment
        self.pyboy.tick(render=True)
        self.last_action = action[0], action[1]
        self.total_steps += 1

    def switch_inventory(self):
        
        ''' Performs the necessary Actions to Switch The BSlot Item in the Inventory '''
        ''' This is done via manually editing the memory addresses of the inventory items '''
        ''' But could be done via the inventory screen. '''


        # get the current item in the BSlot

        current_b_item = RamAddress.wInventoryItems_BSlot.read_memory(self.pyboy)

        # find the index of the current item in the cycle
        try:
            current_inventory_index = INVENTORY_CYCLE.index(current_b_item)
        except:
            current_inventory_index = -1

        #print(current_inventory_index)
        


        possible_inventory = self.pyboy.memory[0xDB02:0xDB0C]
        # remove this to make it just what you have
        #possible_inventory = INVENTORY_CYCLE

        #next_inventory_index = (current_inventory_index + 1) % len(INVENTORY_CYCLE)
        #current_a_item = 0x01
        #inventory_value = INVENTORY_CYCLE[next_inventory_index].value
        #RamAddress.wInventoryItems_BSlot.write_memory(self.pyboy, inventory_value)
        #RamAddress.wInventoryItems_ASlot.write_memory(self.pyboy, current_a_item)
        #RamAddress.wInventoryItems_BSlot.write_memory(self.pyboy, inventory_value)

        #self.pyboy.memory[0xDB4C] = 20
        #self.pyboy.memory[0xDB4D] = 20
        #self.pyboy.memory[0xDB45] = 20

        #return

        possible_inventory = [(index,v, INVENTORY_CYCLE.index(Inventory(v)), INVENTORY_CYCLE.index(Inventory(v))-current_inventory_index) for index,v in enumerate(possible_inventory) if v != 0 and Inventory(v) in INVENTORY_CYCLE]


        if len(possible_inventory) == 0:
            return
        
        possible_inventory.sort(key=lambda x: x[3] if x[3] >= 0 else x[3] + len(INVENTORY_CYCLE))


        slot = possible_inventory[0][0]
        inventory_value = possible_inventory[0][1]


        # writing to various inventory slot memory addresses to affect the change

        current_a_item = RamAddress.wInventoryItems_ASlot.read_memory(self.pyboy)
        RamAddress.wInventoryItems_BSlot.write_memory(self.pyboy, inventory_value)
        RamAddress.wInventoryItems_ASlot.write_memory(self.pyboy, current_a_item)
        RamAddress.wInventoryItems_BSlot.write_memory(self.pyboy, inventory_value)

        inventory_slot_mem = RamAddress.wInventoryItems_SubSlot1.value + slot
        self.pyboy.memory[inventory_slot_mem] = current_b_item

    def script_give_magic_powder(self):

        # check if player is in witch's hut
        # check if player has magic powder, if not give it to them

        if self.get_map_pos() == (9,1,12):
            
            inventory_items = self.pyboy.memory[RamAddress.wInventoryItems_BSlot.value:RamAddress.wInventoryItems_SubSlot10.value+1] 
            if Inventory.MAGIC_POWDER.value not in inventory_items:
                print("Adding Magic Powder")
                for i,v in enumerate(inventory_items):
                    if v == 0:
                        self.pyboy.memory[RamAddress.wInventoryItems_BSlot.value + i] = Inventory.MAGIC_POWDER.value
                        break
            else:
                pass

        # Check for Duplicates
        inventory_items = self.pyboy.memory[RamAddress.wInventoryItems_BSlot.value:RamAddress.wInventoryItems_SubSlot10.value+1]
        inventory_items = [v for v in inventory_items if v != 0]
        if len(inventory_items) != len(set(inventory_items)):
            print(len(inventory_items), len(set(inventory_items)))
            print("Duplicates Found")
            for i in range(len(inventory_items)):
                if inventory_items.count(inventory_items[i]) > 1:
                    self.pyboy.memory[RamAddress.wInventoryItems_BSlot.value + i] = 0
                    break
    ### Util

    def matrix_encoding(self, matrix, max_n):
        return np.squeeze(np.eye(max_n)[matrix.reshape(-1)])

    ### World Position info

    def get_overworld_bool(self,z):

        map_type = MapType(z)
        return map_type == MapType.OVERWORLD
    
    def local_map_to_world_map(self, overworld_bool, mapId, mapRoom):

        # Uses layouts of maps when in a map that has layouts

        # from map_id and room_id get the Z layer

        # overworld translates perfectly
        
        return lookup_world_map_coords(overworld_bool, mapId, mapRoom)

    def get_room_pos(self):
        # Position of Link in the Room

        hLinkRoomPosition = RamAddress.hLinkRoomPosition.read_memory(self.pyboy)

        return (hLinkRoomPosition % 16,hLinkRoomPosition // 16)

    def get_map_pos(self):

        ''' Gets the World Map Position of Link '''
        ''' Eg. (0,0,0) is the top left corner of the overworld map '''

        wIsIndoor = RamAddress.wIsIndoor.read_memory(self.pyboy)
        isOverworld = wIsIndoor == 0x00
        hMapId = RamAddress.hMapId.read_memory(self.pyboy)
        hMapRoom = RamAddress.hMapRoom.read_memory(self.pyboy)
        mx, my, mz = self.local_map_to_world_map(isOverworld, hMapId, hMapRoom)    
        return mx,my,mz

    def get_world_pos(self,ignore_room_pos=False):

        wIsIndoor = RamAddress.wIsIndoor.read_memory(self.pyboy)
        isOverworld = wIsIndoor == 0x00
        hMapId = RamAddress.hMapId.read_memory(self.pyboy)
        hMapRoom = RamAddress.hMapRoom.read_memory(self.pyboy)
        
        if ignore_room_pos:
            x,y = 0,0
        else:
            x,y = self.get_room_pos()

        mx, my, mz = self.local_map_to_world_map(isOverworld, hMapId, hMapRoom)
        return mx * 10 + x, my * 8 + y, mz
    
    def get_room_map(self):
        return Map(RamAddress.hMapId.read_memory(self.pyboy))
    
    def update_last_seen_object_map(self):
        # updates the object info history matrix with the object info currently seen on screen
        # get the current object info
        wRoomObjects = RamAddress.wRoomObjects.read_memory_bytes(self.pyboy, 0x80)
        wRoomObjects = np.reshape(wRoomObjects, (8, 16)) # Reshape into Rows/Cols
        wRoomObjects = wRoomObjects[:,:10] # Drop the last 6 columns its padding

        # get the current map location
        map_x, map_y, map_z = self.get_world_pos(ignore_room_pos=True)

        # add the info to the history
        self.object_info_history[map_y:map_y+8, map_x:map_x+10, map_z] = wRoomObjects

    def get_minimap_object_obs(self,size_x=3,size_y=3):

        base_matrix = np.zeros((size_x*2+1,size_y*2+1))
        wx, wy, wz = self.get_world_pos()

        def clamp_offset(value, min, max):

            if value < min:
                return (min, min-value)
            elif value > max:
                return (max, max-value)
            else:
                return (value, 0)

        min_x, xdiff_min = clamp_offset(wx-size_x, 0, 159)
        max_x, xdiff_max = clamp_offset(wx+size_x+1, 0, 159)
        min_y, ydiff_min = clamp_offset(wy-size_y, 0, 127)
        max_y, ydiff_max = clamp_offset(wy+size_y+1, 0, 127)
        map_type = self.get_room_map().get_overworld_type()
        object_info = self.object_info_history[min_y:max_y, min_x:max_x, wz]
        sy, sx = object_info.shape

        # only need to offset from min values as hitting the max x and y will just keep it at 0,0 anyway

        base_matrix[0+ydiff_min:sy+ydiff_min,0+xdiff_min:sx+xdiff_min] = object_info
        object_info = base_matrix

        return object_info # Shape (7,7)

    def get_minimap_physics_obs(self,size_x=3,size_y=3):
        
        base_matrix = np.zeros((size_x*2+1,size_y*2+1))
        wx, wy, wz = self.get_world_pos()

        # necessary to deal with world limits
        def clamp_offset(value, min, max):

            if value < min:
                return (min, min-value)
            elif value > max:
                return (max, max-value)
            else:
                return (value, 0)
            
        min_x, xdiff_min = clamp_offset(wx-size_x, 0, 159)
        max_x, xdiff_max = clamp_offset(wx+size_x+1, 0, 159)
        min_y, ydiff_min = clamp_offset(wy-size_y, 0, 127)
        max_y, ydiff_max = clamp_offset(wy+size_y+1, 0, 127)
        map_type = self.get_room_map().get_overworld_type()
        object_info = self.object_info_history[min_y:max_y, min_x:max_x, wz]
        sy, sx = object_info.shape

        # only need to offset from min values as hitting the max x and y will just keep it at 0,0 anyway

        base_matrix[0+ydiff_min:sy+ydiff_min,0+xdiff_min:sx+xdiff_min] = object_info
        object_info = base_matrix

        def get_collision_int(obj_id):
            # will return a number between 0-255
            return lookup_object_physics(obj_id, map_type).value

        c_matrix = np.vectorize(get_collision_int)(object_info)
        return c_matrix # Shape (7,7)

    def get_minimap_info_obs(self,size_x=3,size_y=3):

        minimap_info = np.zeros((size_y*2+1,size_x*2+1,10), dtype=np.float32)

        # Layer 0 => Seen Coords
        minimap_info[:,:,0] = self.get_minimap_seen_obs(size_x,size_y) # Seen Position

        # Layer 1 => Seen Map Coords
        # 1 if seen map 
        # 0 if not seen map
        minimap_info[:,:,1] = self.get_minimap_map_obs(size_x,size_y)

        # Layer 2 => Not Current Map

        minimap_info[:,:,2] = self.get_minimap_notroom_obs(size_x,size_y)

        # Layer 2 => Warp Coords
        

        return minimap_info

    def get_minimap_seen_obs(self,size_x=3,size_y=3):

        minimap_seen = np.zeros((size_y*2+1,size_x*2+1), dtype=np.float32)

        x0,y0,z = self.get_world_pos()

        for x in range(-size_x, size_x+1):
            for y in range(-size_y, size_y+1):
                minimap_seen[y+size_y,x+size_x] = 1 if (x0+x,y0+y,z) in self.seen_pos else 0

        return minimap_seen
    
    def get_room_seen_obs(self):

        room_seen = np.zeros((10,8), dtype=np.float32)
        x0, y0, z = self.get_world_pos(ignore_room_pos=True)
        for x in range(0, 10):
            for y in range(0, 8):
                room_seen[x,y] = 1 if (x0+x,y0+y,z) in self.seen_pos else 0
        return room_seen
                 
    def get_minimap_notroom_obs(self,size_x=3,size_y=3):

        # Position in World is Part of a different Map or Not

        minimap_notroom = np.zeros((size_y*2+1,size_x*2+1), dtype=np.float32)

        x0,y0,z = self.get_map_pos()
        wx,wy,wz = self.get_world_pos()

        for x in range(-size_x, size_x+1):
            for y in range(-size_y, size_y+1):
                minimap_notroom[y+size_y,x+size_x] = 1 if (wx+x//16,wy+y//16,wz) != (x0,y0,z) else 0

        return minimap_notroom

    def get_minimap_map_obs(self,size_x=3,size_y=3):

        minimap_warp = np.zeros((size_y*2+1,size_x*2+1), dtype=np.float32)

        x0,y0,z0 = self.get_map_pos()

        for x in range(-size_x, size_x+1):
            for y in range(-size_y, size_y+1):
                minimap_warp[y,x] = 1 if (x0+x,y0+y,z0) in self.seen_map else 0

        return minimap_warp
     
    def get_screen_obs(self):
        
        rescaled_image = rescale(self.pyboy.screen.ndarray[:,:,3], 0.1, anti_aliasing=False)
        rescaled_image = np.resize(rescaled_image, (14,16))
        self.screen_image_history = np.roll(self.screen_image_history, 1, axis=0)
        self.screen_image_history[0,:,:] = rescaled_image
        return self.screen_image_history # Shape (3,14,16)
    
    def get_seen_obs(self):

        start = np.zeros((11,11))
        x0,y0,z = self.get_world_pos()
        for x in range(-5, 6):
            for y in range(-5, 6):
                start[x + 5,y + 5] = 1 if (x0+x,y0+y,z) in self.seen_pos else 0

        #print(start)
        return start

    def get_position_obs(self):

        # Position within the Room
        pos_in_room_x, pos_in_room_y = self.get_room_pos()
        pos_in_room_x, pos_in_room_x = pos_in_room_x / 8, pos_in_room_y / 10

        # Position of Map within the World
        map_x, map_y, map_z = self.get_world_pos(ignore_room_pos=True)
        map_x, map_y, map_z = map_x / 16, map_y / 16, map_z / 12 # 16, 16, 12 are the max values

        return np.array([pos_in_room_x, pos_in_room_y, map_x, map_y, map_z], dtype=np.float32)

    def get_net_reward(self):

        net_reward_dict = {}
        current_reward_dict = self.get_reward_dict()

        scaled_net_reward_dict = {}
        scaled_current_reward_dict = {}

        # Calculate the Scaled Reward

        for i in current_reward_dict.keys():
            net_reward_dict[i] = current_reward_dict[i] - self.last_step_reward_dict[i]
            scaled_current_reward_dict[i] = current_reward_dict[i] * self.config["reward_weights"][i]
            scaled_net_reward_dict[i] = net_reward_dict[i] * self.config["reward_weights"][i]
      
        self.last_step_reward_dict = current_reward_dict.copy()

         
        return sum(scaled_net_reward_dict.values()), scaled_current_reward_dict

    def get_dialog_steps_reward(self):

        ''' When Toadstool unlocks Link wastes heaps of time just using it over and over. lets try and disencourage that '''

        return self.total_dialog_steps

    def get_kills_reward(self):

        c_kill_count = self.get_pop_kill_count()
        #print(c_kill_count, self.last_pop_kill_count)
        if c_kill_count > self.last_pop_kill_count:
            #self.save_image("assets\\notable\\last_kill")
            self.kill_reward = True
            self.total_enemy_kills += c_kill_count - self.last_pop_kill_count
        else:
            self.kill_reward = False

        self.last_pop_kill_count = c_kill_count
        return self.total_enemy_kills

    def get_step_count_reward(self):
        return self.total_steps

    def get_unique_positions_reward(self):

        initial_count = len(self.seen_pos) + self.saved_pos_count
        pos = self.get_world_pos()
        self.seen_pos.add(pos)
        self.last_pos = pos

        final_count = len(self.seen_pos) + self.saved_pos_count
        if final_count > initial_count:
            self.pos_reward = True
        else:
            self.pos_reward = False

        return final_count

    def get_unique_rooms_reward(self):

        inital_count = len(self.seen_map) + self.saved_map_count
        pos = self.get_map_pos()
        self.seen_map.add(pos)
        final_count = len(self.seen_map) + self.saved_map_count
        
        if final_count > inital_count:
            self.room_reward = True
        else:
            self.room_reward = False

        return final_count

    def get_unique_object_reward(self):

        initial_count = len(self.seen_objects) + self.saved_objects_count

        obj_array = np.array(self.get_room_object_info())
        for obj in obj_array.flatten():
            self.seen_objects.add(obj)
        
        final_count = len(self.seen_objects) + self.saved_objects_count
        
        if final_count > initial_count:
            self.object_reward = True
        else:
            self.object_reward = False
        
        return final_count

    def get_unique_entity_reward(self):
        entities_list = self.get_entities_info()
        initial_count = len(self.seen_entities) + self.saved_entities_count

        for e in entities_list:
            et = e[0]
            self.seen_entities.add(et)

        final_count = len(self.seen_entities) + self.saved_entities_count
        
        if final_count > initial_count:
            self.entity_reward = True
        else:
            self.entity_reward = False


        return final_count

    def get_link_finalpos(self):
        
        hLinkFinalPositionX = RamAddress.hLinkFinalPositionX.read_memory(self.pyboy) - 16
        hLinkFinalPositionY = RamAddress.hLinkFinalPositionY.read_memory(self.pyboy) - 16

        hLinkFinalPositionX += 8
        #hLinkFinalPositionY -= 16

        return hLinkFinalPositionX, hLinkFinalPositionY, hLinkFinalPositionX + 16, hLinkFinalPositionY + 16

    def get_entities_info(self):

        wEntitiesPosXTable = RamAddress.wEntitiesPosXTable.read_memory_bytes(self.pyboy, 0x10)
        wEntitiesPosYTable = RamAddress.wEntitiesPosYTable.read_memory_bytes(self.pyboy, 0x10)
        wEntitiesPosXSignTable = RamAddress.wEntitiesPosXSignTable.read_memory_bytes(self.pyboy, 0x10)
        wEntitiesPosYSignTable = RamAddress.wEntitiesPosYSignTable.read_memory_bytes(self.pyboy, 0x10)
        wEntitiesTypeTable = RamAddress.wEntitiesTypeTable.read_memory_bytes(self.pyboy, 0x10)
        wEntitiesStatusTable = RamAddress.wEntitiesStatusTable.read_memory_bytes(self.pyboy, 0x10)
        wEntitiesHitboxPositionTable = RamAddress.wEntitiesHitboxPositionTable.read_memory_bytes(self.pyboy, 0x40)
        wwEntitiesHealthTableTable = RamAddress.wEntitiesHealthTable.read_memory_bytes(self.pyboy, 0x10)

        entities_list = []

        for i in range(0,0x10):

            es = wEntitiesStatusTable[i]
            if es == 0x00:
                continue

            ex = wEntitiesPosXTable[i]
            exs = wEntitiesPosXSignTable[i]
            ey = wEntitiesPosYTable[i]
            eys = wEntitiesPosYSignTable[i] 
            et = wEntitiesTypeTable[i]
            
            ehb = tuple(wEntitiesHitboxPositionTable[i * 0x4: i * 0x4 + 0x4])
            eh = wwEntitiesHealthTableTable[i]

            # Puts a Tile Square around the Entity regardless of its size 
            ex0 = ex - 8  #ex - int(ehb[2]/8*8)
            ey0 = ey - 16 #ey - int(ehb[3]/5*16) 
            ex1 = ex0 + 16 #(int(ehb[2]/8*16))
            ey1 = ey0 + 16 # (int(ehb[3]/5*16))

            entities_list.append((et,ex0,ey0,ex1,ey1,ehb,eh))


        return entities_list

    def get_entities_obs(self):

        def unit_vector(vector):
            """ Returns the unit vector of the vector."""

            if vector[0] == 0 and vector[1] == 0:
                return np.array([1,0])
            return vector / np.linalg.norm(vector)

        def angle_between(v1, v2):
            """Finds angle between two vectors"""
            v1_u = unit_vector(v1)
            v2_u = unit_vector(v2)
            return np.arccos(np.clip(np.dot(v1_u, v2_u), -1.0, 1.0))


        entities_list = self.get_entities_info()
        lx0, ly0, lx1, ly1 = self.get_link_finalpos()

        lxm = (lx0 + lx1)/2
        lym = (ly0 + ly1)/2

        lm = np.array([lxm, lym])
        
        entity_type_obs = np.zeros((16,), dtype=np.int32)
        entity_pos_offset = np.zeros((16,2), dtype=np.float32)
        entity_pos_offset_x = np.zeros((16,), dtype=np.float32)
        entity_pos_offset_y = np.zeros((16,), dtype=np.float32)
        entity_rotation = np.zeros((16,), dtype=np.float32)
        entity_distance = np.zeros((16,), dtype=np.float32)

        for i, (e_name, ex0, ey0, ex1, ey1, ehb,eh) in enumerate(entities_list):

            exm = (ex0 + ex1)/2
            eym = (ey0 + ey1)/2

            em = np.array([exm, eym])

            entity_pos_offset[i] = (em - lm ) / np.array([16*8,16*10]) 

            entity_pos_offset_x[i] = entity_pos_offset[i][0]
            entity_pos_offset_y[i] = entity_pos_offset[i][1]

            entity_distance[i] = np.linalg.norm(entity_pos_offset[i]) / 16 / 13
            entity_rotation[i] = angle_between(entity_pos_offset[i], np.array([1,0])) / np.pi
            entity_type_obs[i] = e_name


        # Concat the arrays of (16,) to (16,4)
        entity_info = np.stack([entity_pos_offset_x, entity_pos_offset_y, entity_rotation, entity_distance], axis=1)


        entity_obs = {
            "type": entity_type_obs,
            "info": entity_info,
        }



        return entity_obs

    def get_sword_reward(self):
        self.sword_reward = False
        if self.sword_dmg:
            self.count_sword_dmg += 1
            self.sword_reward = True
            #self.save_image("assets\\notable\\sword")
        self.sword_dmg = False
        return self.count_sword_dmg

    def get_block_reward(self):
        self.block_reward = False
        if self.block_sfx:
            self.count_block_sfx += 1
            self.block_reward = True
            #self.save_image("assets\\notable\\block")
        self.block_sfx = False
        return self.count_block_sfx

    def get_push_reward(self):
        if self.push_reward:
            self.count_push_sfx += 1
            #self.save_image("assets\\notable\\push")
            self.register_push_sfx()

        #self.push_sfx = False
        return self.count_push_sfx

    def get_collision_reward(self):

        if self.collided_object:
            #self.save_image("assets\\notable\\collided")
            self.count_collided_object += 1
        
        self.collided_object = False
        return self.count_collided_object

    def get_game_progress_dict(self):


        game_progress = {
            "inventory": self.get_inventory_progress(),
            "dungeon_item": self.get_dungeon_item_progress(),
            "trade_sequence": self.get_trading_sequence_progress(),
        }

        return game_progress

    def get_dungeon_item_progress(self):

        ''' 
            To finish a dungeon you need to acquire certain items to make progress.
            The map compass & stone beak are optional but the boss key is required.
            The small keys are also required to open doors within the dungeon.
        '''

        dungeon_item_progress = {}
        for i in range(0,9):
            dungeon_item_progress[f"DUNGEON_{i+1}_MAP"] = 1 * (self.pyboy.memory[0xDB16 + i*0x5] == 0xFF)
            dungeon_item_progress[f"DUNGEON_{i+1}_COMPASS"] = 1 * (self.pyboy.memory[0xDB17 + i*0x5] == 0xFF)
            dungeon_item_progress[f"DUNGEON_{i+1}_STONE"] = 1 * (self.pyboy.memory[0xDB18 + i*0x5] == 0xFF)
            dungeon_item_progress[f"DUNGEON_{i+1}_BOSS_KEY"] = 1 * (self.pyboy.memory[0xDB19 + i*0x5] == 0xFF)
            dungeon_item_progress[f"DUNGEON_{i+1}_SMALL_KEYS"] = min(self.pyboy.memory[0xDB20 + i*0x5],3) / 3 #limit to 3 keys

        return dungeon_item_progress

    def get_trading_sequence_progress(self):

        '''
            If you complete the trading sequence, you'll receive an important item
            which will aid you in finding the location of the final boss. (Magnifing Glass which works automatically)
        '''

        wTradeSequenceItem = RamAddress.wTradeSequenceItem.read_memory(self.pyboy)
        Sequence = [
            "YOSHI_DOLL", #1
            "RIBBON", #2
            "DOG_FOOD", #3
            "BANANAS", #4
            "STICK", #5
            "HONEYCOMB", #6
            "PINEAPPLE", #7
            "HIBISCUS", #8
            "LETTER", #9
            "BROOM", #10
            "FISH_HOOK", #11
            "NECKLACE", #12
            "SCALE", #13
            "MAGNIFING_GLASS" #14
            ]
        
        trade_sequence_progress = {}
        for sn, s in enumerate(Sequence):
            if wTradeSequenceItem >= sn + 1:
                trade_sequence_progress[s] = 1
            else:
                trade_sequence_progress[s] = 0
        
        return trade_sequence_progress
                
    def get_inventory_progress(self):

        inventory_slots = self.pyboy.memory[0xDB00:0xDB0C]

        has_inventory = {}




        has_inventory["FLIPPERS"] = (RamAddress.wHasFlippers.read_memory(self.pyboy) == 0xFF) * 1
        has_inventory["MEDICINE"] = (RamAddress.wHasMedicine.read_memory(self.pyboy)  == 0xFF) * 1
        has_inventory["TOADSTOOL"] = (RamAddress.wHasToadstool.read_memory(self.pyboy)  == 1) * -0.5
        has_inventory["TAIL_KEY"] = (RamAddress.wHasTailKey.read_memory(self.pyboy)  == 0xFF) * 1
        has_inventory["FACE_KEY"] = (RamAddress.wHasFaceKey.read_memory(self.pyboy)  == 0xFF) * 1
        has_inventory["ANGLER_KEY"] = (RamAddress.wHasAnglerKey.read_memory(self.pyboy)  == 0xFF) * 1
        has_inventory["BIRD_KEY"] = (RamAddress.wHasBirdKey.read_memory(self.pyboy)  == 0xFF) * 1


        for i in Inventory:
            if i != Inventory.EMPTY:
                has_inventory[i.name] = 0


        magic_powder_slot = None
        for slot, slot_value in enumerate(inventory_slots):

            if slot_value == 0x00:
                continue

            for i in Inventory:
                
                if i == Inventory.EMPTY:
                    continue

                #elif i == Inventory.MAGIC_POWDER and slot_value == i.value:
                #    if has_inventory["TOADSTOOL"] == :
                #        continue

                elif slot_value == i.value:

                    if i == Inventory.MAGIC_POWDER:
                        magic_powder_slot = slot

                    has_inventory[i.name] = 1
                    break

        #if RamAddress.wHasToadstool.read_memory(self.pyboy)  == 1 and magic_powder_slot is not None :

            # do some crazy shit to make sure no toadstool
        #    prev_alot = RamAddress.wInventoryItems_ASlot.read_memory(self.pyboy)
        #    prev_blot = RamAddress.wInventoryItems_BSlot.read_memory(self.pyboy)
        #    RamAddress.wHasToadstool.write_memory(self.pyboy, 0x00)
        #    self.pyboy.memory[0xDB00 + magic_powder_slot] = Inventory.MAGIC_POWDER.value
        #    RamAddress.wInventoryItems_ASlot.write_memory(self.pyboy, prev_alot)
        #    RamAddress.wInventoryItems_BSlot.write_memory(self.pyboy, prev_blot)
            
        #    print("force No Toadstool")

        #if self.pyboy.memory[0xDB4C] != self.pyboy.memory[0xDB76] and Inventory.MAGIC_POWDER in inventory_slots:
        #    print("set magic powder")
        #    self.pyboy.memory[0xDB4C] = self.pyboy.memory[0xDB76]
        
        if has_inventory["TOADSTOOL"] == 0 and has_inventory["MAGIC_POWDER"] == 1:
            wMagicPowderCount = RamAddress.wMagicPowderCount.read_memory(self.pyboy)
            wMaxMagicPowder = RamAddress.wMaxMagicPowder.read_memory(self.pyboy)
            if wMagicPowderCount < wMaxMagicPowder:
                print("updating Magic Powder")
                RamAddress.wMagicPowderCount.write_memory(self.pyboy, RamAddress.wMaxMagicPowder.read_memory(self.pyboy))

        return has_inventory

    def get_game_progress_array(self):
            
        game_progress = self.get_game_progress_dict()
        game_progress_list = []
        for k,v in game_progress.items():
            game_progress_list.extend(list(v.values()))


        return np.array(game_progress_list, dtype=np.float32)

    def get_game_progress_reward(self):

        game_progress_val = 0
        game_progress = self.get_game_progress_dict()
        for k,v in game_progress.items():
            game_progress_val += sum(v.values())

        if game_progress_val > self.last_game_progress_val:

            self.saved_pos_count += len(self.seen_pos)
            self.saved_map_count += len(self.seen_map)
            self.saved_objects_count += len(self.seen_objects)
            self.saved_entities_count += len(self.seen_entities)
            self.seen_pos.clear()
            self.seen_map.clear()
            self.seen_objects.clear()
            self.seen_entities.clear()
        else:
            self.gameprogress_reward = False

        self.last_game_progress_val = game_progress_val
        return game_progress_val

    def get_health_reward(self):
        return (self.pyboy.memory[0xDB5A] / 0x8) / self.pyboy.memory[0xDB5B] # wHealth # Percentage of health
        
    def get_max_health_reward(self):
        return self.pyboy.memory[0xDB5B] / 16 # wMaxHearts
    
    def get_rupee_count(self):
        rc = self.pyboy.memory[0xDB5D] * 255 + self.pyboy.memory[0xDB5E]
        #print(rc)
        return rc

    def get_inventory_items(self):
        # wInventoryItems
        inventory_slots = self.pyboy.memory[0xDB00:0xDB0C]
        #print(inventory_slots)
        inventory_count = len([i for i in inventory_slots if i != 0x00])

        flippers = self.pyboy.memory[0xDB0C] == 0xFF
        medicine = self.pyboy.memory[0xDB0D] == 0xFF

        return inventory_count + (1 if flippers else 0) + (1 if medicine else 0)

    def get_all_dungeon_progress(self):

        #wDungeonItemFlags

        # for each dungeon (0-7)
        # 5 bytes
        # 0 - map
        # 1 - compass
        # 2 - stone slab?
        # 3 - boss key
        # 4 - small key count
        progress = 0

        for didx in range(0,8):
            dungeon_flags = self.pyboy.memory[0xDB16 + didx*0x5:0xDB16 + didx*0x5 + 0x5]
            for d in dungeon_flags:
                if d != 0x00:
                    progress += 1
        return progress
            
    def get_map_obs(self):

        total = []

        for i in range(0, 0x100, 0x10):



            tile_data = self.pyboy.memory[0x8000+i: 0x8010+i]
            tile_arr = np.array(tile_data, dtype=np.uint8)
            tile_bits = np.unpackbits(tile_arr)
            #print(tile_bits.shape)


            #print(tile_bits)
            #print("\n")
            tile_bits = np.reshape(tile_bits, (8,16))
            #print(tile_bits)
            #print("\n")
            low, high = np.split(tile_bits, 2, axis=1)
            result=(high * 2 + low) * 128
            #print(result)
            #print("\n")

            total.append(result)

        print(np.concatenate(total, axis=1).shape)

    # Getting the image from the screen

    def get_reward_image(self, original=None):

        if original is not None:
            reward_image = original
        else:
            reward_image = PIL.Image.new('RGB', (144,160), (0,0,0))
        draw = PIL.ImageDraw.Draw(reward_image, mode="RGBA")
        if not exists('..//FreeMono.ttf'):
            myFont = ImageFont.load_default(20)
        else:        
            myFont = ImageFont.truetype('..//FreeMono.ttf', 20)


        start_reward = self.start_episode_reward()
        step_reward = self.last_step_reward()
        self.reward_since_start = step_reward - start_reward


        draw.text((10, 70), f"Reward: \n {round(self.reward_since_start,2)}", font=myFont, fill=(255,255,255), stroke_width=2, stroke_fill=(0,0,0))



        return reward_image

    def get_seen_room_image(self, original=None):

        if original is not None:
            seen_obs_image = original
        else:
            seen_obs_image = PIL.Image.new('RGB', (144,160), (0,0,0))
        draw = PIL.ImageDraw.Draw(seen_obs_image, mode="RGBA")


        room_obs = self.get_room_seen_obs()

        for x in range(0,10):
            for y in range(0,8):
                x0 = int(x*14.4)
                y0 = int(y*18)
                x1 = int((x+1)*14.4)
                y1 = int((y+1)*18)

                if room_obs[x,y] == 1:
                    draw.rectangle([x0,y0,x1,y1], fill=(0,255,0,100))

        return seen_obs_image

    def get_entity_obs_image(self,orginal=None):

        if orginal is not None:
            entity_obs_image = orginal
        else:
            entity_obs_image = PIL.Image.new('RGB', (144,160), (0,0,0))
        draw = PIL.ImageDraw.Draw(entity_obs_image, mode="RGBA")

        entity_list = self.get_entities_info()
        if not exists('..//FreeMono.ttf'):
            myFont = ImageFont.load_default(8)
        else:
            myFont = ImageFont.truetype('..//FreeMono.ttf', 8)

        for e_name, ex0, ey0, ex1, ey1,ehb,eh in entity_list:

            tx0 = ex0/16*14.4
            ty0 = ey0/16*18
            tx1 = ex1/16*14.4
            ty1 = ey1/16*18


            #ehbx, ehby, ehbw, ehbh = ehb
            #ehbx, ehby, ehbw, ehbh = ehbx/16*14.4, ehby/16*18, ehbw/16*14.4, ehbh/16*18

            #draw.rectangle([tx0,ty0,tx0+ehbw,ty0+ehbh], fill=(0,0,255,128))


            draw.rectangle([tx0,ty0,tx1,ty1], fill=(0,0,255,128))
            draw.text((tx0,ty0+3), f"{ENTITY_TYPE_LOOKUP[e_name]} {eh}", font=myFont, fill=(255,0,0), stroke_width=2, stroke_fill=(0,0,0))


        lx0, ly0, lx1, ly1 = self.get_link_finalpos()
        draw.rectangle([lx0/16*14.4,ly0/16*18,lx1/16*14.4,ly1/16*18], fill=(255,0,0,128))

        #for x in range(0,10):
        #    for y in range(0,9):
        #        draw.rectangle([x*14.4,y*18,(x+1)*14.4,(y+1)*18], outline=(255,0,0,100), width=1)


        return entity_obs_image

    def get_object_image(self, original=None):

        if original is not None:
            object_obs_image = original
        else:
            object_obs_image = PIL.Image.new('RGB', (144,160), (0,0,0))
        draw = PIL.ImageDraw.Draw(object_obs_image, mode="RGBA")

        wx,wy,wz = self.get_world_pos(ignore_room_pos=True)
        
        if not exists('..//FreeMono.ttf'):
            myFont = ImageFont.load_default(10)
        else:
            myFont = ImageFont.truetype('..//FreeMono.ttf', 10)
         

        for x in range(0,10):
            for y in range(0,8):
                x0 = int(x*14.4)
                y0 = int(y*18)
                x1 = int((x+1)*14.4)
                y1 = int((y+1)*18)

                draw.text((x0+2,y0+2),f"{hex(self.object_info_history[wy+y,wx+x,wz])[2:]}",font=myFont, fill=(255,255,255), stroke_width=2, stroke_fill=(0,0,0))

        return object_obs_image

    def get_image(self, include_entities=False, include_objects=False, include_seen=False, include_reward=False):

        image = self.pyboy.screen.image.convert('RGB').resize((144,160))
        #object_image = self.get_object_obs_image(size_x=8,size_y=8)
        if include_seen:
            seen_image = self.get_seen_room_image(image)
        if include_objects:
            object_image = self.get_object_image(image)
        if include_entities:
            entity_image = self.get_entity_obs_image(image)
        if include_reward:
            reward_image = self.get_reward_image(image)
        
        dst = PIL.Image.new('RGB', (image.width, image.height))
        dst.paste(image, (0, 0))
        #dst.paste(entity_image, (image.width, 0))

        #dst.paste(object_image, (image.width + object_image.width, 0))
        #dst.paste(seen_image, (image.width, 0))

        return np.array(dst)

    def add_video_frame(self):
        
        image_arr = self.get_image()

    def save_image(self,name="default"):
        image = self.get_image(include_reward=True, include_seen=True)
        PIL.Image.fromarray(image).save(f"{name}.png")

    # Utilities to skip frames when Link Cannot Move or Take Actions.

    def get_screen_transition(self):
        # Skips over Frames where Link is transitioning between Rooms (about 40 frames)
        screen_transition = self.pyboy.memory[0xC124] != 0 #wRoomTransition
        return screen_transition
    
    def get_warp_transition(self):
        # Skips over Frames where Warping to another Room (about 60 frames)
        warp_transition = self.pyboy.memory[0xC16B] != 4 #wWarpTransition
        return warp_transition

    def get_gfx_transition(self):

        gfx_transition = self.pyboy.memory[0xC3CA]
        #gfx_transition_count = self.pyboy.memory[0xC180]
        print(gfx_transition)

        return gfx_transition

    def get_dialog_value(self):
        
        dialog_byte = self.pyboy.memory[0xC19F]
        mask = 0xF #  Last 4 bits have info about the dialogue value
        dialog = dialog_byte & mask
        return dialog

    def get_movement_value(self):
        
        movement_byte = self.pyboy.memory[0xFFA1]
        movement = movement_byte
        return movement

    def get_pop_kill_count(self):
        return RamAddress.wPieceOfPowerKillCount.read_memory(self.pyboy)
    
    def get_room_map_type(self):
        map_id = self.pyboy.memory[0xFFF7] #hMapID indoor room map
        overworld = self.pyboy.memory[0xDBA5] == 0x00 # wIsIndoor

        if overworld:
            return MapType.OVERWORLD
        else:
            return Map(map_id).get_overworld_type()
        
    def get_room_map_id(self):
        map_id = self.pyboy.memory[0xFFF7] #hMapID indoor room map
        overworld = self.pyboy.memory[0xDBA5] == 0x00 # wIsIndoor

        if overworld:
            return None
        
        return map_id

    def get_room_object_int(self):
        _wRoomObjects = self.pyboy.memory[0xD711:0xD791]
        _wRoomObjects = np.reshape(_wRoomObjects, (8, 16)) # Reshape into Rows/Cols
        _wRoomObjects = _wRoomObjects[:,:10] # Drop the last 6 columns its padding
        map_type = self.get_room_map_type().value
        _wRoomObjects = np.add(np.multiply(_wRoomObjects, 4), map_type) # Try to keep the object ids unique but similar together
        
        return _wRoomObjects #(8,10)

    def get_room_collision_int(self):
        _wRoomObjects = self.pyboy.memory[0xD711:0xD791]
        _wRoomObjects = np.reshape(_wRoomObjects, (8, 16)) # Reshape into Rows/Cols
        _wRoomObjects = _wRoomObjects[:,:10] # Drop the last 6 columns its padding
        map_type = self.get_room_map_type()
        
        def get_collision_int(obj_id):
            return lookup_object_physics(obj_id, map_type).value
        
        c_matrix = np.vectorize(get_collision_int)(_wRoomObjects)

        return c_matrix #(8,10)

    def get_room_object_info(self):
        _wRoomObjects = self.pyboy.memory[0xD711:0xD791]
        _wRoomObjects = np.reshape(_wRoomObjects, (8, 16)) # Reshape into Rows/Cols
        _wRoomObjects = _wRoomObjects[:,:10] # Drop the last 6 columns its padding
        _wRoomObjects = _wRoomObjects.tolist()
        
        for x in range(0, 8):
            for y in range(0, 10):
                _wRoomObjects[x][y] = lookup_object_id(_wRoomObjects[x][y], self.get_room_map_type())

        return _wRoomObjects
    
    def get_room_collision_info(self):
        _wRoomObjects = self.get_room_object_info()

        for x in range(0, 8):
            for y in range(0, 10):
                _wRoomObjects[x][y] = lookup_object_physics(_wRoomObjects[x][y].value, self.get_room_map_type())

        return _wRoomObjects

    def get_notable(self):
        ''' Returns a string for the stream wrapper to display icons '''

        #   { alias: 'note_acquire', src: 'assets/acquire.png' },
        #   { alias: 'note_aware', src: 'assets/aware.png' }, 
        #   { alias: 'note_block', src: 'assets/block.png' },
        #   { alias: 'note_fall', src: 'assets/fall.png' },
        #   { alias: 'note_hurt', src: 'assets/hurt.png' },
        #   { alias: 'note_push', src: 'assets/push.png' },
        #   { alias: 'note_sword', src: 'assets/sword.png' },


        notable = ""

        if self.kill_reward:
            notable = "note_sword"
            return notable
        
        if self.block_reward:
            notable = "note_block"
            return notable
        
        if self.push_reward:
            notable = "note_push"
            return notable

        #if self.entity_reward or self.object_reward:
        #    notable = "note_aware"
        #    return notable
        
        if self.gameprogress_reward:
            notable = "note_acquire"
            return notable
        
        return notable

    # Registers for Game Information Tracking Between Frames
    
    def register_sword_dmg(self):


        if self.sword_dmg_registered == True:
            return

        def t(env):
            if env.sword_dmg:
                return
            env.sword_dmg = True

        Registers.SWORD_DMG.hook_register(self.pyboy, t, self)
        self.sword_dmg_registered = True

    def deregister_sword_dmg(self):
        
        if self.sword_dmg_registered == False:
            return

        Registers.SWORD_DMG.hook_deregister(self.pyboy)
        self.sword_dmg_registered = False

    def register_block_sfx(self):

        if self.block_sfx_registered == True:
            return

        def t(env):

            if env.block_sfx:
                return
            env.block_sfx = True


        Registers.BLOCK_SFX.hook_register(self.pyboy, t, self)
        self.block_sfx_registered = True

    def deregister_block_sfx(self):

        if self.block_sfx_registered == False:
            return
            
        Registers.BLOCK_SFX.hook_deregister(self.pyboy)
        self.block_sfx_registered = False

    def register_push_sfx(self):

        if self.push_sfx_registered == True:
            return

        def t(env):
            if env.push_sfx:
                return
            #print("push callback")
            
            env.push_sfx = True
            env.deregister_push_sfx()


        Registers.PUSH_SFX.hook_register(self.pyboy, t, self)
        self.push_sfx_registered = True

    def deregister_push_sfx(self):

        if self.push_sfx_registered == False:
            return
        
        Registers.PUSH_SFX.hook_deregister(self.pyboy)
        self.push_sfx_registered = False

    def register_collision(self):

        if self.collided_object_registered == True:
            return

        def t(env):

            if env.collided_object:
                return
            #print("collision callback")
            env.collided_object = True

        Registers.COLLISION.hook_register(self.pyboy, t, self)
        self.collided_object_registered = True

    def deregister_collision(self):

        if self.collided_object_registered == False:
            return

        Registers.COLLISION.hook_deregister(self.pyboy)
        self.collided_object_registered = False

    # Checkpoint Management

    def load_random_checkpoint(self, type="found"):
        import random
        data = self.load_info_json()
        existing_checkpoints = data.get(f"{type}_checkpoints", [])
        if len(existing_checkpoints) == 0:
            return False
        # Get the game states 

        if self.config["lock_start_checkpoint"] in existing_checkpoints:
            #print("Skipping 6_11_12_20")
            #existing_checkpoints.remove("6_11_12_20")
            self.load_checkpoint(self.config["lock_start_checkpoint"], type=type)
            return True

        existing_checkpoints_split = {}
        for v in existing_checkpoints:
            gp = int(v.split("_")[3])
            if gp not in existing_checkpoints_split.keys():
                existing_checkpoints_split[gp] = []
            
            existing_checkpoints_split[gp].append(v)

        gp_list = list(existing_checkpoints_split.keys())
        total_gp = sum(gp_list)
        gp_weights = [k / total_gp for k in gp_list]

        # Random Choice between GameProgress to ensure model gets a variety of experiences


        gp = random.choices(gp_list, weights=gp_weights, k=1)[0]

        checkpoints = existing_checkpoints_split[gp]

        if "result" not in data.keys():
            data["result"] = {}


        seen = []
        seen_val = []
        unseen = []
        max_val = -100000
        min_val = 100000
        total = 0

        
        for checkpoint in checkpoints:

            if f"{type}_{checkpoint}" not in data["result"].keys():
                unseen.append(checkpoint)
            else:
                seen.append(checkpoint)
                val = round(data["result"][f"{type}_{checkpoint}"]["average_result"],0)
                
                seen_val.append(val) 
                if val > max_val:
                    max_val = val

                if val < min_val:
                    min_val = val

                total += val



        # If Any Checkpoints are Unseen, Load One of Those
        if len(unseen) > 0:
            name = random.choice(unseen)
            #print(f"Loading Checkpoint: {type} {name}")
            self.load_checkpoint(name, type=type)
            return True
        
        # If All Checkpoints are Seen, Load using a weighted Average Result

        seen_val = np.array(seen_val)
        seen_val = (max_val - seen_val)
        #print(seen_val)

        if sum(seen_val) <= 0:
            seen_val = np.ones(len(seen_val))

        name = random.choices(seen, weights=seen_val, k=1)[0]
        #print(f"Loading Checkpoint: {type} {name}")
        self.load_checkpoint(name, type=type)
        return True



    def save_checkpoint_result(self):
        if self.checkpoint_loaded:
            checktype, checkname = self.checkpoint
        else:
            return

        info_json = self.load_info_json()
        if "result" not in info_json.keys():
            info_json["result"] = {}

        if f"{checktype}_{checkname}" not in info_json["result"].keys():
            info_json["result"][f"{checktype}_{checkname}"] = {
                "attempts": 1,
                "total_result": self.last_step_reward() - self.start_episode_reward(),
                "average_result": (self.last_step_reward() - self.start_episode_reward())/1,
                "best_result": self.last_step_reward()
            }
        else:
            info_json["result"][f"{checktype}_{checkname}"] = {
                "attempts":  info_json["result"][f"{checktype}_{checkname}"]["attempts"] + 1,
                "total_result": info_json["result"][f"{checktype}_{checkname}"]["total_result"] + self.last_step_reward() - self.start_episode_reward(),
                "average_result": (info_json["result"][f"{checktype}_{checkname}"]["total_result"] + self.last_step_reward() - self.start_episode_reward()) / (info_json["result"][f"{checktype}_{checkname}"]["attempts"] + 1),
                "best_result": max(info_json["result"][f"{checktype}_{checkname}"]["best_result"], self.last_step_reward())
            }

        #print(f"Saving Checkpoint Result for {checktype}_{checkname} -> {self.last_step_reward() - self.start_episode_reward()}")
        self.save_info_json(info_json)

    def load_checkpoint(self, name, type="found"):
        LinkAwakeningData.load(self,name, type=type)
        # Makes Sure Health is Tracked
        data = self.load_info_json()
        if "health" not in data.keys():
            data["health"] = {}
        data["health"][f"{type}_{name}"] = self.get_health_reward()
        self.save_info_json(data)



    def save_checkpoint(self, name, type="found"):
        data = self.load_info_json() 
        existing_checkpoints = data.get(f"{type}_checkpoints", [])
        if name not in existing_checkpoints:
            print(self.get_game_progress_dict())
            LinkAwakeningData(self, name, type=type)
            data[f"{type}_checkpoints"] = data.get(f"{type}_checkpoints", []) + [(name)]
            if "health" not in data.keys():
                data["health"] = {}
            data["health"][f"{type}_{name}"] = self.get_health_reward()

        # Update Room State if Health is better than previous
        elif data["health"].get(f"{type}_{name}", None) != None:
            if data["health"][f"{type}_{name}"] < self.get_health_reward():
                print("Health is better than previous, updating..")
                data["health"][f"{type}_{name}"] = self.get_health_reward()
                LinkAwakeningData(self, name, type=type)

        self.save_info_json(data)

    def load_info_json(self):
        import json
        with open("experiments\checkpoints\info.json", "r") as f:
            data = json.load(f)
            return data
        
    def save_info_json(self, data):
        import json
        with open("experiments\checkpoints\info.json", "w") as f:
            json.dump(data, f, indent=4)







       
           
           
        