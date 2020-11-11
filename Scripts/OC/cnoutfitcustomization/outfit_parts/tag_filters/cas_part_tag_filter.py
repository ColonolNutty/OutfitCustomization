"""
This file is part of the Outfit Customization mod licensed under the Creative Commons Attribution-NonCommercial-NoDerivatives 4.0 International public license (CC BY-NC-ND 4.0).
https://creativecommons.org/licenses/by-nc-nd/4.0/
https://creativecommons.org/licenses/by-nc-nd/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from typing import Tuple, Union

from cnoutfitcustomization.outfit_parts.cas_part_query_tag import OCCASPartQueryTag
from cnoutfitcustomization.outfit_parts.cas_part_tag_type import OCCASPartTagType
from cnoutfitcustomization.queries.tag_filter import OCTagFilter


class OCCASPartTagFilter(OCTagFilter):
    """ A filter for use when querying CAS parts. """
    def __init__(self, match_all_tags: bool, exclude_tags: bool=False, tag_type: OCCASPartTagType=None):
        super().__init__(match_all_tags, exclude_tags=exclude_tags, tag_type=tag_type)

    # noinspection PyMissingOrEmptyDocstring
    @property
    def tag_type(self) -> Union[OCCASPartTagType, None]:
        return super().tag_type

    # noinspection PyMissingOrEmptyDocstring
    def get_tags(self) -> Tuple[OCCASPartQueryTag]:
        result: Tuple[OCCASPartQueryTag] = super().get_tags()
        return result
