"""
This file is part of the Outfit Customization mod licensed under the Creative Commons Attribution-NonCommercial-NoDerivatives 4.0 International public license (CC BY-NC-ND 4.0).
https://creativecommons.org/licenses/by-nc-nd/4.0/
https://creativecommons.org/licenses/by-nc-nd/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from typing import Iterator
from cnoutfitcustomization.outfit_parts.outfit_part import OCOutfitPart
from cnoutfitcustomization.outfit_parts.outfit_parts_loader import OCOutfitPartsLoader
from sims.sim_info import SimInfo
from sims4communitylib.enums.common_species import CommonSpecies
from sims4communitylib.utils.sims.common_age_utils import CommonAgeUtils


class OCOutfitPartsQueryUtils:
    """ Utilities for querying outfit parts. """
    @staticmethod
    def query_outfit_parts_for_sim(sim_info: SimInfo) -> Iterator[OCOutfitPart]:
        """ Retrieve outfit parts with all of the specified tags. """
        for outfit_part in OCOutfitPartsLoader.get().get_loaded_outfit_parts():
            if not OCOutfitPartsQueryUtils.is_available_for_sim(outfit_part, sim_info):
                continue
            yield outfit_part

    @staticmethod
    def is_available_for_sim(outfit_part: OCOutfitPart, sim_info: SimInfo) -> bool:
        """ Determine if an outfit part is available for a sim. """
        age = CommonAgeUtils.get_age(sim_info)
        if age not in outfit_part.available_for.ages:
            return False
        # gender = CommonGenderUtils.get_gender(sim_info)
        # if gender not in outfit_part.available_for.genders:
        #     return False
        common_species = CommonSpecies.get_species(sim_info)
        if common_species not in outfit_part.available_for.species:
            return False
        return True

    @staticmethod
    def query_outfit_parts_by_tags(tags: str) -> Iterator[OCOutfitPart]:
        """ Retrieve outfit parts with all of the specified tags. """
        for outfit_part in OCOutfitPartsLoader.get().get_loaded_outfit_parts():
            should_skip = False
            for tag in tags:
                if tag not in outfit_part.part_tags:
                    should_skip = True
                    break
            if should_skip:
                continue
            yield outfit_part
