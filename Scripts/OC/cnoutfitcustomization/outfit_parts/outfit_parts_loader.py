"""
This file is part of the Outfit Customization mod licensed under the Creative Commons Attribution-NonCommercial-NoDerivatives 4.0 International public license (CC BY-NC-ND 4.0).
https://creativecommons.org/licenses/by-nc-nd/4.0/
https://creativecommons.org/licenses/by-nc-nd/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from typing import Iterator, Tuple, List, Any

from cnoutfitcustomization.modinfo import ModInfo
from sims4.resources import Types
from protocolbuffers.Localization_pb2 import LocalizedString
from cnoutfitcustomization.outfit_parts.outfit_part import OCOutfitPart, OCOutfitPartAvailableFor
from sims4communitylib.logging.has_log import HasLog
from sims4communitylib.mod_support.mod_identity import CommonModIdentity
from sims4communitylib.services.common_service import CommonService
from sims4communitylib.utils.common_resource_utils import CommonResourceUtils


class OCOutfitPartsLoader(CommonService, HasLog):
    """ Loads CAS Parts from snippet files in packages. """

    # noinspection PyMissingOrEmptyDocstring
    @property
    def mod_identity(self) -> CommonModIdentity:
        return ModInfo.get_identity()

    # noinspection PyMissingOrEmptyDocstring
    @property
    def log_identifier(self) -> str:
        return 'oc_outfit_parts_loader'

    def __init__(self) -> None:
        super().__init__()
        self._loaded_outfit_parts: List[OCOutfitPart] = []

    def _load_outfit_parts_from_packages_gen(self) -> Iterator[OCOutfitPart]:
        self.log.debug('Loading outfit parts from packages.')
        outfit_part_collections = CommonResourceUtils.load_instances_with_any_tags(Types.SNIPPET, ('outfit_parts_list',))
        for outfit_part_collection in outfit_part_collections:
            for package_outfit_part in outfit_part_collection.outfit_parts_list:
                outfit_part = OCOutfitPart.load_from_package(package_outfit_part, self.log)
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
        self.log.debug('Initializing outfit parts.')
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
        part_tags: Tuple[Any],
        icon_key: str=None
    ):
        """ Add an outfit part. """
        self._loaded_outfit_parts.append(OCOutfitPart(display_name, raw_display_name, author, icon_id, part_id, available_for, part_tags, icon_key=icon_key))
