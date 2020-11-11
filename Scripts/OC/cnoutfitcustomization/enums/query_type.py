"""
This file is part of the Outfit Customization mod licensed under the Creative Commons Attribution-NonCommercial-NoDerivatives 4.0 International public license (CC BY-NC-ND 4.0).
https://creativecommons.org/licenses/by-nc-nd/4.0/
https://creativecommons.org/licenses/by-nc-nd/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from sims4communitylib.enums.enumtypes.common_int import CommonInt


class OCQueryType(CommonInt):
    """ Query types. """
    ALL_PLUS_ANY: 'OCQueryType' = 0
    ALL_INTERSECT_ANY: 'OCQueryType' = 1
    ALL_PLUS_ANY_MUST_HAVE_ONE: 'OCQueryType' = 2
    ALL_INTERSECT_ANY_MUST_HAVE_ONE: 'OCQueryType' = 3
