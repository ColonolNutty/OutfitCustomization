"""
This file is part of the Outfit Customization mod licensed under the Creative Commons Attribution-NonCommercial-NoDerivatives 4.0 International public license (CC BY-NC-ND 4.0).
https://creativecommons.org/licenses/by-nc-nd/4.0/
https://creativecommons.org/licenses/by-nc-nd/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
import sims4.log
import sims4.reload
import sims4.resources
from typing import Tuple
from cnoutfitcustomization.modinfo import ModInfo
from cnoutfitcustomization.outfit_parts.outfit_part import OCOutfitPartAvailableFor
from cnoutfitcustomization.outfit_parts.outfit_parts_loader import OCOutfitPartsLoader
from protocolbuffers import Dialog_pb2
from sims.outfits.outfit_enums import BodyType
from sims.sim_info_types import Gender, Age
from sims4.resources import Types
from sims4communitylib.enums.common_species import CommonSpecies
from sims4communitylib.exceptions.common_exceptions_handler import CommonExceptionHandler
from sims4communitylib.utils.cas.common_cas_utils import CommonCASUtils
from sims4communitylib.utils.common_log_registry import CommonLogRegistry
from sims4.commands import Command, CommandType, CheatOutput
from sims4communitylib.utils.localization.common_localization_utils import CommonLocalizationUtils

log = CommonLogRegistry.get().register_log(ModInfo.get_identity().name, 'oc_load_vanilla_cas_parts')


@Command('oc.load_vanilla_cas_parts', command_type=CommandType.Live)
def _oc_load_vanilla_cas_parts(_connection=None):
    output = CheatOutput(_connection)
    try:
        output('Loading')
        # noinspection PyUnresolvedReferences
        cas_part_resource_keys = list(sims4.resources.list(type=Types.CASPART))
        for key in cas_part_resource_keys:
            cas_part_id = key.instance
            body_type = CommonCASUtils.get_body_type_of_cas_part(cas_part_id)
            if body_type not in BodyType:
                continue
            log.format_with_message('Loading cas part into OC.', cas_part_id=cas_part_id)
            available_for_genders: Tuple[Gender] = (Gender.MALE, Gender.FEMALE)
            available_for_ages: Tuple[Age] = (Age.TEEN, Age.YOUNGADULT, Age.ADULT, Age.ELDER)
            available_for_species: Tuple[CommonSpecies] = (CommonSpecies.HUMAN,)
            available_for = OCOutfitPartAvailableFor(available_for_genders, available_for_ages, available_for_species)
            OCOutfitPartsLoader.get().add_outfit_part_with_id(CommonLocalizationUtils.create_localized_string(str(cas_part_id)), str(cas_part_id), 'Maxis', key, cas_part_id, available_for, tuple(), icon_key=key)

    except Exception as ex:
        CommonExceptionHandler.log_exception(ModInfo.get_identity().name, 'Problem.', exception=ex)
    output('Done.')


@Command('oc.print', command_type=CommandType.Live)
def _oc_print(_connection=None):
    output = CheatOutput(_connection)
    try:
        log.enable()
        output('Printing')
        log.format(things=dir(Dialog_pb2.UiDialogMessage))
        log.disable()
    except Exception as ex:
        CommonExceptionHandler.log_exception(ModInfo.get_identity().name, 'Problem.', exception=ex)
    output('Done.')
