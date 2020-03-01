"""
This file is part of the Outfit Customization mod licensed under the Creative Commons Attribution-NonCommercial-NoDerivatives 4.0 International public license (CC BY-NC-ND 4.0).
https://creativecommons.org/licenses/by-nc-nd/4.0/
https://creativecommons.org/licenses/by-nc-nd/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from pprint import pformat
from typing import Tuple
from protocolbuffers.Localization_pb2 import LocalizedString
from sims.sim_info_types import Age, Gender
from sims4communitylib.enums.common_species import CommonSpecies
from sims4communitylib.utils.cas.common_cas_utils import CommonCASUtils
from tag import Tag


class OCOutfitPartAvailableFor:
    """ Holds information for what types of sims the part is available for. """
    def __init__(
        self,
        genders: Tuple[Gender],
        ages: Tuple[Age],
        species: Tuple[CommonSpecies]
    ):
        self._genders = genders
        self._ages = ages
        self._species = species

    @property
    def genders(self) -> Tuple[Gender]:
        """ Genders the part is available for. """
        return self._genders

    @property
    def ages(self) -> Tuple[Age]:
        """ Ages the part is available for. """
        return self._ages

    @property
    def species(self) -> Tuple[CommonSpecies]:
        """ Species the part is available for. """
        return self._species

    def is_valid(self) -> bool:
        """ Determine if available for is valid. """
        return len(self.genders) > 0 or len(self.ages) > 0 or len(self.species) > 0

    def __repr__(self) -> str:
        return '<genders:{}, ages:{}, species:{}>'\
            .format(pformat(self.genders), pformat(self.ages), pformat(self.species))

    def __str__(self) -> str:
        return self.__repr__()


class OCOutfitPart:
    """ Holds information related to an Outfit part. """
    def __init__(
        self,
        display_name: LocalizedString,
        raw_display_name: str,
        author: str,
        icon_id: int,
        part_id: int,
        available_for: OCOutfitPartAvailableFor,
        part_tags: Tuple[Tag],
        icon_key: str=None
    ):
        self._display_name = display_name
        self._raw_display_name = raw_display_name
        self._author = author
        self._icon_id = icon_id
        self._icon_key = icon_key
        self._part_id = part_id
        self._available_for = available_for
        self._part_tags = part_tags

    @property
    def display_name(self) -> LocalizedString:
        """ The string display name of the outfit part. """
        return self._display_name

    @property
    def raw_display_name(self) -> str:
        """ The raw text display name of the outfit part. """
        return self._raw_display_name

    @property
    def author(self) -> str:
        """ Author of the outfit part. """
        return self._author

    @property
    def icon_id(self) -> int:
        """ Decimal identifier of the Icon of the outfit part. """
        return self._icon_id

    @property
    def icon_key(self) -> str:
        """ Decimal identifier of the Icon of the outfit part. """
        return self._icon_key

    @property
    def part_id(self) -> int:
        """ Decimal CAS Part Identifier of the outfit part. """
        return self._part_id

    @property
    def available_for(self) -> OCOutfitPartAvailableFor:
        """ Information on what this part is available for. """
        return self._available_for

    @property
    def part_tags(self) -> Tuple[Tag]:
        """ Tags of the outfit part. """
        return self._part_tags

    @property
    def tag_list(self) -> Tuple[str]:
        """ A collection of tags for the outfit part. """
        tags = list()
        tags.append(self.author)
        for gender in self.available_for.genders:
            split = str(gender).split('.')
            tags.append(split[len(split) - 1])
        for age in self.available_for.ages:
            split = str(age).split('.')
            tags.append(split[len(split) - 1])
        for species in self.available_for.species:
            split = str(species).split('.')
            tags.append(split[len(split) - 1])
        for part_tag in self.part_tags:
            tags.append(str(part_tag))
        return tuple(tags)

    def is_valid(self) -> bool:
        """ Determine if the outfit part is valid or not. """
        return self.part_id != -1 and (self.raw_display_name is not None or self.display_name is not None) and CommonCASUtils.is_cas_part_loaded(self.part_id) and self.available_for.is_valid()

    def __repr__(self) -> str:
        return '<display_name: {}, raw_display_name: {}, author:{}, icon_id {}, part_id:{}, available_for:{}, part_tags:{}>'\
            .format(self.display_name, self.raw_display_name, self.author, self.icon_id, self.part_id, pformat(self.available_for), pformat(self.part_tags))

    def __str__(self) -> str:
        return self.__repr__()
