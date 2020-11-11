"""
This file is part of the Outfit Customization mod licensed under the Creative Commons Attribution-NonCommercial-NoDerivatives 4.0 International public license (CC BY-NC-ND 4.0).
https://creativecommons.org/licenses/by-nc-nd/4.0/
https://creativecommons.org/licenses/by-nc-nd/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from typing import Tuple, Union, Any

from cnoutfitcustomization.queries.query_tag import OCQueryTag


class OCTagFilter:
    """ A filter for use when querying. """
    def __init__(self, match_all_tags: bool, exclude_tags: bool=False, tag_type: Any=None):
        self._match_all_tags = match_all_tags
        self._exclude_tags = exclude_tags
        self._tag_type = tag_type

    @property
    def tag_type(self) -> Union[Any, None]:
        """ The type of tags the filter uses. """
        return self._tag_type

    @property
    def match_all_tags(self) -> bool:
        """ Determine if an animation must match all (True) of this filters tags or any (False) of them. """
        return self._match_all_tags

    @property
    def exclude_tags(self) -> bool:
        """ Determine if an animation must not have any of the tags. """
        return self._exclude_tags

    def get_tags(self) -> Tuple[OCQueryTag]:
        """ Retrieve the tags of this filter. """
        return tuple()

    def __repr__(self) -> str:
        return self.__str__()

    def __str__(self) -> str:
        return str(self._tag_type)
