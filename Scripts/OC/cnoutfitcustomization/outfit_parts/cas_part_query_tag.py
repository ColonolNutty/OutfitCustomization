"""
This file is part of the Outfit Customization mod licensed under the Creative Commons Attribution-NonCommercial-NoDerivatives 4.0 International public license (CC BY-NC-ND 4.0).
https://creativecommons.org/licenses/by-nc-nd/4.0/
https://creativecommons.org/licenses/by-nc-nd/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from typing import Any, Tuple

from cnoutfitcustomization.outfit_parts.cas_part_tag_type import OCCASPartTagType
from cnoutfitcustomization.queries.query_tag import OCQueryTag


class OCCASPartQueryTag(OCQueryTag):
    """ A query tag. """
    def __init__(self, tag_type: OCCASPartTagType, value: Any):
        super().__init__(tag_type, value)

    # noinspection PyMissingOrEmptyDocstring
    @property
    def tag_type(self) -> OCCASPartTagType:
        return super().tag_type

    # noinspection PyMissingOrEmptyDocstring
    @property
    def key(self) -> Tuple[OCCASPartTagType, Any]:
        return super().key
