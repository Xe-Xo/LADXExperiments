from enum import IntEnum, Enum,  Flag

from gym_env.const.maps import MapType, Map

# 0x864DB -> Data for Rooster Room 92 - 18 objects
# The first is 2 byes and C6
# the last is 2 byes D6


# An "Object" is object in the world that doesnt use sprite
# Think grass, blocks, fences etc.
# Anything with sprites is an "Entity".

# ObjectInformation for the current Room
# is found wRoomObjects
# When checking for collision the game checks the object ID
# and the MapID (to see if its overworld or indoors)
# And looks up the physics flags for the object

def lookup_object_id(object_id: int, map_type: MapType):

    if map_type == MapType.OVERWORLD:
        if object_id in OverworldObjects._value2member_map_.keys():
            return OverworldObjects(object_id)
        elif object_id in IndoorObjects._value2member_map_.keys():
            return IndoorObjects(object_id)
        else:
            try:
                return OtherObjects(object_id)
            except ValueError:
                return OtherObjects.ERROR
        
    elif map_type == MapType.INDOORS_A or map_type == MapType.INDOORS_B:
        if object_id in IndoorObjects._value2member_map_.keys():
            return IndoorObjects(object_id)
        elif object_id in OverworldObjects._value2member_map_.keys():
            return OverworldObjects(object_id)
        else:
            try:
                return OtherObjects(object_id)
            except ValueError:
                return OtherObjects.ERROR
    else:
        raise ValueError(f"Unknown MapType {map_type}")
        
    


def lookup_object_physics(object_id: int, map_type: MapType):

    if map_type == MapType.OVERWORLD:
        return OVERWORLD_OBJECTS_PHYSICS.get(object_id, PhysicsFlags.OBJ_PHYSICS_NONE)
    elif map_type == MapType.INDOORS_A:
        return INDOOR1_OBJECTS_PHYSICS.get(object_id, PhysicsFlags.OBJ_PHYSICS_NONE)
    elif map_type == MapType.INDOORS_B:
        return INDOOR2_OBJECTS_PHYSICS.get(object_id, PhysicsFlags.OBJ_PHYSICS_NONE)
    else:
        raise ValueError(f"Unknown MapType {map_type}")

# Object types found here:
# https://github.com/zladx/LADX-Disassembly/blob/583c78d2f2a5258b87bf133f75b7129228255650/src/constants/gfx.asm#L211

class OtherObjects(Enum):
    NONE = 0x00
    ERROR = 0xFF

class OverworldObjects(Enum):
    OBJECT_SHORT_GRASS = 0x04
    OBJECT_ROCKY_GROUND = 0x09
    OBJECT_TALL_GRASS = 0x0A
    OBJECT_PATH = 0x0B
    OBJECT_TILES = 0x0C
    OBJECT_WATER_BANK_BOTTOM = 0x0F
    OBJECT_WATER_BANK_TOP = 0x10
    OBJECT_WATER_BANK_RIGHT = 0x11
    OBJECT_WATER_BANK_CORNER_TL = 0x13
    OBJECT_WATER_BANK_CORNER_BR = 0x16
    OBJECT_WATER_BANK_BR = 0x17
    OBJECT_WATER_BANK_BL = 0x18
    OBJECT_WATER_BANK_TR = 0x19
    OBJECT_WATER_BANK_TL = 0x1A
    OBJECT_SHALLOW_WATER = 0x1B
    OBJECT_LIFTABLE_ROCK = 0x20
    OBJECT_TREE_TOP_LEFT = 0x25
    OBJECT_TREE_TOP_RIGHT = 0x26
    OBJECT_TREE_BOTTOM_LEFT = 0x27
    OBJECT_TREE_BOTTOM_RIGHT = 0x28
    OBJECT_TREE_OVERLAP_LEFT = 0x29
    OBJECT_TREE_OVERLAP_RIGHT = 0x2A
    OBJECT_CLIFF_CORNER_BL = 0x2E
    OBJECT_CLIFF_BOTTOM = 0x2F
    OBJECT_CLIFF_LEFT = 0x37
    OBJECT_CLIFF_RIGHT = 0x38
    OBJECT_CLIFF_CORNER_BL_2 = 0x39 # This looks like object cliff corner BL
    OBJECT_CLIFF_BOTTOM_2 = 0x3A # This looks like object cliff bottom 
    OBJECT_CLIFF_CORNER_TL = 0x80
    OBJECT_CLIFF_CORNER_TR = 0x81
    OBJECT_ANIMATED_FLOWERS = 0x44
    OBJECT_PHONE_BOOTH_TOP = 0x45
    OBJECT_CLIFF_TOP = 0x4D
    OBJECT_BUSH = 0x5C
    OBJECT_WEATHER_VANE_BASE = 0x5E
    OBJECT_WELL = 0x61
    OBJECT_HURT_TILE = 0x69
    OBJECT_ROUNDED_BLOCK = 0x6E
    OBJECT_OWL_STATUE = 0x6F
    OBJECT_TREE_BUSHES_BOTTOM_LEFT = 0x82
    OBJECT_TREE_BUSHES_BOTTOM_RIGHT = 0x83
    OBJECT_WEATHER_VANE_TOP = 0x91
    OBJECT_BOMBABLE_CAVE_DOOR = 0xBA
    OBJECT_TAIL_KEYHOLE = 0xC0
    OBJECT_CLOSED_GATE = 0xC2
    OBJECT_GROUND_STAIRS = 0xC6
    OBJECT_BUSH_GROUND_STAIRS = 0xD3
    OBJECT_SIGNPOST = 0xD4
    OBJECT_MONKEY_BRIDGE_TOP = 0xD8
    OBJECT_MONKEY_BRIDGE_MIDDLE = 0xD9
    OBJECT_MONKEY_BRIDGE_BOTTOM = 0xDA
    OBJECT_MONKEY_BRIDGE_BUILT = 0xDB
    OBJECT_WEATHER_VANE_ABOVE = 0xDC
    OBJECT_STEPS = 0xE0
    OBJECT_GROUND_HOLE = 0xE8
    OBJECT_ROCKY_CAVE_DOOR = 0xE1
    OBJECT_CAVE_DOOR = 0xE3
    OBJECT_PIT = 0xE8
    OBJECT_WATERFALL = 0xE9

    OBJECT_MACRO_TREE = 0xF5
    OBJECT_MACRO_TWO_DOORS_HOUSE = 0xF6
    OBJECT_MACRO_LARGE_HOUSE = 0xF7
    OBJECT_MACRO_CATFISH_MAW = 0xF8
    OBJECT_MACRO_PALACE_DOOR = 0xF9
    OBJECT_MACRO_STONE_PIG_HEAD = 0xFA
    OBJECT_MACRO_PALM_TREE = 0xFB
    OBJECT_MACRO_WALLED_PIT = 0xFC
    OBJECT_MACRO_SMALL_HOUSE = 0xFD

class IndoorObjects(Enum):
    OBJECT_FLOOR_OD = 0x0D
    OBJECT_LIFTABLE_POT = 0x20
    OBJECT_WALL_TOP = 0x21
    OBJECT_WALL_BOTTOM = 0x22
    OBJECT_WALL_LEFT = 0x23
    OBJECT_WALL_RIGHT = 0x24
    OBJECT_BOMBED_PASSAGE_VERTICAL = 0x3D
    OBJECT_BOMBED_PASSAGE_HORIZONTAL = 0x3E
    OBJECT_BOMBABLE_WALL_TOP = 0x3F
    OBJECT_BOMBABLE_WALL_BOTTOM = 0x40
    OBJECT_BOMBABLE_WALL_LEFT = 0x41
    OBJECT_BOMBABLE_WALL_RIGHT = 0x42
    OBJECT_HIDDEN_BOMBABLE_WALL_TOP = 0x47
    OBJECT_HIDDEN_BOMBABLE_WALL_BOTTOM = 0x48
    OBJECT_HIDDEN_BOMBABLE_WALL_LEFT = 0x49
    OBJECT_HIDDEN_BOMBABLE_WALL_RIGHT = 0x4A
    OBJECT_SIDE_VIEW_SPIKES = 0x4C
    OBJECT_DASHABLE_ROCK_1 = 0x4E
    OBJECT_DASHABLE_ROCK_2 = 0x4F
    OBJECT_HURT_TILE = 0x69 # Spikes
    OBJECT_POT_WITH_SWITCH = 0x8E
    OBJECT_DASHABLE_ROCK_3 = 0x88
    OBJECT_CHEST_CLOSED = 0xA0
    OBJECT_CHEST_OPEN = 0xA1
    OBJECT_PUSHABLE_BLOCK = 0xA7
    OBJECT_BOMBABLE_BLOCK = 0xA9
    OBJECT_SWITCH_BUTTON = 0xAA
    OBJECT_TORCH_UNLIT = 0xAB
    OBJECT_TORCH_LIT = 0xAC
    OBJECT_STAIRS_DOWN = 0xBE
    OBJECT_HIDDEN_STAIRS_DOWN = 0xBF
    OBJECT_ONE_EYED_STATUE = 0xC0
    OBJECT_STAIRS_UP = 0xCB
    OBJECT_CONVEYOR_BOTTOM = 0xCF
    OBJECT_CONVEYOR_TOP = 0xD0
    OBJECT_CONVEYOR_RIGHT = 0xD1
    OBJECT_CONVEYOR_LEFT = 0xD2
    OBJECT_TRENDY_GAME_BORDER = 0xD3
    OBJECT_RAISED_FENCE_TOP = 0xD5
    OBJECT_RAISED_FENCE_BOTTOM = 0xD6
    OBJECT_RAISED_FENCE_LEFT = 0xD7
    OBJECT_RAISED_FENCE_RIGHT = 0xD8
    OBJECT_LOWERED_BLOCK = 0xDB
    OBJECT_RAISED_BLOCK = 0xDC
    OBJECT_KEYHOLE_BLOCK = 0xDE
    OBJECT_KEY_DOOR_TOP = 0xEC
    OBJECT_KEY_DOOR_BOTTOM = 0xED
    OBJECT_KEY_DOOR_LEFT = 0xEE
    OBJECT_KEY_DOOR_RIGHT = 0xEF
    OBJECT_CLOSED_DOOR_TOP = 0xF0
    OBJECT_CLOSED_DOOR_BOTTOM = 0xF1
    OBJECT_CLOSED_DOOR_LEFT = 0xF2
    OBJECT_CLOSED_DOOR_RIGHT = 0xF3
    OBJECT_OPEN_DOOR_TOP = 0xF4
    OBJECT_OPEN_DOOR_BOTTOM = 0xF5
    OBJECT_OPEN_DOOR_LEFT = 0xF6
    OBJECT_OPEN_DOOR_RIGHT = 0xF7
    OBJECT_BOSS_DOOR = 0xF8
    OBJECT_STAIRS_DOOR = 0xF9
    OBJECT_FLIP_WALL = 0xFA
    OBJECT_ONE_WAY_ARROW = 0xFB
    OBJECT_DUNGEON_ENTRANCE = 0xFC
    OBJECT_INDOOR_ENTRANCE = 0xFD

# Physics Flags Found here
# https://github.com/zladx/LADX-Disassembly/blob/583c78d2f2a5258b87bf133f75b7129228255650/src/constants/physics.asm#L20

