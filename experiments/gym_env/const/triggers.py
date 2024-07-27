
from enum import IntEnum

# When actions are completed in a room,
# They trigger these events as completed
# This is used for progression in dungeons
# wRoomEvent is the value that is set and should be provided
# as an observation to the agent

class RoomTriggers(IntEnum):

    # How to Complete a Room

    TRIGGER_NONE = 0x00
    TRIGGER_KILL_ALL_ENEMIES = 0x01
    TRIGGER_PUSH_SINGLE_BLOCK = 0x02 # Push a single block (tile 0xA7).
    TRIGGER_STEP_ON_BUTTON = 0x03 # can only used once per dungeon
    #TRIGGER_UNKNOWN = 0x04 # found at the end of the Color Dungeon with the fairy
    TRIGGER_LIGHT_TORCHES = 0x05 # light two torches
    TRIGGER_KILL_IN_ORDER = 0x06 # Kill enemies in order of their sprite/object ID (after killing three enemies, the ID is triggered. This is the Pols Voice/Keese/Stalfos puzzle from Bottle Grotto).
    TRIGGER_PUSH_BLOCKS = 0x07 # Push 2 blocks together. They don't both have to be tile A7 (meaning you don't have to push both), but their final position must be horizontal.
    TRIGGER_KILL_SPECIALS = 0x08 # Kill all "special" enemies (normally can't be killed).
    TRIGGER_SOLVE_GLOWING_TILES = 0x09 # This is the five-tile puzzle from Lv.4/Angler's Tunnel.
    TRIGGER_KILL_SIDESCROLL_BOSS = 0x0A # Kill either Angler Fish (Level 4 boss) or Evil Eagle (Level 7 boss).
    TRIGGER_THROW_AT_DOOR = 0x0B # Throw something at a shut door.
    TRIGGER_HORSE_HEADS = 0x0C # Get both horse heads (sprite 0x98) to stand up.
    TRIGGER_THROW_POT_AT_CHEST = 0x0D # Throw a pot at a chest in position 23 to open it and obtain the Nightmare Key
    TRIGGER_FILL_LAVA_GAPS = 0x0E # Fill in the gaps with that rolling thing from Turtle Rock (sprite 0xB1).
    TRIGGER_SHOOT_STATUE_EYE = 0x0F # Shoot an arrow at the eye of a statue (tile 0xC0). You can have as many statues as you want; shooting any of them will work.
    TRIGGER_ANSWER_TUNICS = 0x10 # Answer the questions of the skeletons about their tunics colors. Only works on a room id $12.