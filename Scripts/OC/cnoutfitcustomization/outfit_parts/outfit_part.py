"""
This file is part of the Outfit Customization mod licensed under the Creative Commons Attribution-NonCommercial-NoDerivatives 4.0 International public license (CC BY-NC-ND 4.0).
https://creativecommons.org/licenses/by-nc-nd/4.0/
https://creativecommons.org/licenses/by-nc-nd/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from pprint import pformat
from typing import Tuple, Union

from cnoutfitcustomization.outfit_parts.outfit_parts_collection import OCOutfitPartData
from protocolbuffers.Localization_pb2 import LocalizedString
from sims.sim_info_types import Age, Gender
from sims4communitylib.enums.common_species import CommonSpecies
from sims4communitylib.utils.common_log_registry import CommonLog
from sims4communitylib.utils.localization.common_localization_utils import CommonLocalizationUtils
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

    def is_valid(self) -> Tuple[bool, str]:
        """ Determine if available for is valid. """
        if len(self.genders) == 0 and len(self.ages) == 0 and len(self.species) == 0:
            return False, 'Missing genders, ages, or species!'
        return True, 'Success'

    def __repr__(self) -> str:
        return '<genders:{}, ages:{}, species:{}>'\
            .format(pformat(self.genders), pformat(self.ages), pformat(self.species))

    def __str__(self) -> str:
        return self.__repr__()

    # noinspection PyMissingOrEmptyDocstring
    @classmethod
    def load_from_package(
        cls,
        package_outfit_part: 'OCOutfitPartData'
    ) -> Union['OCOutfitPartAvailableFor', None]:
        available_for_genders: Tuple[Gender] = tuple(getattr(package_outfit_part, 'available_for_genders', tuple()))
        available_for_ages: Tuple[Age] = tuple(getattr(package_outfit_part, 'available_for_ages', tuple()))
        available_for_species: Tuple[CommonSpecies] = tuple(getattr(package_outfit_part, 'available_for_species', tuple()))
        return cls(available_for_genders, available_for_ages, available_for_species)


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
        self._unique_identifier = None

    @property
    def unique_identifier(self) -> str:
        """ An identifier that identifies the CAS part in a unique way. """
        if not self._unique_identifier:
            self._unique_identifier = '{}{}{}'.format(self.author, self.name, self.part_id)
            self._unique_identifier = ''.join((ch for ch in self._unique_identifier if ch.isalnum()))
        return self._unique_identifier

    @property
    def display_name(self) -> LocalizedString:
        """ The string display name of the outfit part. """
        return self._display_name

    @property
    def raw_display_name(self) -> str:
        """ The raw text display name of the outfit part. """
        return self._raw_display_name

    @property
    def name(self) -> str:
        """ The name of the outfit part. """
        return str(self.raw_display_name or self.display_name)

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
    def tags(self) -> Tuple[Tag]:
        """ Tags of the outfit part. """
        return self._part_tags

    @property
    def tag_list(self) -> Tuple[str]:
        """ A collection of tags for the outfit part. """
        tags = list()
        tags.append('ALL')
        tags.append(self.author)
        for gender in self.available_for.genders:
            split = str(gender).split('.')
            tags.append(split[len(split) - 1])
        for tag in self.tags:
            tags.append(str(tag))
        return tuple(tags)

    def is_valid(self) -> Tuple[bool, str]:
        """ Determine if the outfit part is valid or not. """
        if self.part_id == -1:
            return False, 'Missing part_id'
        if self.raw_display_name is None and self.display_name is None:
            return False, 'Missing raw_display_name and display_name'
        return self.available_for.is_valid()

    def __repr__(self) -> str:
        return '<display_name: {}, raw_display_name: {}, author:{}, icon_id {}, part_id:{}, available_for:{}, tags:{}>'\
            .format(self.display_name, self.raw_display_name, self.author, self.icon_id, self.part_id, pformat(self.available_for), pformat(self.tags))

    def __str__(self) -> str:
        return self.__repr__()

    # noinspection PyMissingOrEmptyDocstring
    @classmethod
    def load_from_package(
        cls,
        package_outfit_part: 'OCOutfitPartData',
        log: CommonLog
    ) -> Union['OCOutfitPart', None]:
        display_name: LocalizedString = getattr(package_outfit_part, 'part_display_name')
        raw_display_name: str = getattr(package_outfit_part, 'part_raw_display_name')
        if raw_display_name is None:
            log.debug('Outfit part is missing \'raw_display_name\'.')
            return None
        if not display_name:
            display_name = CommonLocalizationUtils.create_localized_string(raw_display_name)
        author: str = getattr(package_outfit_part, 'part_author', None)
        if author is None:
            log.debug('Outfit part missing author name..')
            return None
        icon_id: int = getattr(package_outfit_part, 'part_icon_id', 0)
        part_id: int = getattr(package_outfit_part, 'part_id', -1)
        if part_id is None or part_id < 0:
            log.debug('Outfit part missing part_id.')
            return None
        available_for = OCOutfitPartAvailableFor.load_from_package(package_outfit_part)
        part_tags: Tuple[Tag] = tuple(getattr(package_outfit_part, 'part_tags', tuple()))
        cas_part = cls(
            display_name,
            raw_display_name,
            author,
            icon_id,
            part_id,
            available_for,
            part_tags
        )
        log.format_with_message('Loaded CAS Part.', cas_part=cas_part)
        if not cas_part.is_valid():
            log.debug('Outfit part not valid.')
            return None
        log.debug('Outfit part valid.')
        return cas_part