class PhysicsFlags(Enum):

    OBJ_PHYSICS_NONE = 0x00 #pass-through
    OBJ_PHYSICS_SOLID = 0x01
    OBJ_PHYSICS_STAIRS = 0x02
    OBJ_PHYSICS_DOOR = 0x03
    OBJ_PHYSICS_OCEAN = 0x04 # blocks enemies but not projectiles?
    OBJ_PHYSICS_SHALLOW_WATER = 0x05
    OBJ_PHYSICS_GRASS = 0x06 # cuttable
    OBJ_PHYSICS_DEEP_WATER = 0x07
    OBJ_PHYSICS_BRIDGE = 0x08 # offsets the sprite up a few pixels
    OBJ_PHYSICS_STAIRS_DOWN = 0x09
    OBJ_PHYSICS_WIDE_STAIRS = 0x0A
    OBJ_PHYSICS_LAVA = 0x0B
    OBJ_PHYSICS_LEDGE_OVERWORLD = 0x10 # jumpable, only downwards
    OBJ_PHYSICS_REMOVABLE_OBSTACLE = 0x30 # bush/rock/keyblock/cracked block/sword-crystals
    OBJ_PHYSICS_PIT = 0x50
    OBJ_PHYSICS_PIT_WARP = 0x51 # pit with warp to other room (D1 boss, D7)
    OBJ_PHYSICS_HOOKSHOTABLE = 0x60 # solid or dash-crystal
    OBJ_PHYSICS_DOOR_OPEN = 0x70 # open door/flip door
    
    #OBJ_PHYSICS_FINE_COLLISION = 0x80 # for 8x8 tile collision. 0-3: side; 4-7: inward corner; 8-B: outward corner
    # Custom based on comments
    OBJ_PHYSICS_FINE_COLLISION_SIDE_1 = 0x80
    OBJ_PHYSICS_FINE_COLLISION_SIDE_2 = 0x81
    OBJ_PHYSICS_FINE_COLLISION_SIDE_3 = 0x82
    OBJ_PHYSICS_FINE_COLLISION_SIDE_4 = 0x83
    OBJ_PHYSICS_FINE_COLLISION_CORNER_INWARD_1 = 0x84
    OBJ_PHYSICS_FINE_COLLISION_CORNER_INWARD_2 = 0x85
    OBJ_PHYSICS_FINE_COLLISION_CORNER_INWARD_3 = 0x86
    OBJ_PHYSICS_FINE_COLLISION_CORNER_INWARD_4 = 0x87
    OBJ_PHYSICS_FINE_COLLISION_CORNER_OUTWARD_1 = 0x88
    OBJ_PHYSICS_FINE_COLLISION_CORNER_OUTWARD_2 = 0x89
    OBJ_PHYSICS_FINE_COLLISION_CORNER_OUTWARD_3 = 0x8A
    OBJ_PHYSICS_FINE_COLLISION_CORNER_OUTWARD_4 = 0x8B
    OBJ_PHYSICS_FINE_COLLISION_MYST_1 = 0x8C # Not in comment?
    OBJ_PHYSICS_FINE_COLLISION_MYST_2 = 0x8D
    OBJ_PHYSICS_FINE_COLLISION_MYST_3 = 0x8E
    OBJ_PHYSICS_FINE_COLLISION_MYST_4 = 0x8F
    ## End Custom
    
    #OBJ_PHYSICS_DOOR_CLOSED = 0x90 # 0-3: key door; 8: boss door; 9-C: bombable door/wall
    # Custom based on comments
    OBJ_PHySICS_DOOR_CLOSED_KEY_1 = 0x90
    OBJ_PHYSICS_DOOR_CLOSED_KEY_2 = 0x91
    OBJ_PHYSICS_DOOR_CLOSED_KEY_3 = 0x92
    OBJ_PHYSICS_DOOR_CLOSED_KEY_4 = 0x93
    OBJ_PHYSICS_DOOR_CLOSED_BOSS_DOOR = 0x98
    OBJ_PHYSICS_DOOR_CLOSED_BOMBABLE_1 = 0x99
    OBJ_PHYSICS_DOOR_CLOSED_BOMBABLE_2 = 0x9A
    OBJ_PHYSICS_DOOR_CLOSED_BOMBABLE_3 = 0x9B
    OBJ_PHYSICS_DOOR_CLOSED_BOMBABLE_4 = 0x9C
    ## End Custom

    OBJ_PHYSICS_WATER_SIDESCROLL = 0xB0
    OBJ_PHYSICS_LADDER_SIDESCROLL = 0xB1
    OBJ_PHYSICS_KEYHOLE = 0xC0

    #OBJ_PHYSICS_LEDGE = 0xD0 # jumpable, 0-3: direction
    # Custom based on comments
    OBJ_PHYSICS_LEDGE_1 = 0xD0
    OBJ_PHYSICS_LEDGE_2 = 0xD1
    OBJ_PHYSICS_LEDGE_3 = 0xD2
    OBJ_PHYSICS_LEDGE_4 = 0xD3
    ## End Custom

    OBJ_PHYSICS_SPIKES = 0xE0
    #OBJ_PHYSICS_CONVEYOR = 0xF0 # but not rapids. 0-3: side; 4-7: diagonal
    # Custom based on comments
    OBJ_PHYSICS_CONVEYOR_SIDE_1 = 0xF0
    OBJ_PHYSICS_CONVEYOR_SIDE_2 = 0xF1
    OBJ_PHYSICS_CONVEYOR_SIDE_3 = 0xF2
    OBJ_PHYSICS_CONVEYOR_SIDE_4 = 0xF3
    OBJ_PHYSICS_CONVEYOR_DIAGONAL_1 = 0xF4
    OBJ_PHYSICS_CONVEYOR_DIAGONAL_2 = 0xF5
    OBJ_PHYSICS_CONVEYOR_DIAGONAL_3 = 0xF6
    OBJ_PHYSICS_CONVEYOR_DIAGONAL_4 = 0xF7
    ## End Custom

    OBJ_PHYSICS_UNUSED = 0xFE
    OBJ_PHYSICS_INVALID = 0xFF

# This is a Custom Thing

class CustomPhysicsFlags(Flag):
    NONE = 0
    SOLID = 1
    WARP = 2
    INTERACT = 4
    WATER = 8
    PIT = 16
    LEDGE = 32
    SIDESCROLL = 64

# Categorise the Phsyics Flags a Little
TRANSLATE_PHYSICS_FLAGS = {

    PhysicsFlags.OBJ_PHYSICS_NONE: CustomPhysicsFlags.NONE,
    PhysicsFlags.OBJ_PHYSICS_SOLID: CustomPhysicsFlags.SOLID,
    PhysicsFlags.OBJ_PHYSICS_STAIRS: CustomPhysicsFlags.WARP,
    PhysicsFlags.OBJ_PHYSICS_DOOR: CustomPhysicsFlags.WARP,
    PhysicsFlags.OBJ_PHYSICS_OCEAN: CustomPhysicsFlags.WATER | CustomPhysicsFlags.SOLID,
    PhysicsFlags.OBJ_PHYSICS_SHALLOW_WATER: CustomPhysicsFlags.WATER,
    PhysicsFlags.OBJ_PHYSICS_GRASS: CustomPhysicsFlags.INTERACT | CustomPhysicsFlags.SOLID,
    PhysicsFlags.OBJ_PHYSICS_DEEP_WATER: CustomPhysicsFlags.WATER | CustomPhysicsFlags.SOLID,
    PhysicsFlags.OBJ_PHYSICS_BRIDGE: CustomPhysicsFlags.NONE,
    PhysicsFlags.OBJ_PHYSICS_STAIRS_DOWN: CustomPhysicsFlags.WARP,
    PhysicsFlags.OBJ_PHYSICS_WIDE_STAIRS: CustomPhysicsFlags.WARP,
    PhysicsFlags.OBJ_PHYSICS_LAVA: CustomPhysicsFlags.WATER | CustomPhysicsFlags.SOLID,
    PhysicsFlags.OBJ_PHYSICS_LEDGE_OVERWORLD: CustomPhysicsFlags.LEDGE,
    PhysicsFlags.OBJ_PHYSICS_REMOVABLE_OBSTACLE: CustomPhysicsFlags.INTERACT | CustomPhysicsFlags.SOLID,
    PhysicsFlags.OBJ_PHYSICS_PIT: CustomPhysicsFlags.PIT,
    PhysicsFlags.OBJ_PHYSICS_PIT_WARP: CustomPhysicsFlags.PIT | CustomPhysicsFlags.WARP,
    PhysicsFlags.OBJ_PHYSICS_HOOKSHOTABLE: CustomPhysicsFlags.INTERACT | CustomPhysicsFlags.SOLID,
    PhysicsFlags.OBJ_PHYSICS_DOOR_OPEN: CustomPhysicsFlags.WARP,
    PhysicsFlags.OBJ_PHYSICS_FINE_COLLISION_SIDE_1 : CustomPhysicsFlags.SOLID,
    PhysicsFlags.OBJ_PHYSICS_FINE_COLLISION_SIDE_2 : CustomPhysicsFlags.SOLID,
    PhysicsFlags.OBJ_PHYSICS_FINE_COLLISION_SIDE_3 : CustomPhysicsFlags.SOLID,
    PhysicsFlags.OBJ_PHYSICS_FINE_COLLISION_SIDE_4 : CustomPhysicsFlags.SOLID,
    PhysicsFlags.OBJ_PHYSICS_FINE_COLLISION_CORNER_INWARD_1 : CustomPhysicsFlags.SOLID,
    PhysicsFlags.OBJ_PHYSICS_FINE_COLLISION_CORNER_INWARD_2 : CustomPhysicsFlags.SOLID,
    PhysicsFlags.OBJ_PHYSICS_FINE_COLLISION_CORNER_INWARD_3 : CustomPhysicsFlags.SOLID,
    PhysicsFlags.OBJ_PHYSICS_FINE_COLLISION_CORNER_INWARD_4 : CustomPhysicsFlags.SOLID,
    PhysicsFlags.OBJ_PHYSICS_FINE_COLLISION_CORNER_OUTWARD_1 : CustomPhysicsFlags.NONE,
    PhysicsFlags.OBJ_PHYSICS_FINE_COLLISION_CORNER_OUTWARD_2 : CustomPhysicsFlags.NONE,
    PhysicsFlags.OBJ_PHYSICS_FINE_COLLISION_CORNER_OUTWARD_3 : CustomPhysicsFlags.NONE,
    PhysicsFlags.OBJ_PHYSICS_FINE_COLLISION_CORNER_OUTWARD_4 : CustomPhysicsFlags.NONE,
    PhysicsFlags.OBJ_PHYSICS_FINE_COLLISION_MYST_1 : CustomPhysicsFlags.SOLID,
    PhysicsFlags.OBJ_PHYSICS_FINE_COLLISION_MYST_2 : CustomPhysicsFlags.SOLID,
    PhysicsFlags.OBJ_PHYSICS_FINE_COLLISION_MYST_3 : CustomPhysicsFlags.SOLID,
    PhysicsFlags.OBJ_PHYSICS_FINE_COLLISION_MYST_4 : CustomPhysicsFlags.SOLID,
    PhysicsFlags.OBJ_PHySICS_DOOR_CLOSED_KEY_1 : CustomPhysicsFlags.WARP | CustomPhysicsFlags.SOLID | CustomPhysicsFlags.INTERACT,
    PhysicsFlags.OBJ_PHYSICS_DOOR_CLOSED_KEY_2 : CustomPhysicsFlags.WARP | CustomPhysicsFlags.SOLID | CustomPhysicsFlags.INTERACT,
    PhysicsFlags.OBJ_PHYSICS_DOOR_CLOSED_KEY_3 : CustomPhysicsFlags.WARP | CustomPhysicsFlags.SOLID | CustomPhysicsFlags.INTERACT,
    PhysicsFlags.OBJ_PHYSICS_DOOR_CLOSED_KEY_4 : CustomPhysicsFlags.WARP | CustomPhysicsFlags.SOLID | CustomPhysicsFlags.INTERACT,
    PhysicsFlags.OBJ_PHYSICS_DOOR_CLOSED_BOSS_DOOR : CustomPhysicsFlags.WARP | CustomPhysicsFlags.SOLID | CustomPhysicsFlags.INTERACT,
    PhysicsFlags.OBJ_PHYSICS_DOOR_CLOSED_BOMBABLE_1 : CustomPhysicsFlags.WARP | CustomPhysicsFlags.SOLID | CustomPhysicsFlags.INTERACT,
    PhysicsFlags.OBJ_PHYSICS_DOOR_CLOSED_BOMBABLE_2 : CustomPhysicsFlags.WARP | CustomPhysicsFlags.SOLID | CustomPhysicsFlags.INTERACT,
    PhysicsFlags.OBJ_PHYSICS_DOOR_CLOSED_BOMBABLE_3 : CustomPhysicsFlags.WARP | CustomPhysicsFlags.SOLID | CustomPhysicsFlags.INTERACT,
    PhysicsFlags.OBJ_PHYSICS_DOOR_CLOSED_BOMBABLE_4 : CustomPhysicsFlags.WARP | CustomPhysicsFlags.SOLID | CustomPhysicsFlags.INTERACT,
    PhysicsFlags.OBJ_PHYSICS_WATER_SIDESCROLL : CustomPhysicsFlags.WATER | CustomPhysicsFlags.SIDESCROLL,
    PhysicsFlags.OBJ_PHYSICS_LADDER_SIDESCROLL : CustomPhysicsFlags.INTERACT | CustomPhysicsFlags.SIDESCROLL,
    PhysicsFlags.OBJ_PHYSICS_KEYHOLE : CustomPhysicsFlags.INTERACT | CustomPhysicsFlags.SOLID,
    PhysicsFlags.OBJ_PHYSICS_LEDGE_1 : CustomPhysicsFlags.LEDGE,
    PhysicsFlags.OBJ_PHYSICS_LEDGE_2 : CustomPhysicsFlags.LEDGE,
    PhysicsFlags.OBJ_PHYSICS_LEDGE_3 : CustomPhysicsFlags.LEDGE,
    PhysicsFlags.OBJ_PHYSICS_LEDGE_4 : CustomPhysicsFlags.LEDGE,
    PhysicsFlags.OBJ_PHYSICS_SPIKES : CustomPhysicsFlags.SOLID,
    PhysicsFlags.OBJ_PHYSICS_CONVEYOR_SIDE_1 : CustomPhysicsFlags.NONE,
    PhysicsFlags.OBJ_PHYSICS_CONVEYOR_SIDE_2 : CustomPhysicsFlags.NONE,
    PhysicsFlags.OBJ_PHYSICS_CONVEYOR_SIDE_3 : CustomPhysicsFlags.NONE,
    PhysicsFlags.OBJ_PHYSICS_CONVEYOR_SIDE_4 : CustomPhysicsFlags.NONE,
    PhysicsFlags.OBJ_PHYSICS_CONVEYOR_DIAGONAL_1 : CustomPhysicsFlags.NONE,
    PhysicsFlags.OBJ_PHYSICS_CONVEYOR_DIAGONAL_2 : CustomPhysicsFlags.NONE,
    PhysicsFlags.OBJ_PHYSICS_CONVEYOR_DIAGONAL_3 : CustomPhysicsFlags.NONE,
    PhysicsFlags.OBJ_PHYSICS_CONVEYOR_DIAGONAL_4 : CustomPhysicsFlags.NONE,
    PhysicsFlags.OBJ_PHYSICS_UNUSED : CustomPhysicsFlags.NONE,
    PhysicsFlags.OBJ_PHYSICS_INVALID : CustomPhysicsFlags.SOLID,

}



