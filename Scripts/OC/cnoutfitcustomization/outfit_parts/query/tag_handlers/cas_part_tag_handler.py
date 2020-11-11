"""
This file is part of the Outfit Customization mod licensed under the Creative Commons Attribution-NonCommercial-NoDerivatives 4.0 International public license (CC BY-NC-ND 4.0).
https://creativecommons.org/licenses/by-nc-nd/4.0/
https://creativecommons.org/licenses/by-nc-nd/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from typing import Any, Tuple

from cnoutfitcustomization.outfit_parts.cas_part_tag_type import OCCASPartTagType
from cnoutfitcustomization.outfit_parts.outfit_part import OCOutfitPart
from cnoutfitcustomization.queries.tag_handler import OCTagHandler


class OCCASPartTagHandler(OCTagHandler):
    """ A filter for CAS Parts. """
    def __init__(self, tag_type: OCCASPartTagType):
        super().__init__(tag_type)

    # noinspection PyMissingOrEmptyDocstring
    @property
    def tag_type(self) -> OCCASPartTagType:
        return super().tag_type

    # noinspection PyMissingOrEmptyDocstring
    def get_tags(self, cas_part: OCOutfitPart) -> Tuple[Any]:
        return super().get_tags(cas_part)

    # noinspection PyMissingOrEmptyDocstring
    def applies(self, cas_part: OCOutfitPart) -> bool:
        return super().applies(cas_part)
