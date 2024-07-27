
from gym_env.const.maps import MapLevel, Map
MapLookup = {
    # Key being (overworld_type.value, room_id) = (x, y, level)
    MapLevel.TAIL_CAVE: {},
    MapLevel.BOTTLE_GROTTO: {},
    MapLevel.KEY_CAVERN: {},
    MapLevel.ANGLERS_TUNNEL: {},
    MapLevel.CATFISHS_MAW: {},
    MapLevel.FACE_SHRINE: {},
    MapLevel.EAGLES_TOWER: {},
    MapLevel.EAGLES_TOWER_ALT: {},
    MapLevel.TURTLE_ROCK: {},
    MapLevel.WINDFISHS_EGG: {},
    MapLevel.COLOR_DUNGEON: {},
    MapLevel.CAVES_HOUSES: {},
}

Tail_Cave_Layout = [
(1,None),(1,None),(1,None),(1,None),(1,None),(1,0x18),(1,0x19),(1,None),
(1,None),(1,None),(1,None),(1,None),(1,None),(1,0x1a),(1,0x1b),(1,None),
(1,None),(1,None),(1,None),(1,None),(1,None),(1,None),(1,0x02),(1,None),
(1,None),(1,0x03),(1,0x04),(1,0x05),(1,None),(1,None),(1,0x06),(1,None),
(1,0x1d),(1,None),(1,0x07),(1,0x08),(1,0x09),(1,0x0a),(1,0x0b),(1,None),
(1,0x1c),(1,0x0c),(1,0x0d),(1,0x0e),(1,0x0f),(1,0x10),(1,0x11),(1,None),
(1,0x01),(1,None),(1,0x12),(1,0x13),(1,0x14),(1,None),(1,None),(1,None),
(1,None),(1,0x15),(1,0x16),(1,0x17),(1,None),(1,None),(1,None),(1,None),
]

Bottle_Grotto_Layout = [
(1,None),(1,None),(1,None),(1,None),(1,None),(1,None),(1,None),(1,None),
(1,None),(1,0x20),(1,0x21),(1,0x22),(1,0x23),(1,0x24),(1,0x25),(1,None),
(1,None),(1,None),(1,0x26),(1,None),(1,None),(1,0x27),(1,None),(1,None),
(1,None),(1,0x28),(1,0x29),(1,0x3a),(1,0x3b),(1,0x2a),(1,0x2b),(1,None),
(1,None),(1,0x2c),(1,None),(1,0x3c),(1,0x3d),(1,None),(1,0x2d),(1,None),
(1,None),(1,0x2e),(1,None),(1,0x3e),(1,0x3f),(1,None),(1,0x2f),(1,None),
(1,None),(1,0x30),(1,0x31),(1,0x32),(1,0x33),(1,0x34),(1,0x35),(1,None),
(1,None),(1,None),(1,0x36),(1,0x37),(1,0x38),(1,0x39),(1,None),(1,None),
]

Key_Cavern_Layout = [
(1,0x40),(1,0x41),(1,0x42),(1,0x43),(1,None),(1,0xaa),(1,0xab),(1,None),
(1,0x44),(1,0x45),(1,0x46),(1,0x47),(1,None),(1,None),(1,None),(1,None),
(1,0x48),(1,0x49),(1,0x4a),(1,0x4b),(1,None),(1,None),(1,0x54),(1,None),
(1,None),(1,0x4c),(1,0x4d),(1,None),(1,None),(1,0x55),(1,0x56),(1,0x57),
(1,None),(1,0x4e),(1,None),(1,None),(1,None),(1,None),(1,0x58),(1,None),
(1,None),(1,0x4f),(1,0x50),(1,None),(1,None),(1,None),(1,0x59),(1,None),
(1,None),(1,0x51),(1,None),(1,None),(1,None),(1,None),(1,0x5a),(1,None),
(1,None),(1,0x52),(1,0x53),(1,None),(1,None),(1,None),(1,0x5b),(1,0x5c),
]

