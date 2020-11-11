"""
This file is part of the Outfit Customization mod licensed under the Creative Commons Attribution-NonCommercial-NoDerivatives 4.0 International public license (CC BY-NC-ND 4.0).
https://creativecommons.org/licenses/by-nc-nd/4.0/
https://creativecommons.org/licenses/by-nc-nd/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from typing import Tuple

from cnoutfitcustomization.enums.query_type import OCQueryType
from cnoutfitcustomization.outfit_parts.cas_part_query_tag import OCCASPartQueryTag
from cnoutfitcustomization.outfit_parts.tag_filters.cas_part_tag_filter import OCCASPartTagFilter
from cnoutfitcustomization.queries.query import OCQuery


class OCCASPartQuery(OCQuery):
    """ A query used to locate animations. """
    def __init__(
        self,
        filters: Tuple[OCCASPartTagFilter],
        query_type: OCQueryType=OCQueryType.ALL_PLUS_ANY
    ):
        super().__init__(filters, query_type)

    # noinspection PyMissingOrEmptyDocstring
    @property
    def include_all_tags(self) -> Tuple[OCCASPartQueryTag]:
        result: Tuple[OCCASPartQueryTag] = super().include_all_tags
        return result

    # noinspection PyMissingOrEmptyDocstring
    @property
    def include_any_tags(self) -> Tuple[OCCASPartQueryTag]:
        result: Tuple[OCCASPartQueryTag] = super().include_any_tags
        return result

    # noinspection PyMissingOrEmptyDocstring
    @property
    def exclude_tags(self) -> Tuple[OCCASPartQueryTag]:
        result: Tuple[OCCASPartQueryTag] = super().exclude_tags
        return result
