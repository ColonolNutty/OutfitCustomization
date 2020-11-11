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


class OCCustomTagsCASPartFilter(OCCASPartTagFilter):
    """ Used to specify tags for filtering. """
    def __init__(self, tags: Tuple[OCCASPartQueryTag], match_all_tags: bool=False, exclude_tags: bool=False):
        super().__init__(match_all_tags, exclude_tags=exclude_tags, tag_type=OCCASPartTagType.CUSTOM_TAG)
        self._custom_tags = tags

    # noinspection PyMissingOrEmptyDocstring
    def get_tags(self) -> Tuple[OCCASPartQueryTag]:
        return self._custom_tags

    def __str__(self) -> str:
        return '{}: {}'.format(
            self.__class__.__name__,
            self._custom_tags
        )
