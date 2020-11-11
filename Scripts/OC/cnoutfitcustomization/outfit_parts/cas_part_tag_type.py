"""
This file is part of the Outfit Customization mod licensed under the Creative Commons Attribution-NonCommercial-NoDerivatives 4.0 International public license (CC BY-NC-ND 4.0).
https://creativecommons.org/licenses/by-nc-nd/4.0/
https://creativecommons.org/licenses/by-nc-nd/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from sims4communitylib.enums.enumtypes.common_int import CommonInt


class OCCASPartTagType(CommonInt):
    """ Tag types. """
    ALL: 'OCCASPartTagType' = 0
    SIM_DETAILS: 'OCCASPartTagType' = 1
    GENDER: 'OCCASPartTagType' = 2
    AGE: 'OCCASPartTagType' = 3
    SPECIES: 'OCCASPartTagType' = 4
    CUSTOM_TAG: 'OCCASPartTagType' = 5
