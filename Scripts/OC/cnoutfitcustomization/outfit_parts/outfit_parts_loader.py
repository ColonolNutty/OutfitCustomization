"""
This file is part of the Outfit Customization mod licensed under the Creative Commons Attribution-NonCommercial-NoDerivatives 4.0 International public license (CC BY-NC-ND 4.0).
https://creativecommons.org/licenses/by-nc-nd/4.0/
https://creativecommons.org/licenses/by-nc-nd/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from typing import Iterator, Tuple, List, Union

from cnoutfitcustomization.modinfo import ModInfo
from cnoutfitcustomization.outfit_parts.outfit_parts_collection import OCOutfitPartData
from sims.sim_info_types import Age, Gender
from sims4.resources import Types
from protocolbuffers.Localization_pb2 import LocalizedString
from cnoutfitcustomization.outfit_parts.outfit_part import OCOutfitPart, OCOutfitPartAvailableFor
from sims4communitylib.enums.common_species import CommonSpecies
from sims4communitylib.events.event_handling.common_event_registry import CommonEventRegistry
from sims4communitylib.events.zone_spin.events.zone_late_load import S4CLZoneLateLoadEvent
from sims4communitylib.services.common_service import CommonService
from sims4communitylib.utils.common_log_registry import CommonLogRegistry
from sims4communitylib.utils.common_resource_utils import CommonResourceUtils
from sims4communitylib.utils.localization.common_localization_utils import CommonLocalizationUtils
from tag import Tag

log = CommonLogRegistry.get().register_log(ModInfo.get_identity().name, 'oc_outfit_parts_loader')


class OCOutfitPartsLoader(CommonService):
    """ Loads OCOutfitParts from snippet files in packages. """
    def __init__(self: 'OCOutfitPartsLoader'):
        self._loaded_outfit_parts: List[OCOutfitPart] = []

    def _load_outfit_part(self, outfit_part_data: OCOutfitPartData) -> Union[OCOutfitPart, None]:
        display_name: LocalizedString = getattr(outfit_part_data, 'part_display_name')
        raw_display_name: str = getattr(outfit_part_data, 'part_raw_display_name')
        if raw_display_name is None:
            log.debug('Outfit part is missing \'raw_display_name\'.')
            return None
        if not display_name:
            display_name = CommonLocalizationUtils.create_localized_string(raw_display_name)
        author: str = str(getattr(outfit_part_data, 'part_author'))
        icon_id: int = getattr(outfit_part_data, 'part_icon_id')
        part_id: int = getattr(outfit_part_data, 'part_id')
        available_for_genders: Tuple[Gender] = tuple(getattr(outfit_part_data, 'available_for_genders'))
        available_for_ages: Tuple[Age] = tuple(getattr(outfit_part_data, 'available_for_ages'))
        available_for_species: Tuple[CommonSpecies] = tuple(getattr(outfit_part_data, 'available_for_species'))
        available_for = OCOutfitPartAvailableFor(available_for_genders, available_for_ages, available_for_species)
        part_tags: Tuple[Tag] = tuple(getattr(outfit_part_data, 'part_tags'))
        outfit_part = OCOutfitPart(display_name, raw_display_name, author, icon_id, part_id, available_for, part_tags)
        log.format_with_message('Loading outfit part.', outfit_part=outfit_part)
        if not outfit_part.is_valid():
            log.debug('Outfit part not valid.')
            return None
        log.debug('Outfit part valid.')
        return outfit_part

    def _load_outfit_parts_from_packages_gen(self) -> Iterator[OCOutfitPart]:
        log.debug('Loading outfit parts from packages.')
        outfit_part_collections = CommonResourceUtils.load_instances_with_any_tags(Types.SNIPPET, ('outfit_parts_list',))
        for outfit_part_collection in outfit_part_collections:
            for outfit_part_data in outfit_part_collection.outfit_parts_list:
                outfit_part = self._load_outfit_part(outfit_part_data)
                if outfit_part is None:
                    continue
                yield outfit_part

    def get_loaded_outfit_parts(self) -> Tuple[OCOutfitPart]:
        """ Retrieve loaded outfit parts. """
        if self._loaded_outfit_parts is None or len(self._loaded_outfit_parts) == 0:
            self._initialize_outfit_parts()
        return tuple(self._loaded_outfit_parts)

    def _initialize_outfit_parts(self) -> Tuple[OCOutfitPart]:
        """ Initialize outfit parts. """
        log.debug('Initializing outfit parts.')
        outfit_parts_list = []
        outfit_parts = self._load_outfit_parts_from_packages_gen()
        for outfit_part in outfit_parts:
            outfit_parts_list.append(outfit_part)
        self._loaded_outfit_parts = outfit_parts_list
        return tuple(outfit_parts_list)

    def add_outfit_part_with_id(
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
        """ Add an outfit part. """
        self._loaded_outfit_parts.append(OCOutfitPart(display_name, raw_display_name, author, icon_id, part_id, available_for, part_tags, icon_key=icon_key))

    @staticmethod
    @CommonEventRegistry.handle_events(ModInfo.get_identity().name)
    def _oc_load_outfit_parts_on_zone_load(event_data: S4CLZoneLateLoadEvent):
        if event_data.game_loaded:
            return
        OCOutfitPartsLoader.get()._initialize_outfit_parts()