class CollisionFlags(IntEnum):
    COLLISION_TYPE_NONE = 0x00
    COLLISION_TYPE_UP = 0x01
    COLLISION_TYPE_DOWN = 0x02
    COLLISION_TYPE_VERTICAL = 0x03
    COLLISION_TYPE_LEFT = 0x04
    COLLISION_TYPE_RIGHT = 0x08
    COLLISION_TYPE_HORIZONTAL = 0x0C
    COLLISION_TYPE_UNKNOWN_10 = 0x10

# Object Physics Flags found here
# https://github.com/zladx/LADX-Disassembly/blob/583c78d2f2a5258b87bf133f75b7129228255650/src/data/objects/physics.asm#L55





OVERWORLD_OBJECTS_PHYSICS = {
    0x00 : PhysicsFlags.OBJ_PHYSICS_SOLID,
    0x01 : PhysicsFlags.OBJ_PHYSICS_NONE,
    0x02 : PhysicsFlags.OBJ_PHYSICS_NONE,
    0x03 : PhysicsFlags.OBJ_PHYSICS_NONE,
    0x04 : PhysicsFlags.OBJ_PHYSICS_NONE,
    0x05 : PhysicsFlags.OBJ_PHYSICS_SOLID,
    0x06 : PhysicsFlags.OBJ_PHYSICS_SOLID,
    0x07 : PhysicsFlags.OBJ_PHYSICS_SOLID,
    0x08 : PhysicsFlags.OBJ_PHYSICS_NONE,
    0x09 : PhysicsFlags.OBJ_PHYSICS_NONE,
    0x0A : PhysicsFlags.OBJ_PHYSICS_GRASS,
    0x0B : PhysicsFlags.OBJ_PHYSICS_NONE,
    0x0C : PhysicsFlags.OBJ_PHYSICS_NONE,
    0x0D : PhysicsFlags.OBJ_PHYSICS_NONE,
    0x0E : PhysicsFlags.OBJ_PHYSICS_DEEP_WATER,
    0x0F : PhysicsFlags.OBJ_PHYSICS_NONE,
    0x10 : PhysicsFlags.OBJ_PHYSICS_NONE,
    0x11 : PhysicsFlags.OBJ_PHYSICS_NONE,
    0x12 : PhysicsFlags.OBJ_PHYSICS_NONE,
    0x13 : PhysicsFlags.OBJ_PHYSICS_NONE,
    0x14 : PhysicsFlags.OBJ_PHYSICS_NONE,
    0x15 : PhysicsFlags.OBJ_PHYSICS_NONE,
    0x16 : PhysicsFlags.OBJ_PHYSICS_NONE,
    0x17 : PhysicsFlags.OBJ_PHYSICS_NONE,
    0x18 : PhysicsFlags.OBJ_PHYSICS_NONE,
    0x19 : PhysicsFlags.OBJ_PHYSICS_NONE,
    0x1A : PhysicsFlags.OBJ_PHYSICS_NONE,
    0x1B : PhysicsFlags.OBJ_PHYSICS_SHALLOW_WATER,
    0x1C : PhysicsFlags.OBJ_PHYSICS_SOLID,
    0x1D : PhysicsFlags.OBJ_PHYSICS_SOLID,
    0x1E : PhysicsFlags.OBJ_PHYSICS_SHALLOW_WATER,
    0x1F : PhysicsFlags.OBJ_PHYSICS_OCEAN,
    0x20 : PhysicsFlags.OBJ_PHYSICS_REMOVABLE_OBSTACLE,
    0x21 : PhysicsFlags.OBJ_PHYSICS_SOLID,
    0x22 : PhysicsFlags.OBJ_PHYSICS_SOLID,
    0x23 : PhysicsFlags.OBJ_PHYSICS_NONE,
    0x24 : PhysicsFlags.OBJ_PHYSICS_NONE,
    0x25 : PhysicsFlags.OBJ_PHYSICS_SOLID,
    0x26 : PhysicsFlags.OBJ_PHYSICS_SOLID,
    0x27 : PhysicsFlags.OBJ_PHYSICS_SOLID,
    0x28 : PhysicsFlags.OBJ_PHYSICS_SOLID,
    0x29 : PhysicsFlags.OBJ_PHYSICS_SOLID,
    0x2A : PhysicsFlags.OBJ_PHYSICS_SOLID,
    0x2B : PhysicsFlags.OBJ_PHYSICS_SOLID,
    0x2C : PhysicsFlags.OBJ_PHYSICS_SOLID,
    0x2D : PhysicsFlags.OBJ_PHYSICS_SOLID,
    0x2E : PhysicsFlags.OBJ_PHYSICS_SOLID,
    0x2F : PhysicsFlags.OBJ_PHYSICS_SOLID,
    0x30 : PhysicsFlags.OBJ_PHYSICS_SHALLOW_WATER,
    0x31 : PhysicsFlags.OBJ_PHYSICS_SOLID,
    0x32 : PhysicsFlags.OBJ_PHYSICS_SOLID,
    0x33 : PhysicsFlags.OBJ_PHYSICS_SOLID,
    0x34 : PhysicsFlags.OBJ_PHYSICS_SOLID,
    0x35 : PhysicsFlags.OBJ_PHYSICS_SOLID,
    0x36 : PhysicsFlags.OBJ_PHYSICS_SOLID,
    0x37 : PhysicsFlags.OBJ_PHYSICS_SOLID,
    0x38 : PhysicsFlags.OBJ_PHYSICS_SOLID,
    0x39 : PhysicsFlags.OBJ_PHYSICS_SOLID,
    0x3A : PhysicsFlags.OBJ_PHYSICS_SOLID,
    0x3B : PhysicsFlags.OBJ_PHYSICS_SOLID,
    0x3C : PhysicsFlags.OBJ_PHYSICS_SOLID,
    0x3D : PhysicsFlags.OBJ_PHYSICS_SOLID,
    0x3E : PhysicsFlags.OBJ_PHYSICS_SOLID,
    0x3F : PhysicsFlags.OBJ_PHYSICS_SOLID,
    0x40 : PhysicsFlags.OBJ_PHYSICS_SOLID,
    0x41 : PhysicsFlags.OBJ_PHYSICS_SOLID,
    0x42 : PhysicsFlags.OBJ_PHYSICS_SOLID,
    0x43 : PhysicsFlags.OBJ_PHYSICS_LEDGE_OVERWORLD,
    0x44 : PhysicsFlags.OBJ_PHYSICS_NONE,
    0x45 : PhysicsFlags.OBJ_PHYSICS_SOLID,
    0x46 : PhysicsFlags.OBJ_PHYSICS_SOLID,
    0x47 : PhysicsFlags.OBJ_PHYSICS_SOLID,
    0x48 : PhysicsFlags.OBJ_PHYSICS_SOLID,
    0x49 : PhysicsFlags.OBJ_PHYSICS_SOLID,
    0x4A : PhysicsFlags.OBJ_PHYSICS_LEDGE_OVERWORLD,
    0x4B : PhysicsFlags.OBJ_PHYSICS_SOLID,
    0x4C : PhysicsFlags.OBJ_PHYSICS_SOLID,
    0x4D : PhysicsFlags.OBJ_PHYSICS_SOLID,
    0x4E : PhysicsFlags.OBJ_PHYSICS_SOLID,
    0x4F : PhysicsFlags.OBJ_PHYSICS_SOLID,
    0x50 : PhysicsFlags.OBJ_PHYSICS_SOLID,
    0x51 : PhysicsFlags.OBJ_PHYSICS_SOLID,
    0x52 : PhysicsFlags.OBJ_PHYSICS_SOLID,
    0x53 : PhysicsFlags.OBJ_PHYSICS_WIDE_STAIRS,
    0x54 : PhysicsFlags.OBJ_PHYSICS_KEYHOLE,
    0x55 : PhysicsFlags.OBJ_PHYSICS_SOLID,
    0x56 : PhysicsFlags.OBJ_PHYSICS_SOLID,
    0x57 : PhysicsFlags.OBJ_PHYSICS_SOLID,
    0x58 : PhysicsFlags.OBJ_PHYSICS_SOLID,
    0x59 : PhysicsFlags.OBJ_PHYSICS_SOLID,
    0x5A : PhysicsFlags.OBJ_PHYSICS_SOLID,
    0x5B : PhysicsFlags.OBJ_PHYSICS_SOLID,
    0x5C : PhysicsFlags.OBJ_PHYSICS_REMOVABLE_OBSTACLE,
    0x5D : PhysicsFlags.OBJ_PHYSICS_SOLID,
    0x5E : PhysicsFlags.OBJ_PHYSICS_SOLID,
    0x5F : PhysicsFlags.OBJ_PHYSICS_SOLID,
    0x60 : PhysicsFlags.OBJ_PHYSICS_SOLID,
    0x61 : PhysicsFlags.OBJ_PHYSICS_SOLID,
    0x62 : PhysicsFlags.OBJ_PHYSICS_SOLID,
    0x63 : PhysicsFlags.OBJ_PHYSICS_SOLID,
    0x64 : PhysicsFlags.OBJ_PHYSICS_SOLID,
    0x65 : PhysicsFlags.OBJ_PHYSICS_SOLID,
    0x66 : PhysicsFlags.OBJ_PHYSICS_SOLID,
    0x67 : PhysicsFlags.OBJ_PHYSICS_SOLID,
    0x68 : PhysicsFlags.OBJ_PHYSICS_SOLID,
    0x69 : PhysicsFlags.OBJ_PHYSICS_SOLID,
    0x6A : PhysicsFlags.OBJ_PHYSICS_SOLID,
    0x6B : PhysicsFlags.OBJ_PHYSICS_SOLID,
    0x6C : PhysicsFlags.OBJ_PHYSICS_SOLID,
    0x6D : PhysicsFlags.OBJ_PHYSICS_SOLID,
    0x6E : PhysicsFlags.OBJ_PHYSICS_HOOKSHOTABLE,
    0x6F : PhysicsFlags.OBJ_PHYSICS_SOLID,
    0x70 : PhysicsFlags.OBJ_PHYSICS_KEYHOLE,
    0x71 : PhysicsFlags.OBJ_PHYSICS_SOLID,
    0x72 : PhysicsFlags.OBJ_PHYSICS_SOLID,
    0x73 : PhysicsFlags.OBJ_PHYSICS_SOLID,
    0x74 : PhysicsFlags.OBJ_PHYSICS_SOLID,
    0x75 : PhysicsFlags.OBJ_PHYSICS_SOLID,
    0x76 : PhysicsFlags.OBJ_PHYSICS_SOLID,
    0x77 : PhysicsFlags.OBJ_PHYSICS_STAIRS,
    0x78 : PhysicsFlags.OBJ_PHYSICS_BRIDGE,
    0x79 : PhysicsFlags.OBJ_PHYSICS_BRIDGE,
    0x7A : PhysicsFlags.OBJ_PHYSICS_BRIDGE,
    0x7B : PhysicsFlags.OBJ_PHYSICS_PIT,
    0x7C : PhysicsFlags.OBJ_PHYSICS_SOLID,
    0x7D : PhysicsFlags.OBJ_PHYSICS_SOLID,
    0x7E : PhysicsFlags.OBJ_PHYSICS_SOLID,
    0x7F : PhysicsFlags.OBJ_PHYSICS_SOLID,
    0x80 : PhysicsFlags.OBJ_PHYSICS_SOLID,
    0x81 : PhysicsFlags.OBJ_PHYSICS_SOLID,
    0x82 : PhysicsFlags.OBJ_PHYSICS_SOLID,
    0x83 : PhysicsFlags.OBJ_PHYSICS_SOLID,
    0x84 : PhysicsFlags.OBJ_PHYSICS_SOLID,
    0x85 : PhysicsFlags.OBJ_PHYSICS_SOLID,
    0x86 : PhysicsFlags.OBJ_PHYSICS_SOLID,
    0x87 : PhysicsFlags.OBJ_PHYSICS_SOLID,
    0x88 : PhysicsFlags.OBJ_PHYSICS_SOLID,
    0x89 : PhysicsFlags.OBJ_PHYSICS_SOLID,
    0x8A : PhysicsFlags.OBJ_PHYSICS_SOLID,
    0x8B : PhysicsFlags.OBJ_PHYSICS_SOLID,
    0x8C : PhysicsFlags.OBJ_PHYSICS_SOLID,
    0x8D : PhysicsFlags.OBJ_PHYSICS_SOLID,
    0x8E : PhysicsFlags.OBJ_PHYSICS_SOLID,
    0x8F : PhysicsFlags.OBJ_PHYSICS_SOLID,
    0x90 : PhysicsFlags.OBJ_PHYSICS_SOLID,
    0x91 : PhysicsFlags.OBJ_PHYSICS_SOLID,
    0x92 : PhysicsFlags.OBJ_PHYSICS_SOLID,
    0x93 : PhysicsFlags.OBJ_PHYSICS_SOLID,
    0x94 : PhysicsFlags.OBJ_PHYSICS_SOLID,
    0x95 : PhysicsFlags.OBJ_PHYSICS_SOLID,
    0x96 : PhysicsFlags.OBJ_PHYSICS_SOLID,
    0x97 : PhysicsFlags.OBJ_PHYSICS_SOLID,
    0x98 : PhysicsFlags.OBJ_PHYSICS_SOLID,
    0x99 : PhysicsFlags.OBJ_PHYSICS_SOLID,
    0x9A : PhysicsFlags.OBJ_PHYSICS_SOLID,
    0x9B : PhysicsFlags.OBJ_PHYSICS_SOLID,
    0x9C : PhysicsFlags.OBJ_PHYSICS_SOLID,
    0x9D : PhysicsFlags.OBJ_PHYSICS_SOLID,
    0x9E : PhysicsFlags.OBJ_PHYSICS_SOLID,
    0x9F : PhysicsFlags.OBJ_PHYSICS_SOLID,
    0xA0 : PhysicsFlags.OBJ_PHYSICS_HOOKSHOTABLE,
    0xA1 : PhysicsFlags.OBJ_PHYSICS_HOOKSHOTABLE,
    0xA2 : PhysicsFlags.OBJ_PHYSICS_SOLID,
    0xA3 : PhysicsFlags.OBJ_PHYSICS_SOLID,
    0xA4 : PhysicsFlags.OBJ_PHYSICS_NONE,
    0xA5 : PhysicsFlags.OBJ_PHYSICS_SOLID,
    0xA6 : PhysicsFlags.OBJ_PHYSICS_SOLID,
    0xA7 : PhysicsFlags.OBJ_PHYSICS_SOLID,
    0xA8 : PhysicsFlags.OBJ_PHYSICS_SOLID,
    0xA9 : PhysicsFlags.OBJ_PHYSICS_SOLID,
    0xAA : PhysicsFlags.OBJ_PHYSICS_SOLID,
    0xAB : PhysicsFlags.OBJ_PHYSICS_SOLID,
    0xAC : PhysicsFlags.OBJ_PHYSICS_SOLID,
    0xAD : PhysicsFlags.OBJ_PHYSICS_SOLID,
    0xAE : PhysicsFlags.OBJ_PHYSICS_SOLID,
    0xAF : PhysicsFlags.OBJ_PHYSICS_SOLID,
    0xB0 : PhysicsFlags.OBJ_PHYSICS_SOLID,
    0xB1 : PhysicsFlags.OBJ_PHYSICS_SOLID,
    0xB2 : PhysicsFlags.OBJ_PHYSICS_SOLID,
    0xB3 : PhysicsFlags.OBJ_PHYSICS_NONE,
    0xB4 : PhysicsFlags.OBJ_PHYSICS_SOLID,
    0xB5 : PhysicsFlags.OBJ_PHYSICS_SOLID,
    0xB6 : PhysicsFlags.OBJ_PHYSICS_SOLID,
    0xB7 : PhysicsFlags.OBJ_PHYSICS_SOLID,
    0xB8 : PhysicsFlags.OBJ_PHYSICS_SOLID,
    0xB9 : PhysicsFlags.OBJ_PHYSICS_NONE,
    0xBA : PhysicsFlags.OBJ_PHYSICS_DOOR_CLOSED_BOMBABLE_1, #PhysicsFlags.OBJ_PHYSICS_DOOR_CLOSED | $09
    0xBB : PhysicsFlags.OBJ_PHYSICS_SOLID,
    0xBC : PhysicsFlags.OBJ_PHYSICS_SOLID,
    0xBD : PhysicsFlags.OBJ_PHYSICS_SOLID,
    0xBE : PhysicsFlags.OBJ_PHYSICS_SOLID,
    0xBF : PhysicsFlags.OBJ_PHYSICS_SOLID,
    0xC0 : PhysicsFlags.OBJ_PHYSICS_KEYHOLE,
    0xC1 : PhysicsFlags.OBJ_PHYSICS_SOLID,
    0xC2 : PhysicsFlags.OBJ_PHYSICS_SOLID,
    0xC3 : PhysicsFlags.OBJ_PHYSICS_SOLID,
    0xC4 : PhysicsFlags.OBJ_PHYSICS_SOLID,
    0xC5 : PhysicsFlags.OBJ_PHYSICS_SOLID,
    0xC6 : PhysicsFlags.OBJ_PHYSICS_STAIRS_DOWN,
    0xC7 : PhysicsFlags.OBJ_PHYSICS_SOLID,
    0xC8 : PhysicsFlags.OBJ_PHYSICS_HOOKSHOTABLE,
    0xC9 : PhysicsFlags.OBJ_PHYSICS_SOLID,
    0xCA : PhysicsFlags.OBJ_PHYSICS_SOLID,
    0xCB : PhysicsFlags.OBJ_PHYSICS_DOOR,
    0xCC : PhysicsFlags.OBJ_PHYSICS_STAIRS_DOWN,
    0xCD : PhysicsFlags.OBJ_PHYSICS_SOLID,
    0xCE : PhysicsFlags.OBJ_PHYSICS_SOLID,
    0xCF : PhysicsFlags.OBJ_PHYSICS_CONVEYOR_DIAGONAL_1, #PhysicsFlags.OBJ_PHYSICS_CONVEYOR | $04
    0xD0 : PhysicsFlags.OBJ_PHYSICS_CONVEYOR_DIAGONAL_2, #PhysicsFlags.OBJ_PHYSICS_CONVEYOR | $05
    0xD1 : PhysicsFlags.OBJ_PHYSICS_CONVEYOR_DIAGONAL_3, #PhysicsFlags.OBJ_PHYSICS_CONVEYOR | $06
    0xD2 : PhysicsFlags.OBJ_PHYSICS_CONVEYOR_DIAGONAL_4, #PhysicsFlags.OBJ_PHYSICS_CONVEYOR | $07
    0xD3 : PhysicsFlags.OBJ_PHYSICS_REMOVABLE_OBSTACLE,
    0xD4 : PhysicsFlags.OBJ_PHYSICS_HOOKSHOTABLE,
    0xD5 : PhysicsFlags.OBJ_PHYSICS_SOLID,
    0xD6 : PhysicsFlags.OBJ_PHYSICS_SOLID,
    0xD7 : PhysicsFlags.OBJ_PHYSICS_SOLID,
    0xD8 : PhysicsFlags.OBJ_PHYSICS_SOLID,
    0xD9 : PhysicsFlags.OBJ_PHYSICS_DEEP_WATER,
    0xDA : PhysicsFlags.OBJ_PHYSICS_SOLID,
    0xDB : PhysicsFlags.OBJ_PHYSICS_BRIDGE,
    0xDC : PhysicsFlags.OBJ_PHYSICS_NONE,
    0xDD : PhysicsFlags.OBJ_PHYSICS_SOLID,
    0xDE : PhysicsFlags.OBJ_PHYSICS_SOLID,
    0xDF : PhysicsFlags.OBJ_PHYSICS_SOLID,
    0xE0 : PhysicsFlags.OBJ_PHYSICS_STAIRS,
    0xE1 : PhysicsFlags.OBJ_PHYSICS_DOOR,
    0xE2 : PhysicsFlags.OBJ_PHYSICS_DOOR,
    0xE3 : PhysicsFlags.OBJ_PHYSICS_DOOR,
    0xE4 : PhysicsFlags.OBJ_PHYSICS_SOLID,
    0xE5 : PhysicsFlags.OBJ_PHYSICS_SOLID,
    0xE6 : PhysicsFlags.OBJ_PHYSICS_FINE_COLLISION_SIDE_2, #PhysicsFlags.OBJ_PHYSICS_FINE_COLLISION | $01
    0xE7 : PhysicsFlags.OBJ_PHYSICS_DOOR,
    0xE8 : PhysicsFlags.OBJ_PHYSICS_PIT,
    0xE9 : PhysicsFlags.OBJ_PHYSICS_SOLID,
    0xEA : PhysicsFlags.OBJ_PHYSICS_SOLID,
    0xEB : PhysicsFlags.OBJ_PHYSICS_DEEP_WATER,
    0xEC : PhysicsFlags.OBJ_PHYSICS_DEEP_WATER,
    0xED : PhysicsFlags.OBJ_PHYSICS_DEEP_WATER,
    0xEE : PhysicsFlags.OBJ_PHYSICS_DEEP_WATER,
    0xEF : PhysicsFlags.OBJ_PHYSICS_PIT,
    0xF0 : PhysicsFlags.OBJ_PHYSICS_LEDGE_2, #PhysicsFlags.OBJ_PHYSICS_LEDGE | $01
    0xF1 : PhysicsFlags.OBJ_PHYSICS_SOLID,
    0xF2 : PhysicsFlags.OBJ_PHYSICS_SOLID,
    0xF3 : PhysicsFlags.OBJ_PHYSICS_LEDGE_1, #PhysicsFlags.OBJ_PHYSICS_LEDGE | $00
    0xF4 : PhysicsFlags.OBJ_PHYSICS_SOLID,
    0xF5 : PhysicsFlags.OBJ_PHYSICS_SOLID,
    0xF6 : PhysicsFlags.OBJ_PHYSICS_SOLID,
    0xF7 : PhysicsFlags.OBJ_PHYSICS_SOLID,
    0xF8 : PhysicsFlags.OBJ_PHYSICS_SOLID,
    0xF9 : PhysicsFlags.OBJ_PHYSICS_SOLID,
    0xFA : PhysicsFlags.OBJ_PHYSICS_SOLID,
    0xFB : PhysicsFlags.OBJ_PHYSICS_SOLID,
    0xFC : PhysicsFlags.OBJ_PHYSICS_SOLID,
    0xFD : PhysicsFlags.OBJ_PHYSICS_SOLID,
    0xFE : PhysicsFlags.OBJ_PHYSICS_SOLID,
    0xFF : PhysicsFlags.OBJ_PHYSICS_INVALID,

}

