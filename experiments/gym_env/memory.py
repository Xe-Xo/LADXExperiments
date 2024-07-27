from enum import Enum

class Registers(Enum):
    # Bank, Address
    PUSH_SFX  = (0x15, 0x7413) #526E
    COLLISION = (0x02, 0x7277)
    BLOCK_SFX = (0x03, 0x6C50)
    SWORD_DMG = (0x03, 0x719D)
    

    def hook_register(self, pyboy, callback, args):
        #print(f"Registering hook for {self.name} at {hex(self.value[0])}:{hex(self.value[1])}")
        try:
            pyboy.hook_register(self.value[0], self.value[1], callback, args)
        except ValueError:
            pass

    def hook_deregister(self, pyboy):
        #print(f"Deregistering hook for {self.name} at {hex(self.value[0])}:{hex(self.value[1])}")
        try:
            pyboy.hook_deregister(self.value[0], self.value[1])
        except:
            pass

import pyboy

class RamAddress(Enum):

    # Link Specific Info
    # -- Probably needed for agent to make short term decisions

    hLinkPositionX = 0xFF98
    hLinkPositionY = 0xFF99
    hLinkSpeedX = 0xFF9A
    hLinkSpeedY = 0xFF9B
    hGameOverStage = 0xFF9C
    hLinkAnimationState = 0xFF9D
    hLinkDirection = 0xFF9E
    hLinkFinalPositionX = 0xFF9F
    hLinkFinalPositionY = 0xFFA0
    hLinkInteractiveMotionBlocked = 0xFFA1
    hLinkPositionZ = 0xFFA2
    hLinkVelocityZ = 0xFFA3
    hLinkSlowWalkingSpeed = 0xFFB2
    hButtonsInactiveDelay = 0xFFB5
    hLinkCountdown = 0xFFB7
    hObjectUnderLink = 0xFFB8
    hLinkRoomPosition = 0xFFFA
    hLinkFinalRoomPosition = 0xFFFB
    wLinkGroundStatus = 0xC11F
    wLinkMotionState = 0xC11C
    wIsUsingSpinAttack = 0xC121
    wSwordCharge = 0xC122
    wIsLinkPushing = 0xC144
    wIsLinkInTheAir = 0xC146


    # Game Progress Info
    wGameplayType = 0xDB95
    wGameplaySubtype = 0xDB96
    wShouldGetLostInMysteriousWoods = 0xC10C

    # Room Specific Info
    hMapRoom = 0xFFF6
    hMapId = 0xFFF7
    hRoomStatus = 0xFFF8
    hisSideScrolling =  0xFFF9

    wRoomEvent = 0xC18E
    wRoomEventEffectExecuted = 0xC18F

    hStaircase = 0xFFAC
    hStaircasePosX = 0xFFAD
    hStaircasePosY = 0xFFAE



    hJingle = 0xFFF2

    wRoomTransitionState  = 0xC124
    wRoomTransitionDirection = 0xC125

    wCollisionType = 0xC133
    wDialogCooldown = 0xC134

    wSwordDirection = 0xC136
    wIgnoreLinkCollisionsCountdown = 0xC13E


    wIsRunningWithPegasusBoots = 0xC14A
    wPegasusBootsChargeMeter = 0xC14B
    wActiveProjectileCount  = 0xC14D

    wHasPlacedBomb = 0xC14E

    wHasMirrorShield = 0xC15A
    wIsUsingShield = 0xC15B
    wIsCarryingLiftedObject = 0xC15C
    wIsOnLowHeath = 0xC163

    wTransitionSequenceCounter = 0xC16B


    wItemUsageContext = 0xC1AD
    wInBossBattle = 0xC18E

    wLatestDroppedBombEntityIndex = 0xC1C1
    wLatestShotArrowEntityIndex = 0xC1C2

    wLinkUsingShovel = 0xC1C7
    wSwitchButtonPressed = 0xC1CB
    wDialogIsWaitingForButtonPress = 0xC1CC

    wEntitiesPosXTable = 0xC200 # x10
    wEntitiesPosYTable = 0xC210 # x10
    wEntitiesPosXSignTable = 0xC220 # x10
    wEntitiesPosYSignTable = 0xC230 # x10
    wEntitiesSpeedXTable = 0xC240 # x10
    wEntitiesSpeedYTable = 0xC250 # x10
    wEntitiesStatusTable = 0xC280 # x10
    wEntitiesStateTable = 0xC290 # x10
    wEntitiesCollisionsTable = 0xC2A0 # x10
    wEntitiesPrivateState1Table = 0xC2B0 # x10
    wEntitiesPrivateState2Table = 0xC2C0 # x10
    wEntitiesPrivateState3Table = 0xC2D0 # x10
    wEntitiesTransitionCountdownTable = 0xC2E0 # x10
    wEntitiesPrivateCountdown1Table = 0xC2F0 # x10
    wEntitiesPrivateCountdown2Table = 0xC300 # x10
    wEntitiesPosZTable = 0xC310 # x10
    wEntitiesPhysicsFlagsTable = 0xC340 # x10
    wEntitiesHitboxFlagsTable = 0xC350 # x10
    wEntitiesHealthTable = 0xC360 # x10
    wEntitiesDirectionTable = 0xC380 # x10
    wEntitiesPrivateState5Table = 0xC390 # x10
    wEntitiesTypeTable = 0xC3A0 #x10
    wEntitiesIgnoreHitsCountdownTable = 0xC410 # x10
    wEntitiesFlashCountdownTable = 0xC420 # x10
    wEntitiesOptions1Table = 0xC430 # x10
    wEntitiesPrivateState4Table = 0xC440 # x10
    wEntitiesLiftedTable = 0xC490 # x10
    wEntitiesHitboxPositionTable = 0xD580 # x40 (x,y,w,h) (4 times 16 entities)


    wShopItemList = 0xC505 # x4
    wItemPickedUpInShop = 0xC509
    wBlockItemUsage = 0xC50A
    wEggMazeProgress = 0xC5AA
    wSwordCollisionEnabled = 0xC5B0

    wFinalNightmareForm = 0xD219

    wWarp0MapCategory = 0xD401
    wWarp0Map = 0xD402
    wWarp0Room = 0xD403
    wWarp0DestinationX = 0xD404
    wWarp0DestinationY = 0xD405
    wWarp0PositionTileIndex = 0xD416

    wWarp1MapCategory = 0xD406
    wWarp1Map = 0xD407
    wWarp1Room = 0xD408
    wWarp1DestinationX = 0xD409
    wWarp1DestinationY = 0xD40A
    wWarp1PositionTileIndex = 0xD417

    wWarp2MapCategory = 0xD40B
    wWarp2Map = 0xD40C
    wWarp2Room = 0xD40D
    wWarp2DestinationX = 0xD40E
    wWarp2DestinationY = 0xD40F
    wWarp2PositionTileIndex = 0xD418

    wWarp3MapCategory = 0xD410
    wWarp3Map = 0xD411
    wWarp3Room = 0xD412
    wWarp3DestinationX = 0xD413
    wWarp3DestinationY = 0xD414
    wWarp3PositionTileIndex = 0xD419

    wPieceOfPowerKillCount = 0xD415
    wGuardianAcornCounter = 0xD471
    wDidStealItem = 0xD47E

    
    wLinkStandingOnSwitchBlock = 0xD6F9
    wRoomSwitchableObject = 0xD6FA
    wSwitchBlocksState = 0xD6FB

    wRoomObjectsArea = 0xD700 # 0x11
    wRoomObjects = 0xD711 # 0xEF

    wOverworldRoomStatus = 0xD800 # 0x100
    wIndoorARoomStatus = 0xD900 # 0x100
    wIndoorBRoomStatus = 0xDA00 # 0x100

    wInventoryItems_BSlot = 0xDB00 # 0x1
    wInventoryItems_ASlot = 0xDB01 # 0x1
    wInventoryItems_SubSlot1 = 0xDB02 # 0x1
    wInventoryItems_SubSlot2 = 0xDB03 # 0x1
    wInventoryItems_SubSlot3 = 0xDB04 # 0x1
    wInventoryItems_SubSlot4 = 0xDB05 # 0x1
    wInventoryItems_SubSlot5 = 0xDB06 # 0x1
    wInventoryItems_SubSlot6 = 0xDB07 # 0x1
    wInventoryItems_SubSlot7 = 0xDB08 # 0x1
    wInventoryItems_SubSlot8 = 0xDB09 # 0x1
    wInventoryItems_SubSlot9 = 0xDB0A # 0x1
    wInventoryItems_SubSlot10 = 0xDB0B # 0x1

    wHasFlippers = 0xD80C
    wHasMedicine = 0xDB0D
    wTradeSequenceItem = 0xDB0E

    wSeashellsCount = 0xDB0F
    wHasTailKey = 0xDB11
    wHasAnglerKey = 0xDB12
    wHasFaceKey = 0xDB13
    wHasBirdKey = 0xDB14

    wGoldenLeavesCount = 0xDB15

    wDungeonItemFlags = 0xDB16
    wPowerBraceletLevel = 0xDB43
    wShieldLevel = 0xDB44
    wArrowCount = 0xDB45

    wHasStolenFromShop = 0xDB46
    wOcarinaSongFlags = 0xDB49
    wHasToadstool = 0xDB4B
    wMagicPowderCount = 0xDB4C
    wBombCount = 0xDB4D
    wSwordLevel = 0xDB4E

    wIsBowWowFollowingLink = 0xDB56
    wHealth = 0xDB5A
    wMaxHearts = 0xDB5B
    wHeartPiecesCount = 0xDB5C
    wRupeeCountHigh = 0xDB5D
    wRupeeCountLow = 0xDB5E

    wMaxMagicPowder = 0xDB76
    wMaxBombs = 0xDB77
    wMaxArrows = 0xDB78

    wTransitionGfxFrameCount = 0xC180
    wTransitionGfx = 0xC17F

    wIsIndoor = 0xDBA5
    wIndoorRoom = 0xDBAE
    wKillCount = 0xDBB5

    wTunicType = 0xDC0F

    def read_memory_bytes(self, pyboy, bytes):
        return pyboy.memory[self.value:self.value+bytes]
    
    def read_memory(self, pyboy):
        return pyboy.memory[self.value]
    
    def write_memory(self, pyboy, value):
        pyboy.memory[self.value] = value




















