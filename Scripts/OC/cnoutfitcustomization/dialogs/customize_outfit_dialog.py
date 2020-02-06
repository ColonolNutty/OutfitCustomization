"""
This file is part of the Outfit Customization mod licensed under the Creative Commons Attribution-NonCommercial-NoDerivatives 4.0 International public license (CC BY-NC-ND 4.0).
https://creativecommons.org/licenses/by-nc-nd/4.0/
https://creativecommons.org/licenses/by-nc-nd/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from typing import Tuple, Any, List
from cnoutfitcustomization.enums.string_identifiers import OCStringId
from cnoutfitcustomization.modinfo import ModInfo
from cnoutfitcustomization.outfit_parts.outfit_part import OCOutfitPart
from cnoutfitcustomization.utils.outfit_part_utils import OCOutfitPartUtils
from sims.outfits.outfit_enums import BodyType
from sims.sim_info import SimInfo
from sims4communitylib.dialogs.choose_object_dialog import CommonChooseObjectDialog
from sims4communitylib.dialogs.common_choice_outcome import CommonChoiceOutcome
from sims4communitylib.enums.enumtypes.int_enum import CommonEnumIntBase
from sims4communitylib.enums.strings_enum import CommonStringId
from sims4communitylib.exceptions.common_exceptions_handler import CommonExceptionHandler
from sims4communitylib.utils.cas.common_cas_utils import CommonCASUtils
from sims4communitylib.utils.common_icon_utils import CommonIconUtils
from sims4communitylib.utils.common_log_registry import CommonLogRegistry
from sims4communitylib.utils.localization.common_localization_utils import CommonLocalizationUtils
from sims4communitylib.utils.localization.common_localized_string_colors import CommonLocalizedStringColor
from ui.ui_dialog_picker import ObjectPickerRow

log = CommonLogRegistry.get().register_log(ModInfo.MOD_NAME, 'oc_customize_outfit_dialog')


class _OutfitPartsBy(CommonEnumIntBase):
    NONE = 0
    TAG = 1
    AUTHOR = 2
    OUTFIT_SLOT = 3


class OCCustomizeOutfitDialog:
    """ A dialog that handles outfit customization. """
    @staticmethod
    @CommonExceptionHandler.catch_exceptions(ModInfo.MOD_NAME)
    def open(sim_info: SimInfo):
        """ Open the dialog for customizing a sims outfit. """
        log.debug('Opening customize outfit dialog.')
        outfit_parts_by_category = 10
        outfit_parts_by_author = 11
        outfit_parts_by_outfit_slot = 12
        remove_all_outfit_parts = 22

        picker_options = list()
        picker_options.append(
            ObjectPickerRow(
                option_id=outfit_parts_by_category,
                name=CommonLocalizationUtils.create_localized_string(OCStringId.OC_FILTER_BY_TAG),
                row_tooltip=None,
                icon=CommonIconUtils.load_arrow_navigate_into_icon(),
                tag=_OutfitPartsBy.TAG
            )
        )

        picker_options.append(
            ObjectPickerRow(
                option_id=outfit_parts_by_author,
                name=CommonLocalizationUtils.create_localized_string(OCStringId.OC_FILTER_BY_AUTHOR),
                row_tooltip=None,
                icon=CommonIconUtils.load_arrow_navigate_into_icon(),
                tag=_OutfitPartsBy.AUTHOR
            )
        )

        picker_options.append(
            ObjectPickerRow(
                option_id=outfit_parts_by_outfit_slot,
                name=CommonLocalizationUtils.create_localized_string(OCStringId.OC_FILTER_BY_OUTFIT_SLOT),
                row_tooltip=None,
                icon=CommonIconUtils.load_arrow_navigate_into_icon(),
                tag=_OutfitPartsBy.OUTFIT_SLOT
            )
        )

        picker_options.append(
            ObjectPickerRow(
                option_id=remove_all_outfit_parts,
                name=CommonLocalizationUtils.create_localized_string(OCStringId.OC_REMOVE_ALL),
                row_tooltip=None,
                icon=CommonIconUtils.load_arrow_right_icon(),
                tag=_OutfitPartsBy.NONE
            )
        )

        @CommonExceptionHandler.catch_exceptions(ModInfo.MOD_NAME)
        def _option_picked(picked_option: _OutfitPartsBy, picker_result: CommonChoiceOutcome):
            if picked_option is None or CommonChoiceOutcome.is_error_or_cancel(picker_result):
                return
            if picked_option == _OutfitPartsBy.NONE:
                OCOutfitPartUtils.remove_outfit_parts(sim_info, tuple(OCOutfitPartUtils.get_outfit_parts(sim_info)))
                OCCustomizeOutfitDialog.open(sim_info)
            else:
                OCCustomizeOutfitDialog._open_outfit_parts_by(sim_info, picked_option)

        dialog = CommonChooseObjectDialog(
            OCStringId.OC_CUSTOMIZE_OUTFIT_OC,
            0,
            tuple(picker_options)
        )
        dialog.show(on_chosen=_option_picked)

    @staticmethod
    def _open_outfit_parts_by(sim_info: SimInfo, outfit_parts_by: _OutfitPartsBy):
        log.format_with_message('Opening outfit parts by', outfit_parts_by=outfit_parts_by)

        def _on_close_callback():
            OCCustomizeOutfitDialog._open_outfit_parts_by(sim_info, outfit_parts_by)

        @CommonExceptionHandler.catch_exceptions(ModInfo.MOD_NAME)
        def _option_picked(picked_outfit_part_category: Tuple[OCOutfitPart], picker_result: CommonChoiceOutcome):
            if picked_outfit_part_category is None or CommonChoiceOutcome.is_error_or_cancel(picker_result):
                OCCustomizeOutfitDialog.open(sim_info)
                return False
            if picked_outfit_part_category == 'None':
                OCCustomizeOutfitDialog._open_outfit_parts_by(sim_info, outfit_parts_by)
                return
            OCCustomizeOutfitDialog._open_with_outfit_parts(sim_info, picked_outfit_part_category, on_close_callback=_on_close_callback)

        picker_options = OCCustomizeOutfitDialog._get_outfit_parts_by_rows(sim_info, outfit_parts_by)

        dialog = CommonChooseObjectDialog(
            OCStringId.OC_CUSTOMIZE_OUTFIT_OC,
            0,
            tuple(picker_options)
        )
        dialog.show(on_chosen=_option_picked)

    @staticmethod
    def _get_outfit_part_key(outfit_part: OCOutfitPart, outfit_parts_by: _OutfitPartsBy=_OutfitPartsBy.NONE) -> Any:
        if outfit_parts_by == _OutfitPartsBy.NONE:
            return None
        if outfit_parts_by == _OutfitPartsBy.TAG:
            return outfit_part.part_tags
        elif outfit_parts_by == _OutfitPartsBy.AUTHOR:
            return outfit_part.author,
        return str(CommonCASUtils.get_body_type_of_cas_part(outfit_part.part_id)).replace('BodyType.', ''),

    @staticmethod
    @CommonExceptionHandler.catch_exceptions(ModInfo.MOD_NAME)
    def _open_with_outfit_parts(sim_info: SimInfo, outfit_parts: Tuple[OCOutfitPart], on_close_callback=None):
        log.format_with_message('Opening with outfit parts.', outfit_parts=outfit_parts)

        def _on_close_callback():
            OCCustomizeOutfitDialog._open_with_outfit_parts(sim_info, outfit_parts, on_close_callback=on_close_callback)

        @CommonExceptionHandler.catch_exceptions(ModInfo.MOD_NAME)
        def _option_picked(picked_outfit_part: OCOutfitPart, picked_result: CommonChoiceOutcome):
            if picked_outfit_part is None or CommonChoiceOutcome.is_error_or_cancel(picked_result):
                if on_close_callback is not None:
                    on_close_callback()
                return False
            if picked_outfit_part == 'RemoveAll':
                OCOutfitPartUtils.remove_outfit_parts(sim_info, outfit_parts)
                OCCustomizeOutfitDialog._open_with_outfit_parts(sim_info, outfit_parts, on_close_callback=on_close_callback)
                return True
            OCCustomizeOutfitDialog._open_body_type_selection(sim_info, picked_outfit_part, on_close_callback=_on_close_callback)

        picker_options = OCCustomizeOutfitDialog._get_outfit_part_rows_by_value(sim_info, outfit_parts)

        dialog = CommonChooseObjectDialog(
            OCStringId.OC_CUSTOMIZE_OUTFIT_OC,
            0,
            tuple(picker_options)
        )
        dialog.show(on_chosen=_option_picked)

    @staticmethod
    @CommonExceptionHandler.catch_exceptions(ModInfo.MOD_NAME)
    def _open_body_type_selection(sim_info: SimInfo, outfit_part: OCOutfitPart, on_close_callback=None):
        @CommonExceptionHandler.catch_exceptions(ModInfo.MOD_NAME)
        def _option_picked(picked_body_type: BodyType, picked_result: CommonChoiceOutcome):
            if picked_body_type is None or CommonChoiceOutcome.is_error_or_cancel(picked_result):
                if on_close_callback is not None:
                    on_close_callback()
                return False
            log.format(picked_body_type=picked_body_type)
            if CommonCASUtils.has_cas_part_attached(sim_info, outfit_part.part_id, body_type=None):
                OCOutfitPartUtils.remove_cas_part(sim_info, outfit_part.part_id, None)
            if picked_body_type == 'Remove':
                OCCustomizeOutfitDialog._open_body_type_selection(sim_info, outfit_part, on_close_callback=on_close_callback)
                return True
            OCOutfitPartUtils.add_cas_part(sim_info, outfit_part.part_id, picked_body_type)
            OCCustomizeOutfitDialog._open_body_type_selection(sim_info, outfit_part, on_close_callback=on_close_callback)
            return True

        picker_options = []

        if CommonCASUtils.has_cas_part_attached(sim_info, outfit_part.part_id, body_type=None):
            picker_options.append(
                ObjectPickerRow(
                    option_id=len(picker_options),
                    name=CommonLocalizationUtils.create_localized_string(OCStringId.OC_REMOVE),
                    row_tooltip=None,
                    icon=CommonIconUtils.load_arrow_right_icon(),
                    tag='Remove'
                )
            )

        default_body_type = CommonCASUtils.get_body_type_of_cas_part(outfit_part.part_id)
        picker_options.append(
            ObjectPickerRow(
                option_id=len(picker_options),
                name=CommonLocalizationUtils.create_localized_string(OCStringId.OC_DEFAULT_VALUE, tokens=(str(default_body_type).replace('BodyType.', ''),)),
                row_tooltip=None,
                icon=CommonIconUtils.load_arrow_right_icon(),
                tag=default_body_type
            )
        )

        sorted_body_types = sorted(BodyType.values, key=lambda bt: str(bt))

        for body_type in sorted_body_types:
            if body_type == BodyType.NONE or body_type == default_body_type:
                continue

            cas_part_id = CommonCASUtils.get_cas_part_id_at_body_type(sim_info, body_type)
            if cas_part_id != -1:
                cas_part_id_at_body_type = str(cas_part_id)
            else:
                cas_part_id_at_body_type = OCStringId.OC_NONE

            name = CommonLocalizationUtils.create_localized_string(OCStringId.OC_LOCATION, tokens=(str(body_type).replace('BodyType.', ''),))
            row_description = CommonLocalizationUtils.create_localized_string(OCStringId.OC_CURRENT, tokens=(cas_part_id_at_body_type,))
            if cas_part_id == outfit_part.part_id:
                name = CommonLocalizationUtils.colorize(name, text_color=CommonLocalizedStringColor.GREEN)
                row_description = CommonLocalizationUtils.colorize(row_description, text_color=CommonLocalizedStringColor.GREEN)

            picker_options.append(
                ObjectPickerRow(
                    option_id=len(picker_options),
                    name=name,
                    row_description=row_description,
                    row_tooltip=None,
                    icon=CommonIconUtils.load_arrow_right_icon(),
                    tag=body_type
                )
            )

        dialog = CommonChooseObjectDialog(
            OCStringId.OC_CHOOSE_BODY_LOCATION,
            OCStringId.OC_WHERE_SHOULD_IT_BE_WORN_AT,
            tuple(picker_options),
            per_page=25
        )
        dialog.show(on_chosen=_option_picked)

    @staticmethod
    def _get_outfit_parts_by_rows(sim_info: SimInfo, outfit_parts_by: _OutfitPartsBy) -> Tuple[ObjectPickerRow]:
        default_picker_row = ObjectPickerRow(
            option_id=0,
            name=CommonLocalizationUtils.create_localized_string(OCStringId.OC_NO_OUTFIT_PARTS_FOUND),
            row_description=CommonLocalizationUtils.create_localized_string(0),
            row_tooltip=None,
            icon=CommonIconUtils.load_question_mark_icon(),
            tag='None'
        )
        if outfit_parts_by == _OutfitPartsBy.NONE:
            log.debug('outfit_parts_by was NONE')
            return default_picker_row,

        outfit_parts = tuple(OCOutfitPartUtils.get_outfit_parts(sim_info))
        log.format_with_message('Creating outfit parts by', outfit_parts_by=outfit_parts_by)
        if len(outfit_parts) == 0:
            log.debug('No outfit parts found!')
            return default_picker_row,

        sorted_outfit_parts = sorted(outfit_parts, key=lambda op: op.raw_display_name)
        if not sorted_outfit_parts:
            log.debug('Failed sort outfit parts')
            return default_picker_row,
        log.format_with_message('Outfit parts sorted.', sorted_outfit_parts=sorted_outfit_parts)

        outfit_parts_by_value_dict = {}
        for outfit_part in sorted_outfit_parts:
            outfit_part: OCOutfitPart = outfit_part
            log.format_with_message('Looking at outfit part.', outfit_part=outfit_part)
            if not CommonCASUtils.is_cas_part_loaded(outfit_part.part_id):
                log.debug('Outfit part not loaded.')
                continue
            keys = OCCustomizeOutfitDialog._get_outfit_part_key(outfit_part, outfit_parts_by=outfit_parts_by)
            if keys is None:
                log.debug('No key found.')
                continue
            for key in keys:
                str_key = str(key)
                by_value = outfit_parts_by_value_dict.get(str_key, list())
                by_value.append(outfit_part)
                outfit_parts_by_value_dict[str_key] = by_value
            log.debug('Outfit part loaded.')
        if len(outfit_parts_by_value_dict) == 0:
            log.format_with_message('No outfit parts found with outfit parts by!', outfit_parts_by=outfit_parts_by, outfit_parts_by_value_dict=outfit_parts_by_value_dict)
            return default_picker_row,
        log.format_with_message('Finished filtering outfit parts.', outfit_parts_by_value_dict=outfit_parts_by_value_dict)

        sorted_keys = sorted(outfit_parts_by_value_dict.keys())
        log.format(sorted_keys=sorted_keys)
        picker_rows = list()
        for key in sorted_keys:
            log.format_with_message('Building key', key=key)
            outfit_parts_by_value: List[OCOutfitPart] = outfit_parts_by_value_dict[key]
            if len(outfit_parts_by_value) == 0:
                log.debug('No parts found in key.')
                continue
            outfit_parts_count = str(len(outfit_parts_by_value))
            log.format_with_message('Found outfit parts', count=outfit_parts_count)
            picker_row = ObjectPickerRow(
                option_id=len(picker_rows),
                name=CommonLocalizationUtils.create_localized_string(key),
                row_description=CommonLocalizationUtils.create_localized_string(OCStringId.OC_OUTFIT_PARTS_COUNT, tokens=(outfit_parts_count,)),
                row_tooltip=None,
                icon=CommonIconUtils.load_arrow_navigate_into_icon(),
                tag=outfit_parts_by_value
            )
            picker_rows.append(picker_row)
        log.format_with_message('Ended with options', picker_rows=picker_rows)
        return tuple(picker_rows)

    @staticmethod
    def _get_outfit_part_rows_by_value(sim_info: SimInfo, outfit_parts: Tuple[OCOutfitPart]) -> Tuple[ObjectPickerRow]:
        if not outfit_parts:
            return ObjectPickerRow(
                option_id=0,
                name=CommonLocalizationUtils.create_localized_string(OCStringId.OC_NO_OUTFIT_PARTS_FOUND),
                row_description=CommonLocalizationUtils.create_localized_string(0),
                row_tooltip=None,
                icon=CommonIconUtils.load_question_mark_icon(),
                tag='None'
            ),

        sorted_outfit_parts = sorted(outfit_parts, key=lambda item: item.raw_display_name)
        picker_rows = list()
        picker_rows.append(
            ObjectPickerRow(
                option_id=0,
                name=CommonLocalizationUtils.create_localized_string(OCStringId.OC_REMOVE_ALL),
                row_description=CommonLocalizationUtils.create_localized_string(0),
                row_tooltip=None,
                icon=CommonIconUtils.load_arrow_right_icon(),
                tag='RemoveAll'
            )
        )
        for outfit_part in sorted_outfit_parts:
            option_id = len(picker_rows)
            part_id = outfit_part.part_id
            author = outfit_part.author
            icon = CommonIconUtils._load_icon(outfit_part.icon_id) or CommonIconUtils.load_question_mark_icon()
            outfit_part_name = outfit_part.display_name or CommonLocalizationUtils.create_localized_string(str(option_id))
            # If outfit part is already equipped
            if CommonCASUtils.has_cas_part_attached(sim_info, part_id, body_type=None):
                outfit_part_name = CommonLocalizationUtils.create_localized_string(CommonStringId.TEXT_WITH_GREEN_COLOR, tokens=(outfit_part_name,))
            picker_rows.append(
                ObjectPickerRow(
                    option_id=option_id,
                    name=outfit_part_name,
                    row_description=CommonLocalizationUtils.create_localized_string(OCStringId.OC_AUTHOR, tokens=(author,)),
                    row_tooltip=lambda *_, **__: CommonLocalizationUtils.create_localized_string(outfit_part_name),
                    icon=icon,
                    tag=outfit_part
                )
            )
        return tuple(picker_rows)