INDOOR1_OBJECTS_PHYSICS = {

    0x00 : PhysicsFlags.OBJ_PHYSICS_NONE,
    0x01 : PhysicsFlags.OBJ_PHYSICS_PIT,
    0x02 : PhysicsFlags.OBJ_PHYSICS_NONE,
    0x03 : PhysicsFlags.OBJ_PHYSICS_NONE,
    0x04 : PhysicsFlags.OBJ_PHYSICS_NONE,
    0x05 : PhysicsFlags.OBJ_PHYSICS_NONE,
    0x06 : PhysicsFlags.OBJ_PHYSICS_LAVA,
    0x07 : PhysicsFlags.OBJ_PHYSICS_NONE,
    0x08 : PhysicsFlags.OBJ_PHYSICS_DOOR_OPEN, #| $0D
    0x09 : PhysicsFlags.OBJ_PHYSICS_DOOR_OPEN, #| $0E
    0x0A : PhysicsFlags.OBJ_PHYSICS_DOOR_OPEN, #| $0F
    0x0B : PhysicsFlags.OBJ_PHYSICS_DOOR_OPEN, #| $0E
    0x0C : PhysicsFlags.OBJ_PHYSICS_DOOR_OPEN, #| $0F
    0x0D : PhysicsFlags.OBJ_PHYSICS_NONE,
    0x0E : PhysicsFlags.OBJ_PHYSICS_DEEP_WATER,
    0x0F : PhysicsFlags.OBJ_PHYSICS_NONE,
    0x10 : PhysicsFlags.OBJ_PHYSICS_FINE_COLLISION_SIDE_2, #| $01
    0x11 : PhysicsFlags.OBJ_PHYSICS_FINE_COLLISION_SIDE_1, #| $00
    0x12 : PhysicsFlags.OBJ_PHYSICS_FINE_COLLISION_SIDE_3, #| $02
    0x13 : PhysicsFlags.OBJ_PHYSICS_FINE_COLLISION_SIDE_4, #| $03
    0x14 : PhysicsFlags.OBJ_PHYSICS_FINE_COLLISION_CORNER_INWARD_1, #| $04
    0x15 : PhysicsFlags.OBJ_PHYSICS_FINE_COLLISION_CORNER_INWARD_2, #| $05
    0x16 : PhysicsFlags.OBJ_PHYSICS_FINE_COLLISION_CORNER_INWARD_3, #| $06
    0x17 : PhysicsFlags.OBJ_PHYSICS_FINE_COLLISION_CORNER_INWARD_4, #| $07
    0x18 : PhysicsFlags.OBJ_PHYSICS_NONE,
    0x19 : PhysicsFlags.OBJ_PHYSICS_FINE_COLLISION_MYST_1, #| $0C
    0x1A : PhysicsFlags.OBJ_PHYSICS_FINE_COLLISION_MYST_2, #| $0D
    0x1B : PhysicsFlags.OBJ_PHYSICS_SHALLOW_WATER,
    0x1C : PhysicsFlags.OBJ_PHYSICS_PIT_WARP,
    0x1D : PhysicsFlags.OBJ_PHYSICS_PIT_WARP,
    0x1E : PhysicsFlags.OBJ_PHYSICS_PIT_WARP,
    0x1F : PhysicsFlags.OBJ_PHYSICS_PIT_WARP,
    0x20 : PhysicsFlags.OBJ_PHYSICS_REMOVABLE_OBSTACLE,
    0x21 : PhysicsFlags.OBJ_PHYSICS_LEDGE_4, #| $03
    0x22 : PhysicsFlags.OBJ_PHYSICS_LEDGE_3, #| $02
    0x23 : PhysicsFlags.OBJ_PHYSICS_LEDGE_1, #| $00
    0x24 : PhysicsFlags.OBJ_PHYSICS_LEDGE_2, #| $01
    0x25 : PhysicsFlags.OBJ_PHYSICS_SOLID,
    0x26 : PhysicsFlags.OBJ_PHYSICS_SOLID,
    0x27 : PhysicsFlags.OBJ_PHYSICS_SOLID,
    0x28 : PhysicsFlags.OBJ_PHYSICS_SOLID,
    0x29 : PhysicsFlags.OBJ_PHYSICS_SOLID,
    0x2A : PhysicsFlags.OBJ_PHYSICS_SOLID,
    0x2B : PhysicsFlags.OBJ_PHYSICS_SOLID,
    0x2C : PhysicsFlags.OBJ_PHYSICS_SOLID,
    0x2D : PhysicsFlags.OBJ_PHySICS_DOOR_CLOSED_KEY_1, #| $00
    0x2E : PhysicsFlags.OBJ_PHySICS_DOOR_CLOSED_KEY_1, #| $00
    0x2F : PhysicsFlags.OBJ_PHYSICS_DOOR_CLOSED_KEY_2, #| $01
    0x30 : PhysicsFlags.OBJ_PHYSICS_DOOR_CLOSED_KEY_2, #| $01
    0x31 : PhysicsFlags.OBJ_PHYSICS_DOOR_CLOSED_KEY_3, #| $02
    0x32 : PhysicsFlags.OBJ_PHYSICS_DOOR_CLOSED_KEY_3, #| $02
    0x33 : PhysicsFlags.OBJ_PHYSICS_DOOR_CLOSED_KEY_4, #| $03
    0x34 : PhysicsFlags.OBJ_PHYSICS_DOOR_CLOSED_KEY_4, #| $03
    0x35 : PhysicsFlags.OBJ_PHYSICS_LEDGE_4, #| $03
    0x36 : PhysicsFlags.OBJ_PHYSICS_LEDGE_4, #| $03
    0x37 : PhysicsFlags.OBJ_PHYSICS_LEDGE_3, #| $02
    0x38 : PhysicsFlags.OBJ_PHYSICS_LEDGE_3, #| $02
    0x39 : PhysicsFlags.OBJ_PHYSICS_LEDGE_1, #| $00
    0x3A : PhysicsFlags.OBJ_PHYSICS_LEDGE_1, #| $00
    0x3B : PhysicsFlags.OBJ_PHYSICS_LEDGE_2, #| $01
    0x3C : PhysicsFlags.OBJ_PHYSICS_LEDGE_2, #| $01
    0x3D : PhysicsFlags.OBJ_PHYSICS_NONE,
    0x3E : PhysicsFlags.OBJ_PHYSICS_NONE,
    0x3F : PhysicsFlags.OBJ_PHYSICS_DOOR_CLOSED_BOMBABLE_1, #| $09
    0x40 : PhysicsFlags.OBJ_PHYSICS_DOOR_CLOSED_BOMBABLE_2, #| $0A
    0x41 : PhysicsFlags.OBJ_PHYSICS_DOOR_CLOSED_BOMBABLE_3, #| $0B
    0x42 : PhysicsFlags.OBJ_PHYSICS_DOOR_CLOSED_BOMBABLE_4, #| $0C
    0x43 : PhysicsFlags.OBJ_PHYSICS_DOOR_OPEN, #| $0C
    0x44 : PhysicsFlags.OBJ_PHYSICS_DOOR_OPEN, #| $0D
    0x45 : PhysicsFlags.OBJ_PHYSICS_SOLID,
    0x46 : PhysicsFlags.OBJ_PHYSICS_SOLID,
    0x47 : PhysicsFlags.OBJ_PHYSICS_DOOR_CLOSED_BOMBABLE_1, #| $09
    0x48 : PhysicsFlags.OBJ_PHYSICS_DOOR_CLOSED_BOMBABLE_2, #| $0A
    0x49 : PhysicsFlags.OBJ_PHYSICS_DOOR_CLOSED_BOMBABLE_3, #| $0B
    0x4A : PhysicsFlags.OBJ_PHYSICS_DOOR_CLOSED_BOMBABLE_4, #| $0C
    0x4B : PhysicsFlags.OBJ_PHYSICS_WATER_SIDESCROLL,
    0x4C : PhysicsFlags.OBJ_PHYSICS_NONE,
    0x4D : PhysicsFlags.OBJ_PHYSICS_NONE,
    0x4E : PhysicsFlags.OBJ_PHYSICS_HOOKSHOTABLE,
    0x4F : PhysicsFlags.OBJ_PHYSICS_HOOKSHOTABLE,
    0x50 : PhysicsFlags.OBJ_PHYSICS_SOLID,
    0x51 : PhysicsFlags.OBJ_PHYSICS_SOLID,
    0x52 : PhysicsFlags.OBJ_PHYSICS_SOLID,
    0x53 : PhysicsFlags.OBJ_PHYSICS_SOLID,
    0x54 : PhysicsFlags.OBJ_PHYSICS_SOLID,
    0x55 : PhysicsFlags.OBJ_PHYSICS_SOLID,
    0x56 : PhysicsFlags.OBJ_PHYSICS_SOLID,
    0x57 : PhysicsFlags.OBJ_PHYSICS_SOLID,
    0x58 : PhysicsFlags.OBJ_PHYSICS_SOLID,
    0x59 : PhysicsFlags.OBJ_PHYSICS_SOLID,
    0x5A : PhysicsFlags.OBJ_PHYSICS_SOLID,
    0x5B : PhysicsFlags.OBJ_PHYSICS_SOLID,
    0x5C : PhysicsFlags.OBJ_PHYSICS_SOLID,
    0x5D : PhysicsFlags.OBJ_PHYSICS_SOLID,
    0x5E : PhysicsFlags.OBJ_PHYSICS_SOLID,
    0x5F : PhysicsFlags.OBJ_PHYSICS_SOLID,
    0x60 : PhysicsFlags.OBJ_PHYSICS_SOLID,
    0x61 : PhysicsFlags.OBJ_PHYSICS_SOLID,
    0x62 : PhysicsFlags.OBJ_PHYSICS_LADDER_SIDESCROLL,
    0x63 : PhysicsFlags.OBJ_PHYSICS_LADDER_SIDESCROLL,
    0x64 : PhysicsFlags.OBJ_PHYSICS_LADDER_SIDESCROLL,
    0x65 : PhysicsFlags.OBJ_PHYSICS_LADDER_SIDESCROLL,
    0x66 : PhysicsFlags.OBJ_PHYSICS_LADDER_SIDESCROLL,
    0x67 : PhysicsFlags.OBJ_PHYSICS_WATER_SIDESCROLL,
    0x68 : PhysicsFlags.OBJ_PHYSICS_SOLID,
    0x69 : PhysicsFlags.OBJ_PHYSICS_NONE,
    0x6A : PhysicsFlags.OBJ_PHYSICS_NONE,
    0x6B : PhysicsFlags.OBJ_PHYSICS_NONE,
    0x6C : PhysicsFlags.OBJ_PHYSICS_SOLID,
    0x6D : PhysicsFlags.OBJ_PHYSICS_SOLID,
    0x6E : PhysicsFlags.OBJ_PHYSICS_NONE,
    0x6F : PhysicsFlags.OBJ_PHYSICS_NONE,
    0x70 : PhysicsFlags.OBJ_PHYSICS_NONE,
    0x71 : PhysicsFlags.OBJ_PHYSICS_NONE,
    0x72 : PhysicsFlags.OBJ_PHYSICS_WATER_SIDESCROLL,
    0x73 : PhysicsFlags.OBJ_PHYSICS_WATER_SIDESCROLL,
    0x74 : PhysicsFlags.OBJ_PHYSICS_WATER_SIDESCROLL,
    0x75 : PhysicsFlags.OBJ_PHYSICS_NONE,
    0x76 : PhysicsFlags.OBJ_PHYSICS_NONE,
    0x77 : PhysicsFlags.OBJ_PHYSICS_NONE,
    0x78 : PhysicsFlags.OBJ_PHYSICS_NONE,
    0x79 : PhysicsFlags.OBJ_PHYSICS_NONE,
    0x7A : PhysicsFlags.OBJ_PHYSICS_NONE,
    0x7B : PhysicsFlags.OBJ_PHYSICS_SOLID,
    0x7C : PhysicsFlags.OBJ_PHYSICS_NONE,
    0x7D : PhysicsFlags.OBJ_PHYSICS_WATER_SIDESCROLL,
    0x7E : PhysicsFlags.OBJ_PHYSICS_WATER_SIDESCROLL,
    0x7F : PhysicsFlags.OBJ_PHYSICS_NONE,
    0x80 : PhysicsFlags.OBJ_PHYSICS_WATER_SIDESCROLL,
    0x81 : PhysicsFlags.OBJ_PHYSICS_WATER_SIDESCROLL,
    0x82 : PhysicsFlags.OBJ_PHYSICS_NONE,
    0x83 : PhysicsFlags.OBJ_PHYSICS_WATER_SIDESCROLL,
    0x84 : PhysicsFlags.OBJ_PHYSICS_WATER_SIDESCROLL,
    0x85 : PhysicsFlags.OBJ_PHYSICS_WATER_SIDESCROLL,
    0x86 : PhysicsFlags.OBJ_PHYSICS_SOLID,
    0x87 : PhysicsFlags.OBJ_PHYSICS_SOLID,
    0x88 : PhysicsFlags.OBJ_PHYSICS_HOOKSHOTABLE,
    0x89 : PhysicsFlags.OBJ_PHYSICS_NONE,
    0x8A : PhysicsFlags.OBJ_PHYSICS_SOLID,
    0x8B : PhysicsFlags.OBJ_PHYSICS_SOLID,
    0x8C : PhysicsFlags.OBJ_PHYSICS_DOOR_OPEN, #| $0C
    0x8D : PhysicsFlags.OBJ_PHYSICS_NONE,
    0x8E : PhysicsFlags.OBJ_PHYSICS_REMOVABLE_OBSTACLE,
    0x8F : PhysicsFlags.OBJ_PHYSICS_HOOKSHOTABLE,
    0x90 : PhysicsFlags.OBJ_PHYSICS_SOLID,
    0x91 : PhysicsFlags.OBJ_PHYSICS_SOLID,
    0x92 : PhysicsFlags.OBJ_PHYSICS_NONE,
    0x93 : PhysicsFlags.OBJ_PHYSICS_FINE_COLLISION_CORNER_OUTWARD_1, #| $08
    0x94 : PhysicsFlags.OBJ_PHYSICS_FINE_COLLISION_CORNER_OUTWARD_2, #| $09
    0x95 : PhysicsFlags.OBJ_PHYSICS_FINE_COLLISION_CORNER_OUTWARD_3, #| $0A
    0x96 : PhysicsFlags.OBJ_PHYSICS_FINE_COLLISION_CORNER_OUTWARD_4, #| $0B
    0x97 : PhysicsFlags.OBJ_PHYSICS_WIDE_STAIRS,
    0x98 : PhysicsFlags.OBJ_PHYSICS_STAIRS,
    0x99 : PhysicsFlags.OBJ_PHYSICS_SOLID,
    0x9A : PhysicsFlags.OBJ_PHYSICS_DOOR_OPEN, #| $0E
    0x9B : PhysicsFlags.OBJ_PHYSICS_SOLID,
    0x9C : PhysicsFlags.OBJ_PHYSICS_SOLID,
    0x9D : PhysicsFlags.OBJ_PHYSICS_NONE,
    0x9E : PhysicsFlags.OBJ_PHYSICS_NONE,
    0x9F : PhysicsFlags.OBJ_PHYSICS_NONE,
    0xA0 : PhysicsFlags.OBJ_PHYSICS_HOOKSHOTABLE,
    0xA1 : PhysicsFlags.OBJ_PHYSICS_HOOKSHOTABLE,
    0xA2 : PhysicsFlags.OBJ_PHYSICS_DOOR,
    0xA3 : PhysicsFlags.OBJ_PHYSICS_DOOR,
    0xA4 : PhysicsFlags.OBJ_PHYSICS_DOOR_CLOSED_BOSS_DOOR, #| $08
    0xA5 : PhysicsFlags.OBJ_PHYSICS_DOOR_CLOSED_BOSS_DOOR, #| $08
    0xA6 : PhysicsFlags.OBJ_PHYSICS_HOOKSHOTABLE,
    0xA7 : PhysicsFlags.OBJ_PHYSICS_HOOKSHOTABLE,
    0xA8 : PhysicsFlags.OBJ_PHYSICS_DOOR,
    0xA9 : PhysicsFlags.OBJ_PHYSICS_REMOVABLE_OBSTACLE,
    0xAA : PhysicsFlags.OBJ_PHYSICS_NONE,
    0xAB : PhysicsFlags.OBJ_PHYSICS_SOLID,
    0xAC : PhysicsFlags.OBJ_PHYSICS_SOLID,
    0xAD : PhysicsFlags.OBJ_PHYSICS_SOLID,
    0xAE : PhysicsFlags.OBJ_PHYSICS_PIT,
    0xAF : PhysicsFlags.OBJ_PHYSICS_PIT,
    0xB0 : PhysicsFlags.OBJ_PHYSICS_PIT,
    0xB1 : PhysicsFlags.OBJ_PHYSICS_DOOR_OPEN, #| $0C
    0xB2 : PhysicsFlags.OBJ_PHYSICS_DOOR_OPEN, #| $0D
    0xB3 : PhysicsFlags.OBJ_PHYSICS_NONE,
    0xB4 : PhysicsFlags.OBJ_PHYSICS_NONE,
    0xB5 : PhysicsFlags.OBJ_PHYSICS_NONE,
    0xB6 : PhysicsFlags.OBJ_PHYSICS_FINE_COLLISION_CORNER_OUTWARD_1, #| $0B
    0xB7 : PhysicsFlags.OBJ_PHYSICS_FINE_COLLISION_CORNER_OUTWARD_2, #| $0A
    0xB8 : PhysicsFlags.OBJ_PHYSICS_FINE_COLLISION_CORNER_OUTWARD_3, #| $0B
    0xB9 : PhysicsFlags.OBJ_PHYSICS_FINE_COLLISION_CORNER_OUTWARD_4, #| $0A
    0xBA : PhysicsFlags.OBJ_PHYSICS_SOLID,
    0xBB : PhysicsFlags.OBJ_PHYSICS_DOOR_OPEN, #| $0C
    0xBC : PhysicsFlags.OBJ_PHYSICS_DOOR_OPEN, #| $0D
    0xBD : PhysicsFlags.OBJ_PHYSICS_SOLID,
    0xBE : PhysicsFlags.OBJ_PHYSICS_NONE,
    0xBF : PhysicsFlags.OBJ_PHYSICS_NONE,
    0xC0 : PhysicsFlags.OBJ_PHYSICS_SOLID,
    0xC1 : PhysicsFlags.OBJ_PHYSICS_DOOR_OPEN, #| $0C
    0xC2 : PhysicsFlags.OBJ_PHYSICS_DOOR_OPEN, #| $0D
    0xC3 : PhysicsFlags.OBJ_PHYSICS_SOLID,
    0xC4 : PhysicsFlags.OBJ_PHYSICS_SOLID,
    0xC5 : PhysicsFlags.OBJ_PHYSICS_SOLID,
    0xC6 : PhysicsFlags.OBJ_PHYSICS_SOLID,
    0xC7 : PhysicsFlags.OBJ_PHYSICS_LEDGE_4, #| $03
    0xC8 : PhysicsFlags.OBJ_PHYSICS_LEDGE_3, #| $02
    0xC9 : PhysicsFlags.OBJ_PHYSICS_LEDGE_1, #| $00
    0xCA : PhysicsFlags.OBJ_PHYSICS_LEDGE_2, #| $01
    0xCB : PhysicsFlags.OBJ_PHYSICS_BRIDGE,
    0xCC : PhysicsFlags.OBJ_PHYSICS_STAIRS_DOWN,
    0xCD : PhysicsFlags.OBJ_PHYSICS_DOOR_OPEN, #| $0E #TODO
    0xCE : PhysicsFlags.OBJ_PHYSICS_SOLID,
    0xCF : PhysicsFlags.OBJ_PHYSICS_CONVEYOR_SIDE_1, #| $00
    0xD0 : PhysicsFlags.OBJ_PHYSICS_CONVEYOR_SIDE_2, #| $01
    0xD1 : PhysicsFlags.OBJ_PHYSICS_CONVEYOR_SIDE_3, #| $02
    0xD2 : PhysicsFlags.OBJ_PHYSICS_CONVEYOR_SIDE_4, #| $03
    0xD3 : PhysicsFlags.OBJ_PHYSICS_DOOR_OPEN, #| $0F
    0xD4 : PhysicsFlags.OBJ_PHYSICS_SPIKES,
    0xD5 : PhysicsFlags.OBJ_PHYSICS_SOLID,
    0xD6 : PhysicsFlags.OBJ_PHYSICS_SOLID,
    0xD7 : PhysicsFlags.OBJ_PHYSICS_SOLID,
    0xD8 : PhysicsFlags.OBJ_PHYSICS_SOLID,
    0xD9 : PhysicsFlags.OBJ_PHYSICS_HOOKSHOTABLE,
    0xDA : PhysicsFlags.OBJ_PHYSICS_NONE,
    0xDB : PhysicsFlags.OBJ_PHYSICS_OCEAN,
    0xDC : PhysicsFlags.OBJ_PHYSICS_OCEAN,
    0xDD : PhysicsFlags.OBJ_PHYSICS_REMOVABLE_OBSTACLE,
    0xDE : PhysicsFlags.OBJ_PHYSICS_SOLID,
    0xDF : PhysicsFlags.OBJ_PHYSICS_NONE,
    0xE0 : PhysicsFlags.OBJ_PHYSICS_NONE,
    0xE1 : PhysicsFlags.OBJ_PHYSICS_NONE,
    0xE2 : PhysicsFlags.OBJ_PHYSICS_NONE,
    0xE3 : PhysicsFlags.OBJ_PHYSICS_NONE,
    0xE4 : PhysicsFlags.OBJ_PHYSICS_NONE,
    0xE5 : PhysicsFlags.OBJ_PHYSICS_NONE,
    0xE6 : PhysicsFlags.OBJ_PHYSICS_NONE,
    0xE7 : PhysicsFlags.OBJ_PHYSICS_NONE,
    0xE8 : PhysicsFlags.OBJ_PHYSICS_NONE,
    0xE9 : PhysicsFlags.OBJ_PHYSICS_NONE,
    0xEA : PhysicsFlags.OBJ_PHYSICS_NONE,
    0xEB : PhysicsFlags.OBJ_PHYSICS_SOLID,
    0xEC : PhysicsFlags.OBJ_PHYSICS_SOLID,
    0xED : PhysicsFlags.OBJ_PHYSICS_SOLID,
    0xEE : PhysicsFlags.OBJ_PHYSICS_SOLID,
    0xEF : PhysicsFlags.OBJ_PHYSICS_SOLID,
    0xF0 : PhysicsFlags.OBJ_PHYSICS_SOLID,
    0xF1 : PhysicsFlags.OBJ_PHYSICS_SOLID,
    0xF2 : PhysicsFlags.OBJ_PHYSICS_SOLID,
    0xF3 : PhysicsFlags.OBJ_PHYSICS_SOLID,
    0xF4 : PhysicsFlags.OBJ_PHYSICS_SOLID,
    0xF5 : PhysicsFlags.OBJ_PHYSICS_SOLID,
    0xF6 : PhysicsFlags.OBJ_PHYSICS_SOLID,
    0xF7 : PhysicsFlags.OBJ_PHYSICS_SOLID,
    0xF8 : PhysicsFlags.OBJ_PHYSICS_SOLID,
    0xF9 : PhysicsFlags.OBJ_PHYSICS_SOLID,
    0xFA : PhysicsFlags.OBJ_PHYSICS_SOLID,
    0xFB : PhysicsFlags.OBJ_PHYSICS_SOLID,
    0xFC : PhysicsFlags.OBJ_PHYSICS_SOLID,
    0xFD : PhysicsFlags.OBJ_PHYSICS_SOLID,
    0xFE : PhysicsFlags.OBJ_PHYSICS_UNUSED,
    0xFF : PhysicsFlags.OBJ_PHYSICS_INVALID,

}