Anglers_Tunnel_Layout = [
(1,None),(1,None),(1,None),(1,None),(1,None),(1,None),(1,None),(1,None),
(1,None),(1,None),(1,None),(1,0x60),(1,0x61),(1,None),(1,None),(1,None),
(1,None),(1,0x62),(1,None),(1,0x63),(1,0x64),(1,None),(1,0x65),(1,None),
(1,0xef),(1,0x66),(1,0x67),(1,0x68),(1,0x69),(1,0x6a),(1,0x6b),(1,None),
(1,0xff),(1,0x6c),(1,0x6d),(1,0x6e),(1,0x6f),(1,0x70),(1,0x71),(1,None),
(1,0x7c),(1,0x7d),(1,0x72),(1,0x73),(1,0x74),(1,0x75),(1,None),(1,None),
(1,0x1e),(1,0x1f),(1,0x76),(1,0x77),(1,0x78),(1,0x79),(1,None),(1,None),
(1,0x5e),(1,0x5f),(1,None),(1,0x7a),(1,0x7b),(1,None),(1,None),(1,None),
]

Catfishs_Maw_Layout = [
(1,None),(1,0x80),(1,0x81),(1,0x82),(1,0x83),(1,0x84),(1,None),(1,None),
(1,None),(1,None),(1,None),(1,0x85),(1,0x86),(1,0x87),(1,0x88),(1,None),
(1,None),(1,0x89),(1,0x8a),(1,0x8b),(1,0x8c),(1,0x8d),(1,0x8e),(1,0x8f),
(1,None),(1,None),(1,None),(1,None),(1,None),(1,0x90),(1,0x91),(1,0x92),
(1,0xa2),(1,0xa3),(1,None),(1,0x93),(1,0x94),(1,0x95),(1,0x96),(1,None),
(1,0xa4),(1,0xa5),(1,0x97),(1,0x98),(1,0x99),(1,0x9a),(1,None),(1,None),
(1,0xa6),(1,0xa7),(1,None),(1,0x9b),(1,0x9c),(1,0x9d),(1,None),(1,None),
(1,0xa8),(1,0xa9),(1,None),(1,None),(1,0x9e),(1,0x9f),(1,0xa0),(1,0xa1),
]

Face_Shrine_Layout = [
(1,0xd8),(1,0xd9),(1,0xda),(1,0xdb),(1,0xdc),(1,0xdd),(1,None),(1,None),
(1,0xb0),(1,None),(1,None),(1,None),(1,None),(1,None),(1,None),(1,0xb1),
(1,0xb2),(1,0xb3),(1,None),(1,0xb4),(1,0xb5),(1,None),(1,0xb6),(1,0xb7),
(1,0xb8),(1,0xb9),(1,0xba),(1,0xbb),(1,0xbc),(1,0xbd),(1,0xbe),(1,0xbf),
(1,0xc0),(1,0xc1),(1,0xc2),(1,0xc3),(1,0xc4),(1,0xc5),(1,0xc6),(1,0xc7),
(1,None),(1,0xc8),(1,0xc9),(1,0xca),(1,0xcb),(1,0xcc),(1,0xcd),(1,None),
(1,None),(1,0xce),(1,0xcf),(1,None),(1,None),(1,0xd0),(1,0xd1),(1,None),
(1,None),(1,0xd2),(1,0xd3),(1,0xd4),(1,0xd5),(1,0xd6),(1,0xd7),(1,None),
]

