from typing import Union, Tuple

from cnoutfitcustomization.modinfo import ModInfo
from cnoutfitcustomization.outfit_parts.outfit_part import OCOutfitPartAvailableFor
from cnoutfitcustomization.outfit_parts.outfit_parts_loader import OCOutfitPartsLoader
from protocolbuffers import Dialog_pb2
from sims.outfits.outfit_enums import BodyType
from sims.sim_info_types import Gender, Age
from sims4.resources import Types
from sims4communitylib.dialogs.choose_object_dialog import CommonChooseObjectDialog
from sims4communitylib.enums.common_species import CommonSpecies
from sims4communitylib.exceptions.common_exceptions_handler import CommonExceptionHandler
from sims4communitylib.utils.cas.common_cas_utils import CommonCASUtils
from sims4communitylib.utils.common_injection_utils import CommonInjectionUtils
from sims4communitylib.utils.common_log_registry import CommonLogRegistry
from sims4.commands import Command, CommandType, CheatOutput
import sims4.log
import sims4.reload
import sims4.resources
from sims4communitylib.utils.localization.common_localization_utils import CommonLocalizationUtils
from sims4communitylib.utils.sims.common_sim_utils import CommonSimUtils
from ui.ui_dialog_picker import ObjectPickerType, ObjectPickerRow, UiObjectPicker, UiDialogObjectPicker

log = CommonLogRegistry.get().register_log(ModInfo.MOD_NAME, 'temp_thingy')
# log.enable()


#@CommonInjectionUtils.inject_into(TunableCasPart, TunableCasPart.load_etree_node.__name__)
def _oc_temp_thing(original, self, node, source, expect_error):
    log.format(original=original, me=self, node=node, source=source, expect_error=expect_error)
    if source is not None and hasattr(source, 's'):
        log.format(source_str=source.s, source_argles=source.args)
    log.format(node_type=type(node), node_cls=node.__class__, node_cls_name=node.__class__.__name__)
    for child_node in node:
        log.format(child_node=child_node)
    return original(self, node, source, expect_error)


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
        CommonExceptionHandler.log_exception(ModInfo.MOD_NAME, 'Problem.', exception=ex)
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
        CommonExceptionHandler.log_exception(ModInfo.MOD_NAME, 'Problem.', exception=ex)
    output('Done.')

@CommonInjectionUtils.inject_into(UiDialogObjectPicker, UiDialogObjectPicker.add_row.__name__)
def _do_it(original, self, row):
    log.format(row=row, row_dir=row)
    return original(self, row)

import math
from interactions import ParticipantTypeSingle, ParticipantTypeSingleSim
from objects.slots import SlotType
from sims4.localization import TunableLocalizedStringFactoryVariant, NULL_LOCALIZED_STRING_FACTORY
from sims4.math import MAX_INT16
from sims4.tuning.tunable import TunableEnumEntry, OptionalTunable, Tunable, TunableVariant, HasTunableSingletonFactory, AutoFactoryInit, TunableRange, TunableReference, TunableSet
import enum
import services
import sims4.log


class OCUiDialogObjectPicker(UiDialogObjectPicker):
    def build_msg(self, **kwargs):
        msg = super().build_msg(**kwargs)
        log.format(msg_dir=dir(msg))
        msg.dialog_type = Dialog_pb2.UiDialogMessage.OBJECT_PICKER
        msg.picker_data = self.build_object_picker()
        return msg

    def _build_customize_picker(self, picker_data):
        raise NotImplementedError

    def build_object_picker(self):
        picker_data = Dialog_pb2.UiDialogPicker()
        log.format(picker_data_dir=dir(picker_data))
        picker_data.title = self._build_localized_string_msg(self.title)
        if self.picker_type is not None:
            picker_data.type = Dialog_pb2.UiDialogPicker.OBJECT
        picker_data.min_selectable = self.min_selectable
        if isinstance(self.max_selectable, int):
            picker_data_max_selectable = self.max_selectable
        else:
            picker_data_max_selectable = self.max_selectable.get_max_selectable(self, self._resolver)
        if picker_data_max_selectable is not None:
            picker_data.max_selectable = picker_data_max_selectable
        picker_data.owner_sim_id = self.owner.sim_id
        if self.target_sim is not None:
            picker_data.target_sim_id = self.target_sim.sim_id
        self.max_selectable_num = picker_data.max_selectable
        picker_data.is_sortable = self.is_sortable
        picker_data.use_dropdown_filter = self.use_dropdown_filter
        picker_data.description_display = self.row_description_display
        self._build_customize_picker(picker_data)
        return picker_data


class OCUiObjectPicker(OCUiDialogObjectPicker):

    class UiObjectPickerObjectPickerType(enum.Int):
        INTERACTION = ObjectPickerType.INTERACTION
        OBJECT = ObjectPickerType.OBJECT
        PIE_MENU = ObjectPickerType.PIE_MENU
        OBJECT_LARGE = ObjectPickerType.OBJECT_LARGE
        OBJECT_SQUARE = ObjectPickerType.OBJECT_SQUARE

    FACTORY_TUNABLES = {'picker_type': TunableEnumEntry(description='\n            Object picker type for the picker dialog.\n            ', tunable_type=UiObjectPickerObjectPickerType, default=UiObjectPickerObjectPickerType.OBJECT)}

    def _validate_row(self, row):
        return isinstance(row, ObjectPickerRow)

    def _build_customize_picker(self, picker_data):
        for row in self.picker_rows:
            row_data = picker_data.object_picker_data.row_data.add()
            row.populate_protocol_buffer(row_data)


class OCCommonChooseObjectDialog(CommonChooseObjectDialog):
    @CommonExceptionHandler.catch_exceptions(ModInfo.MOD_NAME, fallback_return=None)
    def _create_dialog(
        self,
        picker_type: UiObjectPicker.UiObjectPickerObjectPickerType=UiObjectPicker.UiObjectPickerObjectPickerType.OBJECT
    ) -> Union[UiObjectPicker, None]:
        return OCUiObjectPicker.TunableFactory().default(
            CommonSimUtils.get_active_sim_info(),
            text=lambda *_, **__: self.description,
            title=lambda *_, **__: self.title,
            min_selectable=1,
            max_selectable=1,
            picker_type=picker_type
        )