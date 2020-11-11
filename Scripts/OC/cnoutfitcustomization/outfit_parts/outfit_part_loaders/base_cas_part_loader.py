"""
This file is part of the Outfit Customization mod licensed under the Creative Commons Attribution-NonCommercial-NoDerivatives 4.0 International public license (CC BY-NC-ND 4.0).
https://creativecommons.org/licenses/by-nc-nd/4.0/
https://creativecommons.org/licenses/by-nc-nd/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from typing import Tuple, Iterator, Any

from cnoutfitcustomization.modinfo import ModInfo
from cnoutfitcustomization.outfit_parts.outfit_part import OCOutfitPart
from sims4.resources import Types
from sims4communitylib.exceptions.common_exceptions_handler import CommonExceptionHandler
from sims4communitylib.logging.has_log import HasLog
from sims4communitylib.mod_support.mod_identity import CommonModIdentity
from sims4communitylib.services.common_service import CommonService
from sims4communitylib.utils.cas.common_cas_utils import CommonCASUtils
from sims4communitylib.utils.common_resource_utils import CommonResourceUtils


class OCBaseCASPartLoader(CommonService, HasLog):
    """ Loads Outfit Parts. """
    # noinspection PyMissingOrEmptyDocstring
    @property
    def mod_identity(self) -> CommonModIdentity:
        return ModInfo.get_identity()

    # noinspection PyMissingOrEmptyDocstring
    @property
    def log_identifier(self) -> str:
        return 'oc_outfit_part_loader'

    @property
    def snippet_names(self) -> Tuple[str]:
        """ The names of snippets containing Outfit Parts. """
        raise NotImplementedError()

    @CommonExceptionHandler.catch_exceptions(ModInfo.get_identity(), fallback_return=tuple())
    def load(self) -> Iterator[OCOutfitPart]:
        """load()

        Loads all CAS parts.

        :return: An iterable of CAS parts.
        :rtype: Iterator[OCOutfitPart]
        """
        snippet_names: Tuple[str] = self.snippet_names

        for cas_part_package in CommonResourceUtils.load_instances_with_any_tags(Types.SNIPPET, snippet_names):
            try:
                cas_parts: Tuple[OCOutfitPart] = tuple(self._load(cas_part_package))

                for outfit_part in cas_parts:
                    outfit_part: OCOutfitPart = outfit_part
                    if outfit_part is None:
                        continue
                    (is_valid_result, is_valid_reason) = outfit_part.is_valid()
                    if is_valid_result:
                        yield outfit_part
                    else:
                        if outfit_part.part_id != -1 and not CommonCASUtils.is_cas_part_loaded(outfit_part.part_id):
                            continue
                        self.log.error('Outfit Part \'{}\' by \'{}\' is not valid. Reason: {}'.format(outfit_part.name, outfit_part.author, is_valid_reason), throw=False)
            except Exception as ex:
                self.log.format_error('Error while parsing outfit parts from \'{}\''.format(cas_part_package), exception=ex)

    def _load(self, package_outfit_parts: Any) -> Tuple[OCOutfitPart]:
        raise NotImplementedError()