Eagles_Tower_Layout = [
(2,None),(2,0X11),(2,0X12),(2,None),(2,None),(2,None),(2,None),(2,0XE8),
(2,0X13),(2,0X14),(2,0X15),(2,0X16),(2,None),(2,0X2B),(2,0X2C),(2,0XF8),
(2,0X17),(2,0X18),(2,0X19),(2,0X1A),(2,None),(2,0X2D),(2,0X2E),(2,None),
(2,0X1B),(2,0X1C),(2,0X1D),(2,0X1E),(2,None),(2,None),(2,None),(2,None),
(2,0X01),(2,0X02),(2,0X03),(2,0X04),(2,None),(2,0X1F),(2,0X20),(2,None),
(2,0X05),(2,0X06),(2,0X07),(2,0X08),(2,0X21),(2,0X22),(2,0X23),(2,0X24),
(2,0X09),(2,0X0A),(2,0X0B),(2,0X0C),(2,0X25),(2,0X26),(2,0X27),(2,0X28),
(2,0X0D),(2,0X0E),(2,0X0F),(2,0X10),(2,None),(2,0X29),(2,0X2A),(2,None),
]

Eagles_Tower_collapse_Layout = [
(2,None),(2,0X11),(2,0X12),(2,None),(2,None),(2,None),(2,None),(2,0XE8),
(2,0X13),(2,0X14),(2,0X15),(2,0X16),(2,None),(2,None),(2,None),(2,0XF8),
(2,0X17),(2,0X18),(2,0X19),(2,0X1A),(2,None),(2,None),(2,None),(2,None),
(2,0X1B),(2,0X1C),(2,0X1D),(2,0X1E),(2,None),(2,None),(2,None),(2,None),
(2,0X01),(2,0X02),(2,0X03),(2,0X04),(2,None),(2,0X1F),(2,0X20),(2,None),
(2,0X05),(2,0X06),(2,0X07),(2,0X08),(2,0X21),(2,0X2B),(2,0X2C),(2,0X24),
(2,0X09),(2,0X0A),(2,0X0B),(2,0X0C),(2,0X25),(2,0X2D),(2,0X2E),(2,0X28),
(2,0X0D),(2,0X0E),(2,0X0F),(2,0X10),(2,None),(2,0X29),(2,0X2A),(2,None),
]

Turtle_Rock_Layout = [
(2,0X60),(2,0X61),(2,None),(2,0X30),(2,0X31),(2,None),(2,0X62),(2,0X63),
(2,0X32),(2,0X64),(2,0X65),(2,0X34),(2,0X35),(2,0X66),(2,0X67),(2,0X37),
(2,0X38),(2,0X39),(2,0X3A),(2,0X3B),(2,0X3C),(2,0X3D),(2,0X3E),(2,0X3F),
(2,None),(2,0X40),(2,0X41),(2,0X42),(2,0X43),(2,0X44),(2,0X45),(2,None),
(2,None),(2,0X46),(2,0X47),(2,0X48),(2,0X49),(2,0X4A),(2,0X4B),(2,None),
(2,0X4C),(2,0X4D),(2,0X4E),(2,0X4F),(2,0X50),(2,0X51),(2,0X52),(2,0X53),
(2,0X54),(2,0X55),(2,0X56),(2,0X57),(2,0X58),(2,0X59),(2,0X5A),(2,0X5B),
(2,0X5C),(2,0X68),(2,0X69),(2,0X5D),(2,0X5E),(2,0X6A),(2,0X6B),(2,0X5F),
]

