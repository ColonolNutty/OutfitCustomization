"""
This file is part of the Outfit Customization mod licensed under the Creative Commons Attribution-NonCommercial-NoDerivatives 4.0 International public license (CC BY-NC-ND 4.0).
https://creativecommons.org/licenses/by-nc-nd/4.0/
https://creativecommons.org/licenses/by-nc-nd/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from typing import Tuple

from cnoutfitcustomization.outfit_parts.outfit_part import OCOutfitPart
from cnoutfitcustomization.outfit_parts.outfit_part_loaders.base_cas_part_loader import OCBaseCASPartLoader
from cnoutfitcustomization.outfit_parts.outfit_parts_collection import OCOutfitPartsCollection


class OCOutfitCustomizationCASPartLoader(OCBaseCASPartLoader):
    """ Loads OC Outfit Parts. """

    # noinspection PyMissingOrEmptyDocstring
    @property
    def log_identifier(self) -> str:
        return 'oc_outfit_part_loader_outfit_customization'

    # noinspection PyMissingOrEmptyDocstring
    @property
    def snippet_names(self) -> Tuple[str]:
        result: Tuple[str] = (
            'outfit_parts_list',
        )
        return result

    def _load(self, package_outfit_part_collection: OCOutfitPartsCollection) -> Tuple[OCOutfitPart]:
        cas_parts: Tuple[OCOutfitPart] = (
            *tuple([OCOutfitPart.load_from_package(package_outfit_part, self.log) for package_outfit_part in getattr(package_outfit_part_collection, 'outfit_parts_list', tuple())]),
        )
        return cas_parts
