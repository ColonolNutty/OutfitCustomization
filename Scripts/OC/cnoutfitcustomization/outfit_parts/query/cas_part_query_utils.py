"""
This file is part of the Outfit Customization mod licensed under the Creative Commons Attribution-NonCommercial-NoDerivatives 4.0 International public license (CC BY-NC-ND 4.0).
https://creativecommons.org/licenses/by-nc-nd/4.0/
https://creativecommons.org/licenses/by-nc-nd/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from typing import Tuple, Set, Iterator

from cnoutfitcustomization.enums.query_type import OCQueryType
from cnoutfitcustomization.modinfo import ModInfo
from cnoutfitcustomization.outfit_parts.outfit_part import OCOutfitPart
from cnoutfitcustomization.outfit_parts.query.cas_part_query import OCCASPartQuery
from cnoutfitcustomization.outfit_parts.tag_filters.cas_part_tag_filter import OCCASPartTagFilter
from cnoutfitcustomization.outfit_parts.tag_filters.sim_filter import OCSimCASPartFilter
from cnoutfitcustomization.outfit_parts.tag_filters.tags_filter import OCTagsCASPartFilter
from sims.sim_info import SimInfo
from sims4communitylib.utils.sims.common_sim_name_utils import CommonSimNameUtils

from sims4communitylib.logging.has_log import HasLog
from sims4communitylib.mod_support.mod_identity import CommonModIdentity


class OCCASPartQueryUtils(HasLog):
    """ Query for CAS parts using various filter configurations. """

    # noinspection PyMissingOrEmptyDocstring
    @property
    def mod_identity(self) -> CommonModIdentity:
        return ModInfo.get_identity()

    # noinspection PyMissingOrEmptyDocstring
    @property
    def log_identifier(self) -> str:
        return 'oc_cas_part_utils'

    def __init__(self) -> None:
        super().__init__()
        from cnoutfitcustomization.outfit_parts.cas_part_query_registry import OCCASPartQueryRegistry
        self.query_registry = OCCASPartQueryRegistry()

    def get_available(self) -> Tuple[OCOutfitPart]:
        """ Get available CAS Parts. """
        return self.query_registry.get_available()

    def has_cas_parts_for_sim(
        self,
        sim_info: SimInfo,
        ignore_cas_parts: Tuple[str]=(),
        additional_tags: Tuple[str]=(),
        additional_filters: Iterator[OCCASPartTagFilter]=()
    ) -> bool:
        """has_cas_parts_for_sim(\
            sim_info,\
            ignore_cas_parts=(),\
            additional_tags=(),\
            additional_filters=()\
        )

        Determine if CAS Parts exist for the criteria.

        :param sim_info: An instance of a Sim
        :type sim_info: SimInfo
        :param additional_tags: Additional tags to add to the query. Default is an empty collection.
        :type additional_tags: Tuple[Any], optional
        :param ignore_cas_parts: A collection of identifiers to ignore. Default is an empty collection.
        :type ignore_cas_parts: Tuple[str], optional
        :param additional_filters: Additional filters. Default is an empty collection.
        :type additional_filters: Iterator[OCCASPartTagFilter], optional.
        :return: True, if CAS Parts exist for the criteria. False, if not.
        :rtype: bool
        """
        self.log.format_with_message(
            'Checking if CAS Parts exist for Sim.',
            sim_name=CommonSimNameUtils.get_full_name(sim_info),
            additional_filters=additional_filters,
            ignore_cas_parts=ignore_cas_parts,
            additional_tags=additional_tags
        )
        filters: Tuple[OCCASPartTagFilter] = (
            OCSimCASPartFilter(sim_info),
            OCTagsCASPartFilter(additional_tags),
            *additional_filters
        )
        # Include Object Tag, Include Category Tag

        queries: Tuple[OCCASPartQuery] = (self.query_registry.create_query(filters, query_type=OCQueryType.ALL_PLUS_ANY),)
        return self.query_registry.has_cas_parts(queries)

    def get_cas_parts_for_sim(
        self,
        sim_info: SimInfo,
        ignore_cas_parts: Tuple[str]=(),
        additional_tags: Tuple[str]=(),
        additional_filters: Iterator[OCCASPartTagFilter]=()
    ) -> Tuple[OCOutfitPart]:
        """get_cas_parts_for_sim(\
            sim_info,\
            ignore_cas_parts=(),\
            additional_tags=(),\
            additional_filters=()\
        )

        Retrieve CAS Parts using the criteria.

        :param sim_info: An instance of a Sim
        :type sim_info: SimInfo
        :param additional_tags: Additional tags to add to the query. Default is an empty collection.
        :type additional_tags: Tuple[Any], optional
        :param ignore_cas_parts: A collection of identifiers to ignore. Default is an empty collection.
        :type ignore_cas_parts: Tuple[str], optional
        :param additional_filters: Additional filters. Default is an empty collection.
        :type additional_filters: Iterator[OCCASPartTagFilter], optional.
        :return: A collection of CAS Parts matching the criteria.
        :rtype: Set[OCOutfitPart]
        """
        self.log.format_with_message(
            'Get CAS Parts for Sim.',
            sim_name=CommonSimNameUtils.get_full_name(sim_info),
            additional_filters=tuple(additional_filters),
            ignore_cas_parts=ignore_cas_parts,
            additional_tags=additional_tags
        )
        filters: Tuple[OCCASPartTagFilter] = (
            OCSimCASPartFilter(sim_info),
            OCTagsCASPartFilter(additional_tags),
            *tuple(additional_filters)
        )
        # Include Object Tag, Include Category Tag

        queries: Tuple[OCCASPartQuery] = (self.query_registry.create_query(filters, query_type=OCQueryType.ALL_PLUS_ANY),)
        return tuple(self.query_registry.get_cas_parts(queries))
