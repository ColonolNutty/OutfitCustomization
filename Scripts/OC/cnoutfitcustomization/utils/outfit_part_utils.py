"""
This file is part of the Outfit Customization mod licensed under the Creative Commons Attribution-NonCommercial-NoDerivatives 4.0 International public license (CC BY-NC-ND 4.0).
https://creativecommons.org/licenses/by-nc-nd/4.0/
https://creativecommons.org/licenses/by-nc-nd/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from typing import Tuple, Iterator, Union

from cnoutfitcustomization.modinfo import ModInfo
from cnoutfitcustomization.outfit_parts.outfit_part import OCOutfitPart
from cnoutfitcustomization.outfit_parts.query.outfit_parts_query_utils import OCOutfitPartsQueryUtils
from sims.outfits.outfit_enums import BodyType
from sims.sim_info import SimInfo
from sims4communitylib.utils.cas.common_cas_utils import CommonCASUtils
from sims4communitylib.utils.common_log_registry import CommonLogRegistry

log = CommonLogRegistry.get().register_log(ModInfo.get_identity().name, 'oc_outfit_part_utils')


class OCOutfitPartUtils:
    """ Utilities for managing outfit parts of sims. """
    @staticmethod
    def get_outfit_parts(sim_info: SimInfo) -> Iterator[OCOutfitPart]:
        """ Retrieve outfit parts that match the sim. """
        return OCOutfitPartsQueryUtils.query_outfit_parts_for_sim(sim_info)

    @staticmethod
    def remove_outfit_parts(sim_info: SimInfo, outfit_parts: Tuple[OCOutfitPart]):
        """ Remove the specified outfit parts from a sim. """
        log.format_with_message('Removing outfit parts', outfit_parts=outfit_parts)
        for outfit_part in outfit_parts:
            if OCOutfitPartUtils.remove_cas_part(sim_info, outfit_part.part_id, body_type=None):
                log.format_with_message('Removed outfit part.', outfit_part=outfit_part)
                continue
            log.format_with_message('Failed to remove outfit part.', outfit_part=outfit_part)

    @staticmethod
    def remove_cas_part(sim_info: SimInfo, cas_part_id: int, body_type: Union[BodyType, None]) -> bool:
        """ Remove the specified outfit part from a sim. """
        log.format_with_message('Attempting to remove outfit part from sim.', cas_part_id=cas_part_id, body_type=body_type)

        return CommonCASUtils.detach_cas_part_from_sim(sim_info, cas_part_id, body_type=body_type)

    @staticmethod
    def add_cas_part(sim_info: SimInfo, cas_part_id: int, body_type: Union[BodyType, None]) -> bool:
        """ Add the specified outfit part to a sim. """
        log.format_with_message('Attempting to add outfit part to sim.', cas_part_id=cas_part_id, body_type=body_type)
        return CommonCASUtils.attach_cas_part_to_sim(sim_info, cas_part_id, body_type=body_type)
