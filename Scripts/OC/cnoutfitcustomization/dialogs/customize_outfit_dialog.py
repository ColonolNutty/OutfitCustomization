"""
This file is part of the Outfit Customization mod licensed under the Creative Commons Attribution-NonCommercial-NoDerivatives 4.0 International public license (CC BY-NC-ND 4.0).
https://creativecommons.org/licenses/by-nc-nd/4.0/
https://creativecommons.org/licenses/by-nc-nd/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
# noinspection PyBroadException
from sims4communitylib.dialogs.common_ok_dialog import CommonOkDialog
from sims4communitylib.utils.sims.common_sim_name_utils import CommonSimNameUtils

# noinspection PyBroadException
from ui.ui_dialog_picker import UiObjectPicker

try:
    # noinspection PyUnresolvedReferences
    from enum import Int
except:
    # noinspection PyMissingOrEmptyDocstring
    class Int:
        pass
from typing import Tuple, Any, List, Callable
from cnoutfitcustomization.enums.string_identifiers import OCStringId
from cnoutfitcustomization.modinfo import ModInfo
from cnoutfitcustomization.outfit_parts.outfit_part import OCOutfitPart
from cnoutfitcustomization.utils.outfit_part_utils import OCOutfitPartUtils
from sims.outfits.outfit_enums import BodyType
from sims.sim_info import SimInfo
from sims4communitylib.dialogs.option_dialogs.common_choose_object_option_dialog import CommonChooseObjectOptionDialog
from sims4communitylib.dialogs.option_dialogs.options.common_dialog_option_context import CommonDialogOptionContext
from sims4communitylib.dialogs.option_dialogs.options.objects.common_dialog_action_option import \
    CommonDialogActionOption
from sims4communitylib.dialogs.option_dialogs.options.objects.common_dialog_object_option import \
    CommonDialogObjectOption
from sims4communitylib.enums.strings_enum import CommonStringId
from sims4communitylib.exceptions.common_exceptions_handler import CommonExceptionHandler
from sims4communitylib.utils.cas.common_cas_utils import CommonCASUtils
from sims4communitylib.utils.common_icon_utils import CommonIconUtils
from sims4communitylib.utils.common_log_registry import CommonLogRegistry
from sims4communitylib.utils.localization.common_localization_utils import CommonLocalizationUtils
from sims4communitylib.utils.localization.common_localized_string_colors import CommonLocalizedStringColor

log = CommonLogRegistry.get().register_log(ModInfo.get_identity().name, 'oc_customize_outfit_dialog')


class _OutfitPartsBy(Int):
    NONE = 0
    TAG = 1
    AUTHOR = 2
    OUTFIT_SLOT = 3


class OCCustomizeOutfitDialog:
    """ A dialog that handles outfit customization. """
    @staticmethod
    @CommonExceptionHandler.catch_exceptions(ModInfo.get_identity().name)
    def open(sim_info: SimInfo):
        """ Open the dialog for customizing a sims outfit. """
        log.format_with_message('Opening customize outfit dialog.', sim=CommonSimNameUtils.get_full_name(sim_info))

        option_dialog = CommonChooseObjectOptionDialog(
            OCStringId.OC_CUSTOMIZE_OUTFIT_OC,
            0,
            mod_identity=ModInfo.get_identity()
        )

        def _reopen_dialog() -> None:
            option_dialog.show(sim_info=sim_info)

        def _on_remove_chosen() -> None:
            OCOutfitPartUtils.remove_outfit_parts(sim_info, tuple(OCOutfitPartUtils.get_outfit_parts(sim_info)))
            option_dialog.show(sim_info=sim_info)

        def _on_option_chosen(option_identifier: str, choice: int):
            log.debug('Opening Outfit Parts: {}'.format(option_identifier))
            OCCustomizeOutfitDialog._open_outfit_parts_by(sim_info, choice, on_close_callback=_reopen_dialog)

        option_dialog.add_option(
            CommonDialogObjectOption(
                'By Tag',
                _OutfitPartsBy.TAG,
                CommonDialogOptionContext(
                    OCStringId.OC_FILTER_BY_TAG,
                    0,
                    icon=CommonIconUtils.load_arrow_navigate_into_icon()
                ),
                on_chosen=_on_option_chosen
            )
        )

        option_dialog.add_option(
            CommonDialogObjectOption(
                'By Outfit Slot',
                _OutfitPartsBy.OUTFIT_SLOT,
                CommonDialogOptionContext(
                    OCStringId.OC_FILTER_BY_OUTFIT_SLOT,
                    0,
                    icon=CommonIconUtils.load_arrow_navigate_into_icon()
                ),
                on_chosen=_on_option_chosen
            )
        )

        option_dialog.add_option(
            CommonDialogObjectOption(
                'By Author',
                _OutfitPartsBy.AUTHOR,
                CommonDialogOptionContext(
                    OCStringId.OC_FILTER_BY_AUTHOR,
                    0,
                    icon=CommonIconUtils.load_arrow_navigate_into_icon()
                ),
                on_chosen=_on_option_chosen
            )
        )

        option_dialog.add_option(
            CommonDialogActionOption(
                CommonDialogOptionContext(
                    OCStringId.OC_REMOVE_ALL,
                    0,
                    icon=CommonIconUtils.load_x_icon(),
                    tooltip_text_identifier=OCStringId.OC_REMOVE_ALL
                ),
                on_chosen=_on_remove_chosen,
                always_visible=True
            )
        )

        option_dialog.show(sim_info=sim_info)

    @staticmethod
    def _open_outfit_parts_by(sim_info: SimInfo, outfit_parts_by: int, on_close_callback: Callable[..., Any]):
        log.format_with_message('Opening outfit parts by', outfit_parts_by=outfit_parts_by)

        def _on_close() -> None:
            on_close_callback()

        option_dialog = CommonChooseObjectOptionDialog(
            OCStringId.OC_CUSTOMIZE_OUTFIT_OC,
            0,
            mod_identity=ModInfo.get_identity(),
            on_close=_on_close
        )

        def _reopen_dialog() -> None:
            option_dialog.show(sim_info=sim_info)

        def _on_option_chosen(option_identifier: str, picked_category: Tuple[OCOutfitPart]):
            log.debug('Opening Outfit Parts By: {}'.format(option_identifier))
            OCCustomizeOutfitDialog._open_with_outfit_parts(sim_info, picked_category, on_close_callback=_reopen_dialog)

        def _no_outfit_parts_found() -> None:
            CommonOkDialog(
                OCStringId.OC_CUSTOMIZE_OUTFIT_OC,
                OCStringId.OC_NO_OUTFIT_PARTS_FOUND
            ).show(on_acknowledged=_on_close)

        if outfit_parts_by == _OutfitPartsBy.NONE:
            log.debug('outfit_parts_by was NONE')
            _no_outfit_parts_found()
            return

        outfit_parts = tuple(OCOutfitPartUtils.get_outfit_parts(sim_info))
        log.format_with_message('Creating outfit parts by', outfit_parts_by=outfit_parts_by)
        if len(outfit_parts) == 0:
            log.debug('No outfit parts found!')
            _no_outfit_parts_found()
            return

        sorted_outfit_parts = sorted(outfit_parts, key=lambda op: op.raw_display_name)
        if not sorted_outfit_parts:
            log.debug('Failed to sort outfit parts by name')
            _no_outfit_parts_found()
            return

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
            log.debug('No outfit parts found!')
            _no_outfit_parts_found()
            return

        log.format_with_message('Finished filtering outfit parts.', outfit_parts_by_value_dict=outfit_parts_by_value_dict)

        sorted_keys = sorted(outfit_parts_by_value_dict.keys())
        log.format(sorted_keys=sorted_keys)
        for key in sorted_keys:
            log.format_with_message('Building key', key=key)
            outfit_parts_by_value: List[OCOutfitPart] = outfit_parts_by_value_dict[key]
            if len(outfit_parts_by_value) == 0:
                log.debug('No parts found in key.')
                continue
            outfit_parts_count = str(len(outfit_parts_by_value))
            log.format_with_message('Found outfit parts', count=outfit_parts_count)
            option_dialog.add_option(
                CommonDialogObjectOption(
                    key,
                    tuple(outfit_parts_by_value),
                    CommonDialogOptionContext(
                        key,
                        OCStringId.OC_OUTFIT_PARTS_COUNT,
                        description_tokens=(outfit_parts_count,),
                        icon=CommonIconUtils.load_arrow_navigate_into_icon()
                    ),
                    on_chosen=_on_option_chosen
                )
            )

        if not option_dialog.has_options():
            log.debug('No options found in dialog.')
            _no_outfit_parts_found()
            return

        log.debug('Showing dialog.')

        option_dialog.show(sim_info=sim_info)

    @staticmethod
    def _get_outfit_part_key(outfit_part: OCOutfitPart, outfit_parts_by: int=_OutfitPartsBy.NONE) -> Any:
        if outfit_parts_by == _OutfitPartsBy.NONE:
            return None
        if outfit_parts_by == _OutfitPartsBy.TAG:
            return outfit_part.part_tags
        elif outfit_parts_by == _OutfitPartsBy.AUTHOR:
            return outfit_part.author,
        return str(CommonCASUtils.get_body_type_of_cas_part(outfit_part.part_id)).replace('BodyType.', ''),

    @staticmethod
    @CommonExceptionHandler.catch_exceptions(ModInfo.get_identity().name)
    def _open_with_outfit_parts(sim_info: SimInfo, outfit_parts: Tuple[OCOutfitPart], on_close_callback=None, current_page: int=1):
        log.format_with_message('Opening with outfit parts.', outfit_parts=outfit_parts)

        def _on_close() -> None:
            on_close_callback()

        option_dialog = CommonChooseObjectOptionDialog(
            OCStringId.OC_CUSTOMIZE_OUTFIT_OC,
            0,
            mod_identity=ModInfo.get_identity(),
            on_close=_on_close
        )

        def _reopen_dialog() -> None:
            OCCustomizeOutfitDialog._open_with_outfit_parts(sim_info, outfit_parts, on_close_callback=on_close_callback, current_page=option_dialog.current_page)

        def _on_option_chosen(option_identifier: str, picked_outfit_part: OCOutfitPart):
            log.debug('Chose outfit part: {}'.format(option_identifier))
            OCCustomizeOutfitDialog._open_body_type_selection(sim_info, picked_outfit_part, on_close_callback=_reopen_dialog)

        def _on_remove_chosen() -> None:
            OCOutfitPartUtils.remove_outfit_parts(sim_info, outfit_parts)
            _reopen_dialog()

        def _no_outfit_parts_found() -> None:
            CommonOkDialog(
                OCStringId.OC_CUSTOMIZE_OUTFIT_OC,
                OCStringId.OC_NO_OUTFIT_PARTS_FOUND
            ).show(on_acknowledged=_on_close)

        if not outfit_parts:
            _no_outfit_parts_found()
            return

        sorted_outfit_parts = sorted(outfit_parts, key=lambda item: item.raw_display_name)

        option_dialog.add_option(
            CommonDialogActionOption(
                CommonDialogOptionContext(
                    OCStringId.OC_REMOVE_ALL,
                    0,
                    icon=CommonIconUtils.load_x_icon(),
                    tooltip_text_identifier=OCStringId.OC_REMOVE_ALL
                ),
                on_chosen=_on_remove_chosen,
                always_visible=True
            )
        )
        for outfit_part in sorted_outfit_parts:
            part_id = outfit_part.part_id
            author = outfit_part.author
            icon = CommonIconUtils._load_icon(outfit_part.icon_id) or CommonIconUtils.load_question_mark_icon()
            outfit_part_name = outfit_part.display_name
            # If outfit part is already equipped
            if CommonCASUtils.has_cas_part_attached(sim_info, part_id, body_type=None):
                outfit_part_name = CommonLocalizationUtils.create_localized_string(CommonStringId.TEXT_WITH_GREEN_COLOR, tokens=(outfit_part_name,))

            option_dialog.add_option(
                CommonDialogObjectOption(
                    str(part_id),
                    outfit_part,
                    CommonDialogOptionContext(
                        outfit_part_name,
                        OCStringId.OC_AUTHOR,
                        description_tokens=(author,),
                        icon=icon
                    ),
                    on_chosen=_on_option_chosen
                )
            )

        option_dialog.show(sim_info=sim_info, picker_type=UiObjectPicker.UiObjectPickerObjectPickerType.OBJECT_LARGE, page=current_page)

    @staticmethod
    @CommonExceptionHandler.catch_exceptions(ModInfo.get_identity().name)
    def _open_body_type_selection(sim_info: SimInfo, outfit_part: OCOutfitPart, on_close_callback=None):
        def _on_close() -> None:
            on_close_callback()

        def _reopen_dialog() -> None:
            OCCustomizeOutfitDialog._open_body_type_selection(sim_info, outfit_part, on_close_callback=on_close_callback)

        def _on_option_chosen(option_identifier: str, picked_body_type: BodyType):
            log.debug('Chose body type: {}'.format(option_identifier))
            if CommonCASUtils.has_cas_part_attached(sim_info, outfit_part.part_id, body_type=None):
                OCOutfitPartUtils.remove_cas_part(sim_info, outfit_part.part_id, None)
            OCOutfitPartUtils.add_cas_part(sim_info, outfit_part.part_id, picked_body_type)
            _reopen_dialog()

        def _on_remove_chosen() -> None:
            if CommonCASUtils.has_cas_part_attached(sim_info, outfit_part.part_id, body_type=None):
                OCOutfitPartUtils.remove_cas_part(sim_info, outfit_part.part_id, None)
            _reopen_dialog()

        option_dialog = CommonChooseObjectOptionDialog(
            OCStringId.OC_CHOOSE_BODY_LOCATION,
            OCStringId.OC_WHERE_SHOULD_IT_BE_WORN_AT,
            mod_identity=ModInfo.get_identity(),
            per_page=25,
            on_close=_on_close
        )

        if CommonCASUtils.has_cas_part_attached(sim_info, outfit_part.part_id, body_type=None):
            option_dialog.add_option(
                CommonDialogActionOption(
                    CommonDialogOptionContext(
                        OCStringId.OC_REMOVE,
                        0,
                        icon=CommonIconUtils.load_x_icon(),
                        tooltip_text_identifier=OCStringId.OC_REMOVE
                    ),
                    on_chosen=_on_remove_chosen,
                    always_visible=True
                )
            )

        default_body_type = CommonCASUtils.get_body_type_of_cas_part(outfit_part.part_id)
        option_dialog.add_option(
            CommonDialogObjectOption(
                'Default',
                default_body_type,
                CommonDialogOptionContext(
                    OCStringId.OC_DEFAULT_VALUE,
                    0,
                    title_tokens=(str(default_body_type).replace('BodyType.', ''),),
                    icon=CommonIconUtils.load_arrow_right_icon()
                ),
                on_chosen=_on_option_chosen
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

            option_dialog.add_option(
                CommonDialogObjectOption(
                    str(body_type),
                    body_type,
                    CommonDialogOptionContext(
                        name,
                        row_description,
                        icon=CommonIconUtils.load_arrow_right_icon(),
                        tooltip_text_identifier=name
                    ),
                    on_chosen=_on_option_chosen
                )
            )

        option_dialog.show(sim_info=sim_info)
