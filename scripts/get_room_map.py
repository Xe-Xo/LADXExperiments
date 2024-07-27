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

LayoutList = [
    Custom_Caves_Houses_Layout,
]




def check_rooms():
    room_map_dict = {}
    count = 0

    for i in range(1,4):
        for y in range(0,0x10):
            for x in range(0,0x10):
                found = False
                
                for a,(room_list) in enumerate(LayoutList):

                    for a_index,(room_abc, room_num) in enumerate(room_list):
                        if i == room_abc and y*0x10+x == room_num:
                            if found == True:
                                room_map_dict[(i,y*0x10+x)].append((a,a_index))
                            else:
                                found = True
                                room_map_dict[(i,y*0x10+x)] = [(a,a_index)]

                
                if found == False:
                    if i != 3:
                        count += 1
                        print(f"Room not found: {i} {padded_hex(y*0x10+x,2)}")

    print(count)

    import json

    new_json = {}
    for i in room_map_dict.keys():
        a,b = i
        if a not in new_json.keys():
            new_json[a] = []
        if b != len(new_json[a]):
            print(f"Error: {a} {b} {len(new_json[a])}")
            
        new_json[a].append((room_map_dict[i][0][1] // 8, room_map_dict[i][0][1] % 8, room_map_dict[i][0][0]))

    with open("room_map.json","w") as f:
        json.dump(new_json, f, indent=2)

    for i in room_map_dict.keys():
        a,b = i
        
        if len(room_map_dict[i]) > 1:
            print(f"Multiple rooms found: {i} {room_map_dict[i]}")
        else:
            print(a,padded_hex(b,2), room_map_dict[i][0][0],(room_map_dict[i][0][1] // 8, room_map_dict[i][0][1] % 8))





def padded_hex(i,l):
    return f"{i:#00{l+2}x}".upper()

def resort_lists():
    str_ = "Nulls_proper = [\n"
    a, b = Nulls
    for n,c in enumerate(b):
        if c is None:
            str_ += f"({a},None)," 
        else:
            str_ += f"({a},{padded_hex(c,2)}),"
        if n % 8 == 7:
            str_ += "\n"

    str_ += "]"
    print(str_)

            
import PIL
import PIL.Image



def get_room_map_section(room_x, room_y, room_z):

    

    if room_z == 0:
        source_image = "assets//bigmap0.png"
    elif room_z == 1:
        source_image = "assets//bigmap1.png"
    elif room_z == 2:
        source_image = "assets//bigmap2.png"
    else:
        raise ValueError("room section?")
    
    room_size = (160,128)

    x0 = room_x * room_size[0]
    y0 = room_y * room_size[1]
    x1 = x0 + room_size[0]
    y1 = y0 + room_size[1]
    
    img = PIL.Image.open(source_image)
    room_section = img.crop((x0,y0,x1,y1))
    return room_section



import math
def generate_image(room_list,name):

    layout_sizes = {
    "Tail_Cave": (7,6),
    "Bottle_Grotto": (6,7),
    "Key_Cavern": (6,8),
    "Anglers_Tunnel": (7,7),
    "Catfishs_Maw": (7,8),
    "Face_Shrine": (8,8),
    "Eagles_Tower": (8,8),
    "Eagles_Tower_collapse": (8,8),
    "Turtle_Rock": (8,8),
    "WindFishEgg": (8,8),
    "WindFishEgg_seq1": (4,4),
    "WindFishEgg_seq2": (2,5),
    "WindFishEgg_seq3": (4,6),
    "WindFishEgg_seq4": (5,5),
    "Overworld": (16,16),
    "Custom_Caves_Houses": (16,16),
    }

    if name in layout_sizes.keys():
        
        room_list_len = layout_sizes[name][1]
        other = layout_sizes[name][0]
        name = name + "_squish"
    else:
        room_list_len = int(math.ceil(len(room_list) / 8))
        other = 8

    im = PIL.Image.new("RGB",(160*other,128*room_list_len),(0,0,0))
    for a,(i,b) in enumerate(room_list):
        x = a % other
        y = a // other

        if b is not None:
            print(x,y)
            #print(i*16+j/8*16)
            room = get_room_map_section(b%16,b//16,i)
            im.paste(room,(x*160,y*128))
    print(len(room_list))

    im.save(f"assets/generated/{name}.png")




def save_room_pic(room_tuple):
    #if room_tuple[2] != 0:
    #    return
    get_room_map_section(room_tuple[0],room_tuple[1],room_tuple[2]).save(f"assets/rooms/{room_tuple[2]}_{room_tuple[0]}_{room_tuple[1]}.png")


    

if __name__ == "__main__":
    print("Starting")
    save_room_pic((2,11,2))

    #generate_image(Custom_Caves_Houses_Layout,"Custom_Caves_Houses")
    #generate_image(Tail_Cave_squish,"Tail_Cave")
    #generate_image(Bottle_Grotto_squish,"Bottle_Grotto")
    #generate_image(Key_Cavern_squish,"Key_Cavern")
    #generate_image(Anglers_Tunnel_squish,"Anglers_Tunnel")
    #generate_image(WindFishEgg_proper_seq1,"WindFishEgg_seq1")
    #generate_image(WindFishEgg_proper_seq2,"WindFishEgg_seq2")
    #generate_image(WindFishEgg_proper_seq3,"WindFishEgg_seq3")
    #generate_image(WindFishEgg_proper_seq4,"WindFishEgg_seq4")
    #generate_image(Face_Shrine_proper,"Face_Shrine")
    #generate_image(Eagles_Tower_proper,"Eagles_Tower")
    #generate_image(Eagles_Tower_collapse_proper,"Eagles_Tower_collapse")
    #generate_image(Turtle_Rock_proper,"Turtle_Rock")
    #generate_image(WindFishEgg_proper,"WindFishEgg")
    #generate_image(Color_Dungeon_proper,"Color_Dungeon")
    #generate_image(Custom_Caves_proper,"Caves")
    #generate_image(House_proper,"Houses")
    #generate_image(Nulls_proper,"Nulls")    


