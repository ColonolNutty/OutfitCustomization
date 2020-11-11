"""
This file is part of the Outfit Customization mod licensed under the Creative Commons Attribution-NonCommercial-NoDerivatives 4.0 International public license (CC BY-NC-ND 4.0).
https://creativecommons.org/licenses/by-nc-nd/4.0/
https://creativecommons.org/licenses/by-nc-nd/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from typing import Iterator, Tuple

from cnoutfitcustomization.outfit_parts.cas_part_query_tag import OCCASPartQueryTag
from cnoutfitcustomization.outfit_parts.cas_part_tag_type import OCCASPartTagType
from cnoutfitcustomization.outfit_parts.tag_filters.cas_part_tag_filter import OCCASPartTagFilter


class OCTagsCASPartFilter(OCCASPartTagFilter):
    """ Filter CAS Parts by Tags. """
    def __init__(self, tags: Iterator[str], match_all_tags: bool=False, exclude_tags: bool=False):
        super().__init__(match_all_tags, exclude_tags=exclude_tags, tag_type=OCCASPartTagType.CUSTOM_TAG)
        self._tags = tags

    # noinspection PyMissingOrEmptyDocstring
    def get_tags(self) -> Tuple[OCCASPartQueryTag]:
        return tuple([OCCASPartQueryTag(self.tag_type, tag) for tag in self._tags])

    def __str__(self) -> str:
        return '{}: {}'.format(
            self.__class__.__name__,
            self._tags
        )
