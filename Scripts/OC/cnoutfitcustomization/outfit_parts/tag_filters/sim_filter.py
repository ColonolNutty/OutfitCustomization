"""
This file is part of the Outfit Customization mod licensed under the Creative Commons Attribution-NonCommercial-NoDerivatives 4.0 International public license (CC BY-NC-ND 4.0).
https://creativecommons.org/licenses/by-nc-nd/4.0/
https://creativecommons.org/licenses/by-nc-nd/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from typing import Tuple

from cnoutfitcustomization.outfit_parts.cas_part_query_tag import OCCASPartQueryTag
from cnoutfitcustomization.outfit_parts.cas_part_tag_type import OCCASPartTagType
from cnoutfitcustomization.outfit_parts.tag_filters.cas_part_tag_filter import OCCASPartTagFilter
from sims.sim_info import SimInfo
from sims4communitylib.enums.common_species import CommonSpecies
from sims4communitylib.utils.sims.common_age_utils import CommonAgeUtils
from sims4communitylib.utils.sims.common_gender_utils import CommonGenderUtils
from sims4communitylib.utils.sims.common_sim_name_utils import CommonSimNameUtils


class OCSimCASPartFilter(OCCASPartTagFilter):
    """ Filter CAS Parts for a Sim. """
    def __init__(self, sim_info: SimInfo) -> None:
        super().__init__(True, tag_type=OCCASPartTagType.SIM_DETAILS)
        self._sim_info = sim_info

    # noinspection PyMissingOrEmptyDocstring
    def get_tags(self) -> Tuple[OCCASPartQueryTag]:
        result: Tuple[OCCASPartQueryTag] = (
            OCCASPartQueryTag(OCCASPartTagType.AGE, CommonAgeUtils.get_age(self._sim_info)),
            OCCASPartQueryTag(OCCASPartTagType.GENDER, CommonGenderUtils.get_gender(self._sim_info)),
            OCCASPartQueryTag(OCCASPartTagType.SPECIES, CommonSpecies.get_species(self._sim_info)),
        )
        return result

    def __str__(self) -> str:
        return '{}: {}, Age: {}, Gender: {}, Species: {}'.format(
            self.__class__.__name__,
            CommonSimNameUtils.get_full_name(self._sim_info),
            CommonAgeUtils.get_age(self._sim_info),
            CommonGenderUtils.get_gender(self._sim_info),
            CommonSpecies.get_species(self._sim_info)
        )