Custom_Caves_Houses_Layout = [
(2,0XB6),(2,0XB7),(2,0XB8),(2,0XB9),(2,0X85),(2,0X86),(2,0XFD),(2,0XF3),(1,0xE3),(1,0xFA),(2,0x99),(2,0x9B),(2,0x9C),(2,0x9D),(2,0x9F),(2,0xA0),
(2,0XED),(2,0XEE),(2,0XEA),(2,0XEB),(2,0XEC),(2,0X87),(2,0XF1),(2,0XF2),(2,0xA1),(2,0xA2),(2,0xA3),(2,0xA5),(2,0xA6),(2,0xA7),(2,0xA8),(2,0xA9),
(2,0XFE),(2,0XEF),(2,0XBA),(2,0XBB),(2,0XBC),(2,0X8D),(2,0XF9),(2,0XFA),(2,0xAA),(2,0xAD),(2,0xB0),(2,0xB2),(2,0xB4),(2,0xC7),(2,0xCB),(2,0xCC),
(2,0X80),(2,0X81),(2,0X82),(2,0X83),(2,0X84),(2,0X8C),(2,0X88),(2,0X8A),(2,0xD7),(2,0xD9),(2,0xDA),(2,0xDB),(2,0xDC),(2,0xDD),(2,0xE3),(2,0xE9),
(2,0X90),(2,0X91),(2,0X92),(2,0xE5),(2,0X8E),(2,0X9A),(2,0X89),(2,0X8B),(0,None),(0,None),(0,None),(0,None),(0,None),(0,None),(0,None),(0,None),
(2,0X97),(2,0X93),(2,0X94),(2,0X95),(2,0X96),(2,0xF5),(2,0XAB),(2,0XAC),(0,None),(0,None),(0,None),(0,None),(0,None),(0,None),(0,None),(0,None),
(2,0X98),(2,0X7A),(2,0X7B),(2,0xCD),(2,0XE6),(2,0XE7),(2,0xB5),(2,0XBD),(0,None),(0,None),(0,None),(0,None),(0,None),(0,None),(0,None),(0,None),
(2,0xB3),(2,0X7C),(2,0X7D),(2,0X7E),(2,0XF6),(2,0XF7),(2,0XDE),(2,0XDF),(0,None),(0,None),(0,None),(0,None),(0,None),(0,None),(0,None),(0,None),
(1,0XE0),(1,0XE1),(1,0XE2),(1,0XAC),(1,0XE4),(1,0XE5),(1,0XE6),(1,0XE7),(0,None),(0,None),(0,None),(0,None),(0,None),(0,None),(0,None),(0,None),
(1,0XF0),(1,0XF1),(1,0XF2),(1,0XF3),(1,0XF4),(1,0XF5),(1,0XF6),(1,0XF7),(0,None),(0,None),(0,None),(0,None),(0,None),(0,None),(0,None),(0,None),
(1,0XE8),(1,0XE9),(1,0XEA),(1,0XEB),(1,0XEC),(1,0XED),(1,0XEE),(2,0x6F),(0,None),(0,None),(0,None),(0,None),(0,None),(0,None),(0,None),(0,None),
(1,0XF8),(1,0XF9),(2,0xFC),(1,0XFB),(1,0XFC),(1,0XFD),(1,0XFE),(2,0x7F),(0,None),(0,None),(0,None),(0,None),(0,None),(0,None),(0,None),(0,None),
(2,0xA4),(2,0xAE),(2,0xAF),(2,0xE4),(2,0xBE),(2,0xBF),(2,0xFB),(2,0x8F),(0,None),(0,None),(0,None),(0,None),(0,None),(0,None),(0,None),(0,None),
(2,0xC0),(2,0xC1),(2,0xB1),(2,0xF4),(2,0xCE),(2,0xCF),(2,0xC9),(2,0xCA),(0,None),(0,None),(0,None),(0,None),(0,None),(0,None),(0,None),(0,None),
(2,0xC2),(2,0xC3),(2,0xC5),(2,0xC6),(2,0xE0),(2,0xE1),(2,0xE2),(2,0xC8),(0,None),(0,None),(0,None),(0,None),(0,None),(0,None),(0,None),(0,None),
(2,0xD2),(2,0xD3),(2,0xD5),(2,0xD6),(2,0xF0),(2,0xD0),(2,0xD1),(2,0xD8),(0,None),(0,None),(0,None),(0,None),(0,None),(0,None),(0,None),(0,None),
]

