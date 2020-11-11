"""
This file is part of the Outfit Customization mod licensed under the Creative Commons Attribution-NonCommercial-NoDerivatives 4.0 International public license (CC BY-NC-ND 4.0).
https://creativecommons.org/licenses/by-nc-nd/4.0/
https://creativecommons.org/licenses/by-nc-nd/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from typing import Tuple, Any

from cnoutfitcustomization.outfit_parts.cas_part_query_registry import OCCASPartQueryRegistry
from cnoutfitcustomization.outfit_parts.cas_part_tag_type import OCCASPartTagType
from cnoutfitcustomization.outfit_parts.outfit_part import OCOutfitPart
from cnoutfitcustomization.outfit_parts.query.tag_handlers.cas_part_tag_handler import OCCASPartTagHandler


@OCCASPartQueryRegistry.register_tag_handler(filter_type=OCCASPartTagType.CUSTOM_TAG)
class OCCustomTagsCASPartTagHandler(OCCASPartTagHandler):
    """ Tags. """

    # noinspection PyMissingOrEmptyDocstring
    def get_tags(self, cas_part: OCOutfitPart) -> Tuple[Any]:
        return tuple(cas_part.tags)

    # noinspection PyMissingOrEmptyDocstring
    def applies(self, cas_part: OCOutfitPart) -> bool:
        return len(cas_part.tags) > 0
