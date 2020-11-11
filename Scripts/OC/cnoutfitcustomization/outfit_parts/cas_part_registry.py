"""
This file is part of the Outfit Customization mod licensed under the Creative Commons Attribution-NonCommercial-NoDerivatives 4.0 International public license (CC BY-NC-ND 4.0).
https://creativecommons.org/licenses/by-nc-nd/4.0/
https://creativecommons.org/licenses/by-nc-nd/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from typing import Tuple, Iterator, List, Dict

from cnoutfitcustomization.modinfo import ModInfo
from cnoutfitcustomization.outfit_parts.outfit_part import OCOutfitPart
from cnoutfitcustomization.outfit_parts.outfit_part_loaders.base_cas_part_loader import OCBaseCASPartLoader
from sims4communitylib.events.event_handling.common_event_registry import CommonEventRegistry
from sims4communitylib.events.zone_spin.events.zone_early_load import S4CLZoneEarlyLoadEvent
from sims4communitylib.logging.has_log import HasLog
from sims4communitylib.mod_support.mod_identity import CommonModIdentity
from sims4communitylib.services.common_service import CommonService
from sims4communitylib.utils.cas.common_cas_utils import CommonCASUtils

from sims4.commands import Command, CommandType, CheatOutput


class OCCASPartRegistry(CommonService, HasLog):
    """ A registry containing cas parts. """

    def __init__(self) -> None:
        super().__init__()
        self._loaded = False
        self._cas_part_collection = None
        from cnoutfitcustomization.outfit_parts.outfit_part_loaders.outfit_customization_cas_part_loader import \
            OCOutfitCustomizationCASPartLoader
        self._cas_part_loaders: List[OCBaseCASPartLoader] = list((
            OCOutfitCustomizationCASPartLoader(),
        ))

    # noinspection PyMissingOrEmptyDocstring
    @property
    def mod_identity(self) -> CommonModIdentity:
        return ModInfo.get_identity()

    # noinspection PyMissingOrEmptyDocstring
    @property
    def log_identifier(self) -> str:
        return 'oc_cas_part_registry'

    @property
    def cas_part_collection(self) -> List[OCOutfitPart]:
        """ A collection of loaded cas parts. """
        if self._cas_part_collection is None:
            self._cas_part_collection = list(self._load())
        return self._cas_part_collection

    @cas_part_collection.setter
    def cas_part_collection(self, value: Tuple[OCOutfitPart]):
        self._cas_part_collection = value

    @property
    def cas_part_loaders(self) -> List[OCBaseCASPartLoader]:
        """ Loaders that load CAS Parts. """
        return self._cas_part_loaders

    @classmethod
    def add_cas_part_loader(cls, cas_part_loader: OCBaseCASPartLoader) -> bool:
        """ Add a loader. """
        cas_part_registry = cls()
        if cas_part_loader in cas_part_registry.cas_part_loaders:
            return False
        cas_part_registry.cas_part_loaders.append(cas_part_loader)
        return True

    def add_cas_part(self, cas_part: OCOutfitPart) -> bool:
        """add_cas_part(cas_part)

        Add a CAS Part to the registry.

        :param cas_part: An instance of a CAS Part
        :type cas_part: OCOutfitPart
        :return: True, if the part was successfully added. False, if not.
        :rtype: bool
        """
        if cas_part in self.cas_part_collection:
            return False
        self.cas_part_collection.append(cas_part)
        return True

    def _load(self) -> Iterator[OCOutfitPart]:
        for cas_part_loader in self.cas_part_loaders:
            for cas_part in cas_part_loader.load():
                yield cas_part

    def collect(
        self,
        collect_all: bool=True,
        collect_available: bool=True
    ) -> Tuple[Tuple[OCOutfitPart], Tuple[OCOutfitPart], Dict[str, OCOutfitPart]]:
        """ Collect CAS Parts. """
        try:
            self.log.debug('Collecting CAS Parts...')
            all_list: List[OCOutfitPart] = []
            available_list: List[OCOutfitPart] = []
            available_identifiers_list: Dict[str, OCOutfitPart] = {}
            data_list: Tuple[OCOutfitPart] = self._cas_part_collection
            for cas_part_data in data_list:
                if collect_all:
                    all_list.append(cas_part_data)
                if collect_available:
                    available_list.append(cas_part_data)
                    available_identifiers_list[cas_part_data.unique_identifier] = cas_part_data
            self.log.debug('Done sorting CAS Parts')

            if collect_all:
                self.log.debug('Has All CAS Parts.')
                author_names = set()
                for cas_part_data in all_list:
                    if cas_part_data.author not in author_names:
                        author_names.add(cas_part_data.author)
                author_names = list(author_names)
                author_names.sort()
                author_names = dict([(author_name, author_names.index(author_name)) for author_name in author_names])
                for cas_part_data in all_list:
                    cas_part_data.author_index = author_names[cas_part_data.author]
                all_list.sort(key=lambda x: x.author_index)
                for (index, cas_part_data) in enumerate(all_list):
                    cas_part_data: OCOutfitPart = cas_part_data
                    cas_part_data.cas_part_index = index
                self.log.debug('Collected all CAS Parts.')
            if collect_available:
                self.log.debug('Has available CAS Parts.')
                available_list.sort(key=lambda x: x.author_index)
                self.log.debug('Collected all available CAS Parts.')
            self.log.debug('Done collecting CAS Parts.')
            return tuple(all_list), tuple(available_list), available_identifiers_list
        except Exception as ex:
            self.log.error('Error while collecting CAS Parts.', exception=ex)
            return tuple(), tuple(), dict()

    @staticmethod
    @CommonEventRegistry.handle_events(ModInfo.get_identity())
    def _load_cas_parts_on_zone_load(event_data: S4CLZoneEarlyLoadEvent) -> bool:
        if event_data.game_loaded:
            # If the game is already loaded, we've already loaded the data once.
            return False
        if not OCCASPartRegistry().cas_part_collection is None:
            return False
        return True


@Command('oc.show_cas_parts', command_type=CommandType.Live)
def _oc_show_cas_parts(_connection: int=None):
    output = CheatOutput(_connection)
    output('Showing loaded CAS Parts')
    OCCASPartRegistry().log.enable()
    for cas_part in OCCASPartRegistry().cas_part_collection:
        OCCASPartRegistry().log.debug(repr(cas_part))
    OCCASPartRegistry().log.disable()
    output('Done showing loaded CAS Parts.')


@Command('oc.is_cas_part_loaded', command_type=CommandType.Live)
def _oc_is_cas_part_loaded(part_id: int=None, _connection: int=None):
    output = CheatOutput(_connection)
    if part_id is None:
        output('No CAS Part specified!')
        return
    output('Checking if CAS Part {} is loaded.'.format(part_id))
    if CommonCASUtils.is_cas_part_loaded(part_id):
        output('CAS Part is loaded.')
    else:
        output('CAS Part is not loaded.')