WindFishEgg_Layout = [
(2,None),(2,None),(2,None),(2,None),(2,None),(2,None),(2,None),(2,None),
(2,None),(2,None),(2,None),(2,0X74),(2,None),(2,None),(2,None),(2,None),
(2,None),(2,None),(2,None),(2,0X73),(2,None),(2,None),(2,None),(2,None),
(2,None),(2,None),(2,None),(2,0X71),(2,None),(2,None),(2,None),(2,None),
(2,None),(2,None),(2,None),(2,0X72),(2,None),(2,None),(2,None),(2,None),
(2,None),(2,None),(2,None),(2,0X76),(2,None),(2,None),(2,None),(2,None),
(2,None),(2,None),(2,None),(2,0X75),(2,None),(2,None),(2,None),(2,None),
(2,None),(2,None),(2,None),(2,0X70),(2,None),(2,None),(2,None),(2,None),
]

Color_Dungeon_Layout = [
(3,None),(3,None),(3,None),(3,None),(3,None),(3,None),(3,None),(3,None),
(3,None),(3,None),(3,None),(3,None),(3,None),(3,None),(3,None),(3,None),
(3,None),(3,None),(3,None),(3,None),(3,None),(3,None),(3,None),(3,None),
(3,None),(3,0X00),(3,0X01),(3,None),(3,None),(3,0X02),(3,0X03),(3,None),
(3,None),(3,0X04),(3,0X05),(3,0X06),(3,0X07),(3,0X08),(3,0X09),(3,None),
(3,None),(3,None),(3,0X0A),(3,0X0B),(3,0X0C),(3,0X0D),(3,None),(3,None),
(3,None),(3,None),(3,0X0E),(3,0X0F),(3,0X10),(3,0X11),(3,None),(3,None),
(3,None),(3,None),(3,0X12),(3,0X13),(3,0X14),(3,0X15),(3,None),(3,None),
]

LAYOUTS = {
    MapLevel.TAIL_CAVE : (Tail_Cave_Layout, 8, 8),
    MapLevel.BOTTLE_GROTTO : (Bottle_Grotto_Layout, 8, 8),
    MapLevel.KEY_CAVERN : (Key_Cavern_Layout, 8, 8),
    MapLevel.ANGLERS_TUNNEL : (Anglers_Tunnel_Layout, 8, 8),
    MapLevel.CATFISHS_MAW : (Catfishs_Maw_Layout, 8, 8),
    MapLevel.FACE_SHRINE : (Face_Shrine_Layout, 8, 8),
    MapLevel.EAGLES_TOWER : (Eagles_Tower_Layout, 8, 8),
    MapLevel.EAGLES_TOWER_ALT : (Eagles_Tower_collapse_Layout, 8, 8),
    MapLevel.TURTLE_ROCK : (Turtle_Rock_Layout, 8, 8),
    MapLevel.WINDFISHS_EGG : (WindFishEgg_Layout, 8, 8),
    MapLevel.COLOR_DUNGEON : (Color_Dungeon_Layout, 8, 8),
    MapLevel.CAVES_HOUSES : (Custom_Caves_Houses_Layout, 16, 16),
}

def load_layouts():

    for l in LAYOUTS.keys():
        layout, width, height = LAYOUTS[l]
        for i, (level, room_id) in enumerate(layout):
            if room_id is None:
                continue
            
            MapLookup[l][room_id] = (i % width, i // width)
    print("Loaded layouts")


def lookup_world_map_coords(overworld_bool,map_id,room_id):

    if overworld_bool:

        return room_id % 16, room_id // 16, MapLevel.OVERWORLD
    
    else:

        map = Map(map_id)

        overworld_type = map.get_overworld_type()
        map_level = map.get_map_level()

        if map_level in MapLookup.keys():
            if room_id in MapLookup[map_level].keys():
                return MapLookup[map_level][room_id][0], MapLookup[map_level][room_id][1], map_level
    
    raise ValueError("Not a valid room_id for this map")


load_layouts()