INDOOR2_OBJECTS_PHYSICS = {

    0x00 : PhysicsFlags.OBJ_PHYSICS_NONE,
    0x01 : PhysicsFlags.OBJ_PHYSICS_PIT,
    0x02 : PhysicsFlags.OBJ_PHYSICS_NONE,
    0x03 : PhysicsFlags.OBJ_PHYSICS_NONE,
    0x04 : PhysicsFlags.OBJ_PHYSICS_NONE,
    0x05 : PhysicsFlags.OBJ_PHYSICS_NONE,
    0x06 : PhysicsFlags.OBJ_PHYSICS_LAVA,
    0x07 : PhysicsFlags.OBJ_PHYSICS_NONE,
    0x08 : PhysicsFlags.OBJ_PHYSICS_DOOR_OPEN, #| $0D
    0x09 : PhysicsFlags.OBJ_PHYSICS_DOOR_OPEN, #| $0E
    0x0A : PhysicsFlags.OBJ_PHYSICS_DOOR_OPEN, #| $0F
    0x0B : PhysicsFlags.OBJ_PHYSICS_DOOR_OPEN, #| $0E
    0x0C : PhysicsFlags.OBJ_PHYSICS_DOOR_OPEN, #| $0F
    0x0D : PhysicsFlags.OBJ_PHYSICS_NONE,
    0x0E : PhysicsFlags.OBJ_PHYSICS_DEEP_WATER,
    0x0F : PhysicsFlags.OBJ_PHYSICS_NONE,
    0x10 : PhysicsFlags.OBJ_PHYSICS_FINE_COLLISION_SIDE_2, #| $01
    0x11 : PhysicsFlags.OBJ_PHYSICS_FINE_COLLISION_SIDE_1, #| $00
    0x12 : PhysicsFlags.OBJ_PHYSICS_FINE_COLLISION_SIDE_3, #| $02
    0x13 : PhysicsFlags.OBJ_PHYSICS_FINE_COLLISION_SIDE_4, #| $03
    0x14 : PhysicsFlags.OBJ_PHYSICS_FINE_COLLISION_CORNER_INWARD_1, #| $04
    0x15 : PhysicsFlags.OBJ_PHYSICS_FINE_COLLISION_CORNER_INWARD_2, #| $05
    0x16 : PhysicsFlags.OBJ_PHYSICS_FINE_COLLISION_CORNER_INWARD_3, #| $06
    0x17 : PhysicsFlags.OBJ_PHYSICS_FINE_COLLISION_CORNER_INWARD_4, #| $07
    0x18 : PhysicsFlags.OBJ_PHYSICS_NONE,
    0x19 : PhysicsFlags.OBJ_PHYSICS_FINE_COLLISION_MYST_1, #| $0C
    0x1A : PhysicsFlags.OBJ_PHYSICS_FINE_COLLISION_MYST_2, #| $0D
    0x1B : PhysicsFlags.OBJ_PHYSICS_SHALLOW_WATER,
    0x1C : PhysicsFlags.OBJ_PHYSICS_PIT_WARP,
    0x1D : PhysicsFlags.OBJ_PHYSICS_PIT_WARP,
    0x1E : PhysicsFlags.OBJ_PHYSICS_PIT_WARP,
    0x1F : PhysicsFlags.OBJ_PHYSICS_PIT_WARP,
    0x20 : PhysicsFlags.OBJ_PHYSICS_REMOVABLE_OBSTACLE,
    0x21 : PhysicsFlags.OBJ_PHYSICS_LEDGE_4, #| $03
    0x22 : PhysicsFlags.OBJ_PHYSICS_LEDGE_3, #| $02
    0x23 : PhysicsFlags.OBJ_PHYSICS_LEDGE_1, #| $00
    0x24 : PhysicsFlags.OBJ_PHYSICS_LEDGE_2, #| $01
    0x25 : PhysicsFlags.OBJ_PHYSICS_SOLID,
    0x26 : PhysicsFlags.OBJ_PHYSICS_SOLID,
    0x27 : PhysicsFlags.OBJ_PHYSICS_SOLID,
    0x28 : PhysicsFlags.OBJ_PHYSICS_SOLID,
    0x29 : PhysicsFlags.OBJ_PHYSICS_SOLID,
    0x2A : PhysicsFlags.OBJ_PHYSICS_SOLID,
    0x2B : PhysicsFlags.OBJ_PHYSICS_SOLID,
    0x2C : PhysicsFlags.OBJ_PHYSICS_SOLID,
    0x2D : PhysicsFlags.OBJ_PHySICS_DOOR_CLOSED_KEY_1, #| $00
    0x2E : PhysicsFlags.OBJ_PHySICS_DOOR_CLOSED_KEY_1, #| $00
    0x2F : PhysicsFlags.OBJ_PHYSICS_DOOR_CLOSED_KEY_2, #| $01
    0x30 : PhysicsFlags.OBJ_PHYSICS_DOOR_CLOSED_KEY_2, #| $01
    0x31 : PhysicsFlags.OBJ_PHYSICS_DOOR_CLOSED_KEY_3, #| $02
    0x32 : PhysicsFlags.OBJ_PHYSICS_DOOR_CLOSED_KEY_3, #| $02
    0x33 : PhysicsFlags.OBJ_PHYSICS_DOOR_CLOSED_KEY_4, #| $03
    0x34 : PhysicsFlags.OBJ_PHYSICS_DOOR_CLOSED_KEY_4, #| $03
    0x35 : PhysicsFlags.OBJ_PHYSICS_LEDGE_4, #| $03
    0x36 : PhysicsFlags.OBJ_PHYSICS_LEDGE_4, #| $03
    0x37 : PhysicsFlags.OBJ_PHYSICS_LEDGE_3, #| $02
    0x38 : PhysicsFlags.OBJ_PHYSICS_LEDGE_3, #| $02
    0x39 : PhysicsFlags.OBJ_PHYSICS_LEDGE_1, #| $00
    0x3A : PhysicsFlags.OBJ_PHYSICS_LEDGE_1, #| $00
    0x3B : PhysicsFlags.OBJ_PHYSICS_LEDGE_2, #| $01
    0x3C : PhysicsFlags.OBJ_PHYSICS_LEDGE_2, #| $01
    0x3D : PhysicsFlags.OBJ_PHYSICS_NONE,
    0x3E : PhysicsFlags.OBJ_PHYSICS_NONE,
    0x3F : PhysicsFlags.OBJ_PHYSICS_DOOR_CLOSED_BOMBABLE_1, #| $09
    0x40 : PhysicsFlags.OBJ_PHYSICS_DOOR_CLOSED_BOMBABLE_2, #| $0A
    0x41 : PhysicsFlags.OBJ_PHYSICS_DOOR_CLOSED_BOMBABLE_3, #| $0B
    0x42 : PhysicsFlags.OBJ_PHYSICS_DOOR_CLOSED_BOMBABLE_4, #| $0C
    0x43 : PhysicsFlags.OBJ_PHYSICS_DOOR_OPEN, #| $0C
    0x44 : PhysicsFlags.OBJ_PHYSICS_DOOR_OPEN, #| $0D
    0x45 : PhysicsFlags.OBJ_PHYSICS_SOLID,
    0x46 : PhysicsFlags.OBJ_PHYSICS_SOLID,
    0x47 : PhysicsFlags.OBJ_PHYSICS_DOOR_CLOSED_BOMBABLE_1, #| $09
    0x48 : PhysicsFlags.OBJ_PHYSICS_DOOR_CLOSED_BOMBABLE_2, #| $0A
    0x49 : PhysicsFlags.OBJ_PHYSICS_DOOR_CLOSED_BOMBABLE_3, #| $0B
    0x4A : PhysicsFlags.OBJ_PHYSICS_DOOR_CLOSED_BOMBABLE_4, #| $0C
    0x4B : PhysicsFlags.OBJ_PHYSICS_WATER_SIDESCROLL,
    0x4C : PhysicsFlags.OBJ_PHYSICS_NONE,
    0x4D : PhysicsFlags.OBJ_PHYSICS_NONE,
    0x4E : PhysicsFlags.OBJ_PHYSICS_HOOKSHOTABLE,
    0x4F : PhysicsFlags.OBJ_PHYSICS_HOOKSHOTABLE,
    0x50 : PhysicsFlags.OBJ_PHYSICS_NONE,
    0x51 : PhysicsFlags.OBJ_PHYSICS_NONE,
    0x52 : PhysicsFlags.OBJ_PHYSICS_NONE,
    0x53 : PhysicsFlags.OBJ_PHYSICS_NONE,
    0x54 : PhysicsFlags.OBJ_PHYSICS_NONE,
    0x55 : PhysicsFlags.OBJ_PHYSICS_NONE,
    0x56 : PhysicsFlags.OBJ_PHYSICS_NONE,
    0x57 : PhysicsFlags.OBJ_PHYSICS_NONE,
    0x58 : PhysicsFlags.OBJ_PHYSICS_NONE,
    0x59 : PhysicsFlags.OBJ_PHYSICS_NONE,
    0x5A : PhysicsFlags.OBJ_PHYSICS_PIT,
    0x5B : PhysicsFlags.OBJ_PHYSICS_NONE,
    0x5C : PhysicsFlags.OBJ_PHYSICS_NONE,
    0x5D : PhysicsFlags.OBJ_PHYSICS_NONE,
    0x5E : PhysicsFlags.OBJ_PHYSICS_NONE,
    0x5F : PhysicsFlags.OBJ_PHYSICS_PIT,
    0x60 : PhysicsFlags.OBJ_PHYSICS_NONE,
    0x61 : PhysicsFlags.OBJ_PHYSICS_NONE,
    0x62 : PhysicsFlags.OBJ_PHYSICS_NONE,
    0x63 : PhysicsFlags.OBJ_PHYSICS_NONE,
    0x64 : PhysicsFlags.OBJ_PHYSICS_PIT,
    0x65 : PhysicsFlags.OBJ_PHYSICS_NONE,
    0x66 : PhysicsFlags.OBJ_PHYSICS_NONE,
    0x67 : PhysicsFlags.OBJ_PHYSICS_NONE,
    0x68 : PhysicsFlags.OBJ_PHYSICS_NONE,
    0x69 : PhysicsFlags.OBJ_PHYSICS_NONE,
    0x6A : PhysicsFlags.OBJ_PHYSICS_NONE,
    0x6B : PhysicsFlags.OBJ_PHYSICS_NONE,
    0x6C : PhysicsFlags.OBJ_PHYSICS_NONE,
    0x6D : PhysicsFlags.OBJ_PHYSICS_NONE,
    0x6E : PhysicsFlags.OBJ_PHYSICS_NONE,
    0x6F : PhysicsFlags.OBJ_PHYSICS_NONE,
    0x70 : PhysicsFlags.OBJ_PHYSICS_NONE,
    0x71 : PhysicsFlags.OBJ_PHYSICS_NONE,
    0x72 : PhysicsFlags.OBJ_PHYSICS_WATER_SIDESCROLL,
    0x73 : PhysicsFlags.OBJ_PHYSICS_WATER_SIDESCROLL,
    0x74 : PhysicsFlags.OBJ_PHYSICS_WATER_SIDESCROLL,
    0x75 : PhysicsFlags.OBJ_PHYSICS_NONE,
    0x76 : PhysicsFlags.OBJ_PHYSICS_NONE,
    0x77 : PhysicsFlags.OBJ_PHYSICS_NONE,
    0x78 : PhysicsFlags.OBJ_PHYSICS_NONE,
    0x79 : PhysicsFlags.OBJ_PHYSICS_NONE,
    0x7A : PhysicsFlags.OBJ_PHYSICS_NONE,
    0x7B : PhysicsFlags.OBJ_PHYSICS_SOLID,
    0x7C : PhysicsFlags.OBJ_PHYSICS_NONE,
    0x7D : PhysicsFlags.OBJ_PHYSICS_WATER_SIDESCROLL,
    0x7E : PhysicsFlags.OBJ_PHYSICS_WATER_SIDESCROLL,
    0x7F : PhysicsFlags.OBJ_PHYSICS_NONE,
    0x80 : PhysicsFlags.OBJ_PHYSICS_WATER_SIDESCROLL,
    0x81 : PhysicsFlags.OBJ_PHYSICS_WATER_SIDESCROLL,
    0x82 : PhysicsFlags.OBJ_PHYSICS_NONE,
    0x83 : PhysicsFlags.OBJ_PHYSICS_WATER_SIDESCROLL,
    0x84 : PhysicsFlags.OBJ_PHYSICS_WATER_SIDESCROLL,
    0x85 : PhysicsFlags.OBJ_PHYSICS_WATER_SIDESCROLL,
    0x86 : PhysicsFlags.OBJ_PHYSICS_SOLID,
    0x87 : PhysicsFlags.OBJ_PHYSICS_SOLID,
    0x88 : PhysicsFlags.OBJ_PHYSICS_HOOKSHOTABLE,
    0x89 : PhysicsFlags.OBJ_PHYSICS_NONE,
    0x8A : PhysicsFlags.OBJ_PHYSICS_SOLID,
    0x8B : PhysicsFlags.OBJ_PHYSICS_SOLID,
    0x8C : PhysicsFlags.OBJ_PHYSICS_DOOR_OPEN, #| $0C
    0x8D : PhysicsFlags.OBJ_PHYSICS_NONE,
    0x8E : PhysicsFlags.OBJ_PHYSICS_REMOVABLE_OBSTACLE,
    0x8F : PhysicsFlags.OBJ_PHYSICS_HOOKSHOTABLE,
    0x90 : PhysicsFlags.OBJ_PHYSICS_SOLID,
    0x91 : PhysicsFlags.OBJ_PHYSICS_SOLID,
    0x92 : PhysicsFlags.OBJ_PHYSICS_NONE,
    0x93 : PhysicsFlags.OBJ_PHYSICS_FINE_COLLISION_CORNER_OUTWARD_1, #| $08
    0x94 : PhysicsFlags.OBJ_PHYSICS_FINE_COLLISION_CORNER_OUTWARD_2, #| $09
    0x95 : PhysicsFlags.OBJ_PHYSICS_FINE_COLLISION_CORNER_OUTWARD_3, #| $0A
    0x96 : PhysicsFlags.OBJ_PHYSICS_FINE_COLLISION_CORNER_OUTWARD_4, #| $0B
    0x97 : PhysicsFlags.OBJ_PHYSICS_WIDE_STAIRS,
    0x98 : PhysicsFlags.OBJ_PHYSICS_STAIRS,
    0x99 : PhysicsFlags.OBJ_PHYSICS_SOLID,
    0x9A : PhysicsFlags.OBJ_PHYSICS_DOOR_OPEN, #| $0E
    0x9B : PhysicsFlags.OBJ_PHYSICS_SOLID,
    0x9C : PhysicsFlags.OBJ_PHYSICS_SOLID,
    0x9D : PhysicsFlags.OBJ_PHYSICS_NONE,
    0x9E : PhysicsFlags.OBJ_PHYSICS_NONE,
    0x9F : PhysicsFlags.OBJ_PHYSICS_NONE,
    0xA0 : PhysicsFlags.OBJ_PHYSICS_HOOKSHOTABLE,
    0xA1 : PhysicsFlags.OBJ_PHYSICS_HOOKSHOTABLE,
    0xA2 : PhysicsFlags.OBJ_PHYSICS_DOOR,
    0xA3 : PhysicsFlags.OBJ_PHYSICS_DOOR,
    0xA4 : PhysicsFlags.OBJ_PHYSICS_DOOR_CLOSED_BOSS_DOOR, #| $08
    0xA5 : PhysicsFlags.OBJ_PHYSICS_DOOR_CLOSED_BOSS_DOOR, #| $08
    0xA6 : PhysicsFlags.OBJ_PHYSICS_HOOKSHOTABLE,
    0xA7 : PhysicsFlags.OBJ_PHYSICS_HOOKSHOTABLE,
    0xA8 : PhysicsFlags.OBJ_PHYSICS_DOOR,
    0xA9 : PhysicsFlags.OBJ_PHYSICS_REMOVABLE_OBSTACLE,
    0xAA : PhysicsFlags.OBJ_PHYSICS_NONE,
    0xAB : PhysicsFlags.OBJ_PHYSICS_SOLID,
    0xAC : PhysicsFlags.OBJ_PHYSICS_SOLID,
    0xAD : PhysicsFlags.OBJ_PHYSICS_SOLID,
    0xAE : PhysicsFlags.OBJ_PHYSICS_PIT,
    0xAF : PhysicsFlags.OBJ_PHYSICS_PIT,
    0xB0 : PhysicsFlags.OBJ_PHYSICS_PIT,
    0xB1 : PhysicsFlags.OBJ_PHYSICS_DOOR_OPEN, #| $0C
    0xB2 : PhysicsFlags.OBJ_PHYSICS_DOOR_OPEN, #| $0D
    0xB3 : PhysicsFlags.OBJ_PHYSICS_NONE,
    0xB4 : PhysicsFlags.OBJ_PHYSICS_NONE,
    0xB5 : PhysicsFlags.OBJ_PHYSICS_NONE,
    0xB6 : PhysicsFlags.OBJ_PHYSICS_FINE_COLLISION_CORNER_OUTWARD_1, #| $0B
    0xB7 : PhysicsFlags.OBJ_PHYSICS_FINE_COLLISION_CORNER_OUTWARD_2, #| $0A
    0xB8 : PhysicsFlags.OBJ_PHYSICS_FINE_COLLISION_CORNER_OUTWARD_3, #| $0B
    0xB9 : PhysicsFlags.OBJ_PHYSICS_FINE_COLLISION_CORNER_OUTWARD_4, #| $0A
    0xBA : PhysicsFlags.OBJ_PHYSICS_SOLID,
    0xBB : PhysicsFlags.OBJ_PHYSICS_DOOR_OPEN, #| $0C
    0xBC : PhysicsFlags.OBJ_PHYSICS_DOOR_OPEN, #| $0D
    0xBD : PhysicsFlags.OBJ_PHYSICS_SOLID,
    0xBE : PhysicsFlags.OBJ_PHYSICS_NONE,
    0xBF : PhysicsFlags.OBJ_PHYSICS_NONE,
    0xC0 : PhysicsFlags.OBJ_PHYSICS_SOLID,
    0xC1 : PhysicsFlags.OBJ_PHYSICS_DOOR_OPEN, #| $0C
    0xC2 : PhysicsFlags.OBJ_PHYSICS_DOOR_OPEN, #| $0D
    0xC3 : PhysicsFlags.OBJ_PHYSICS_SOLID,
    0xC4 : PhysicsFlags.OBJ_PHYSICS_SOLID,
    0xC5 : PhysicsFlags.OBJ_PHYSICS_SOLID,
    0xC6 : PhysicsFlags.OBJ_PHYSICS_SOLID,
    0xC7 : PhysicsFlags.OBJ_PHYSICS_LEDGE_4, #| $03
    0xC8 : PhysicsFlags.OBJ_PHYSICS_LEDGE_3, #| $02
    0xC9 : PhysicsFlags.OBJ_PHYSICS_LEDGE_1, #| $00
    0xCA : PhysicsFlags.OBJ_PHYSICS_LEDGE_2, #| $01
    0xCB : PhysicsFlags.OBJ_PHYSICS_BRIDGE,
    0xCC : PhysicsFlags.OBJ_PHYSICS_STAIRS_DOWN,
    0xCD : PhysicsFlags.OBJ_PHYSICS_DOOR_OPEN, #| $0E #TODO
    0xCE : PhysicsFlags.OBJ_PHYSICS_SOLID,
    0xCF : PhysicsFlags.OBJ_PHYSICS_CONVEYOR_SIDE_1, #| $00
    0xD0 : PhysicsFlags.OBJ_PHYSICS_CONVEYOR_SIDE_2, #| $01
    0xD1 : PhysicsFlags.OBJ_PHYSICS_CONVEYOR_SIDE_3, #| $02
    0xD2 : PhysicsFlags.OBJ_PHYSICS_CONVEYOR_SIDE_4, #| $03
    0xD3 : PhysicsFlags.OBJ_PHYSICS_DOOR_OPEN, #| $0F
    0xD4 : PhysicsFlags.OBJ_PHYSICS_SPIKES,
    0xD5 : PhysicsFlags.OBJ_PHYSICS_SOLID,
    0xD6 : PhysicsFlags.OBJ_PHYSICS_SOLID,
    0xD7 : PhysicsFlags.OBJ_PHYSICS_SOLID,
    0xD8 : PhysicsFlags.OBJ_PHYSICS_SOLID,
    0xD9 : PhysicsFlags.OBJ_PHYSICS_HOOKSHOTABLE,
    0xDA : PhysicsFlags.OBJ_PHYSICS_NONE,
    0xDB : PhysicsFlags.OBJ_PHYSICS_OCEAN,
    0xDC : PhysicsFlags.OBJ_PHYSICS_OCEAN,
    0xDD : PhysicsFlags.OBJ_PHYSICS_REMOVABLE_OBSTACLE,
    0xDE : PhysicsFlags.OBJ_PHYSICS_SOLID,
    0xDF : PhysicsFlags.OBJ_PHYSICS_NONE,
    0xE0 : PhysicsFlags.OBJ_PHYSICS_NONE,
    0xE1 : PhysicsFlags.OBJ_PHYSICS_NONE,
    0xE2 : PhysicsFlags.OBJ_PHYSICS_NONE,
    0xE3 : PhysicsFlags.OBJ_PHYSICS_NONE,
    0xE4 : PhysicsFlags.OBJ_PHYSICS_NONE,
    0xE5 : PhysicsFlags.OBJ_PHYSICS_NONE,
    0xE6 : PhysicsFlags.OBJ_PHYSICS_NONE,
    0xE7 : PhysicsFlags.OBJ_PHYSICS_NONE,
    0xE8 : PhysicsFlags.OBJ_PHYSICS_NONE,
    0xE9 : PhysicsFlags.OBJ_PHYSICS_NONE,
    0xEA : PhysicsFlags.OBJ_PHYSICS_NONE,
    0xEB : PhysicsFlags.OBJ_PHYSICS_SOLID,
    0xEC : PhysicsFlags.OBJ_PHYSICS_SOLID,
    0xED : PhysicsFlags.OBJ_PHYSICS_SOLID,
    0xEE : PhysicsFlags.OBJ_PHYSICS_SOLID,
    0xEF : PhysicsFlags.OBJ_PHYSICS_SOLID,
    0xF0 : PhysicsFlags.OBJ_PHYSICS_SOLID,
    0xF1 : PhysicsFlags.OBJ_PHYSICS_SOLID,
    0xF2 : PhysicsFlags.OBJ_PHYSICS_SOLID,
    0xF3 : PhysicsFlags.OBJ_PHYSICS_SOLID,
    0xF4 : PhysicsFlags.OBJ_PHYSICS_SOLID,
    0xF5 : PhysicsFlags.OBJ_PHYSICS_SOLID,
    0xF6 : PhysicsFlags.OBJ_PHYSICS_SOLID,
    0xF7 : PhysicsFlags.OBJ_PHYSICS_SOLID,
    0xF8 : PhysicsFlags.OBJ_PHYSICS_SOLID,
    0xF9 : PhysicsFlags.OBJ_PHYSICS_SOLID,
    0xFA : PhysicsFlags.OBJ_PHYSICS_SOLID,
    0xFB : PhysicsFlags.OBJ_PHYSICS_SOLID,
    0xFC : PhysicsFlags.OBJ_PHYSICS_SOLID,
    0xFD : PhysicsFlags.OBJ_PHYSICS_SOLID,
    0xFE : PhysicsFlags.OBJ_PHYSICS_UNUSED,
    0xFF : PhysicsFlags.OBJ_PHYSICS_INVALID,
}



