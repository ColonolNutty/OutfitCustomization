"""
This file is part of the Outfit Customization mod licensed under the Creative Commons Attribution-NonCommercial-NoDerivatives 4.0 International public license (CC BY-NC-ND 4.0).
https://creativecommons.org/licenses/by-nc-nd/4.0/
https://creativecommons.org/licenses/by-nc-nd/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from sims.sim_info import SimInfo
from sims4communitylib.utils.sims.common_age_utils import CommonAgeUtils


class OCSettingUtils:
    """ Utilities used by the OC mod. """
    @staticmethod
    def is_enabled_for_interactions(sim_info: SimInfo) -> bool:
        """ Determine if a Sim can perform the Outfit Customization interactions. """
        return not CommonAgeUtils.is_baby(sim_info)
