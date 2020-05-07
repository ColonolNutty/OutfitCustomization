"""
The Sims 4 Community Library is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from sims4communitylib.enums.enumtypes.int_enum import CommonEnumIntBase


class CommonInteractionId(CommonEnumIntBase):
    """Identifiers for interactions.

    """
    PICK_UP_SIM = 141018
    PICK_UP_SIM_REVERSED = 141925
    CARRY_PICK_UP_TO_BED = 156217
    CARRY_PICK_UP = 134423
    CARRY_PICK_UP_FROM_SEATED = 155633
    CARRY_HUG = 155721
    CARRY_HOLD_OBJECT = 13135
    CARRY_HOLD_SIM = 132170
    CALL_INTO_ARMS_PICK_UP_PET = 173668
    SIM_TO_PET_NON_TOUCHING_PICKUP_PET = 186124
    SOCIAL_MIXER_SUPER_PICK_UP_PET = 160585
    MIXER_SOCIAL_T_PETS_FRIENDLY_HOLD_UP_CARRYING_CHILD = 168236
    GO_HERE = 14410
    SUPER_INTERACTION_GO_HERE = 27242
    GUITAR_PRACTICE = 13471

    SIM_STAND = 13983
    SIM_STAND_EXCLUSIVE = 23835
    STAND_PASSIVE = 14310
    SIM_SWIM = 102325
    SIM_CHAT = 13998
    CAT_STAND = 120562
    CAT_STAND_PASSIVE = 120558
    DOG_STAND = 120569
    DOG_STAND_PASSIVE = 120561
    DOG_SWIM = 170682
    DOG_SWIM_PASSIVE = 174558

    # Deliver Baby
    DELIVER_BABY_CAT = 159901
    DELIVER_BABY_DOG = 159902
    BASSINET_DELIVER_BABY = 13070
    SIM_DELIVER_BABY_CREATE_BASSINET = 97294

    # Sit
    SEATING_SIT = 31564
    SEATING_SIT_TODDLER_BED = 156920
    SEATING_SIT_SINGLE = 74779
    SEATING_SIT_CTYAE = 157667
    SEATING_SIT_RESTAURANT_RALLY_ONLY = 134949
    SEATING_SIT_POST_GRAND_MEAL_WAIT_ENJOY_COMPANY = 182774
    SEATING_SIT_DIRECTOR_CHAIR = 191162
    SEATING_SIT_HAIR_MAKE_UP_CHAIR = 201508
    SIT_PASSIVE = 14244

    # Shower
    GENERIC_SHOWER = 13439
    SHOWER_TAKE_SHOWER = 13950
    SHOWER_TAKE_SHOWER_NO_PRIVACY = 110817
    SHOWER_TAKE_SHOWER_PASSIVE = 13952
    SHOWER_TAKE_SHOWER_APARTMENT_NEIGHBOR_FLIRTY = 154397
    SHOWER_TAKE_SHOWER_BRISK = 39965
    SHOWER_TAKE_SHOWER_BRISK_NO_PRIVACY = 110818
    SHOWER_TAKE_SHOWER_COLD_SHOWER = 24332
    SHOWER_TAKE_SHOWER_COLD_SHOWER_NO_PRIVACY = 110819
    SHOWER_TAKE_SHOWER_ENERGIZED = 23839
    SHOWER_TAKE_SHOWER_ENERGIZED_NO_PRIVACY = 110820
    SHOWER_TAKE_SHOWER_SING_IN_SHOWER = 141926
    SHOWER_TAKE_SHOWER_STEAMY = 39860
    SHOWER_TAKE_SHOWER_STEAMY_NO_PRIVACY = 110821
    SHOWER_TAKE_SHOWER_THOUGHTFUL = 39845
    SHOWER_TAKE_SHOWER_THOUGHTFUL_NO_PRIVACY = 110822
    SUPER_INTERACTION_CAMPING_BATHROOM_SHOWER_FEMALE = 104658
    SUPER_INTERACTION_CAMPING_BATHROOM_SHOWER_MALE = 104659
    SIM_RAIN_SHOWER = 185951
    SOCIAL_MIXER_SHOWER_SING_IN_SHOWER = 141216
    SOCIAL_MIXER_SHOWER_SING_IN_SHOWER_AUTONOMOUS = 141928

    # Bath
    GENERIC_BATH = 13427
    GENERIC_BUBBLE_BATH = 35352
    GENERIC_RELAXING_BATH = 120467
    BATHTUB_TAKE_BATH_LOOP = 13085
    BATHTUB_TAKE_BATH_RELAXING_BATH_IDLE_LOOP = 120473
    BATHTUB_TAKE_BATH_RELAXING_BATH_PLAY = 120474
    BATHTUB_TAKE_BATH_RELAXING_BATH_FALL_ASLEEP = 120475
    BATHTUB_TAKE_BATH_RELAXING_BATH_IDLE_LOOP_MUD = 121800
    BATHTUB_TAKE_BATH_RELAXING_BATH_PLAY_MUD = 121804
    BATHTUB_TAKE_BATH_RELAXING_BATH_FALL_ASLEEP_MUD = 121802
    BATHTUB_TAKE_BUBBLE_BATH_MERMAID = 213939
    BATHTUB_TAKE_BATH_MERMAID = 213938
    BATHTUB_NAP_MERMAID = 215915
    BATHTUB_PLAY_MERMAID = 215876
    IDLE_HYGIENE_MERMAID = 215764

    # S4CL
    S4CL_DEBUG_SHOW_RUNNING_AND_QUEUED_INTERACTIONS = 5900237111545222349
    S4CL_DEBUG_SHOW_ACTIVE_BUFFS = 12481803320243318715
    S4CL_DEBUG_SHOW_TRAITS = 2108116777929577381
    S4CL_DEBUG_SHOW_RUNNING_SITUATIONS = 10355438442708473961