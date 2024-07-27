
from enum import IntEnum

class Inventory(IntEnum):

    EMPTY = 0x00
    SWORD = 0x01
    BOMBS = 0x02
    POWER_BRACELET = 0x03
    SHIELD = 0x04
    BOW = 0x05
    HOOKSHOT = 0x06
    MAGIC_ROD = 0x07
    PEGASUS_BOOTS = 0x08
    OCARINA = 0x09
    ROCS_FEATHER = 0x0A
    SHOVEL = 0x0B
    MAGIC_POWDER = 0x0C
    BOOMERANG = 0x0D





INVENTORY_CYCLE = [
    Inventory.EMPTY,
    Inventory.SHIELD,
    Inventory.BOMBS,
    Inventory.POWER_BRACELET,
    Inventory.BOW,
    Inventory.HOOKSHOT,
    Inventory.SWORD,
    Inventory.MAGIC_ROD,
    Inventory.PEGASUS_BOOTS,
    Inventory.OCARINA,
    Inventory.ROCS_FEATHER,
    Inventory.SHOVEL,
    Inventory.MAGIC_POWDER,
    Inventory.BOOMERANG
]