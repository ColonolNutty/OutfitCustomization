"""
This file is part of the Outfit Customization mod licensed under the Creative Commons Attribution-NonCommercial-NoDerivatives 4.0 International public license (CC BY-NC-ND 4.0).
https://creativecommons.org/licenses/by-nc-nd/4.0/
https://creativecommons.org/licenses/by-nc-nd/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from cnoutfitcustomization.outfit_parts.query.cas_part_query_utils import OCCASPartQueryUtils
from sims4communitylib.dialogs.common_ok_dialog import CommonOkDialog
from sims4communitylib.dialogs.option_dialogs.options.objects.common_dialog_select_option import \
    CommonDialogSelectOption
from sims4communitylib.enums.enumtypes.common_int import CommonInt
from sims4communitylib.logging.has_log import HasLog
from sims4communitylib.mod_support.mod_identity import CommonModIdentity
from sims4communitylib.services.sim.cas.common_sim_outfit_io import CommonSimOutfitIO
from sims4communitylib.utils.common_function_utils import CommonFunctionUtils
from sims4communitylib.utils.sims.common_sim_name_utils import CommonSimNameUtils
from ui.ui_dialog_picker import UiObjectPicker
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
from sims4communitylib.utils.localization.common_localization_utils import CommonLocalizationUtils
from sims4communitylib.utils.localization.common_localized_string_colors import CommonLocalizedStringColor


class _OutfitPartsBy(CommonInt):
    NONE: '_OutfitPartsBy' = 0
    TAG: '_OutfitPartsBy' = 1
    AUTHOR: '_OutfitPartsBy' = 2
    OUTFIT_SLOT: '_OutfitPartsBy' = 3


class OCCustomizeOutfitDialog(HasLog):
    """ A dialog that handles outfit customization. """
    def __init__(self, sim_info: SimInfo, on_close: Callable[..., Any]=CommonFunctionUtils.noop) -> None:
        super().__init__()
        self._sim_info = sim_info
        self._on_close = on_close

    # noinspection PyMissingOrEmptyDocstring
    @property
    def mod_identity(self) -> CommonModIdentity:
        return ModInfo.get_identity()

    # noinspection PyMissingOrEmptyDocstring
    @property
    def log_identifier(self) -> str:
        return 'oc_customize_outfit_dialog'

    @CommonExceptionHandler.catch_exceptions(ModInfo.get_identity())
    def open(self) -> None:
        """ Open the dialog for customizing a sims outfit. """
        self.log.format_with_message('Opening customize outfit dialog.', sim=CommonSimNameUtils.get_full_name(self._sim_info))

        def _on_close() -> None:
            if self._on_close is not None:
                self._on_close()

        def _reopen_dialog() -> None:
            option_dialog.show(sim_info=self._sim_info, page=option_dialog.current_page)

        outfit_parts = OCCASPartQueryUtils().get_cas_parts_for_sim(self._sim_info)
        if not outfit_parts:
            CommonOkDialog(
                OCStringId.OC_CUSTOMIZE_OUTFIT_OC,
                OCStringId.OC_NO_OUTFIT_PARTS_FOUND,
                mod_identity=self.mod_identity
            ).show(on_acknowledged=_on_close)
            return

        option_dialog = CommonChooseObjectOptionDialog(
            OCStringId.OC_CUSTOMIZE_OUTFIT_OC,
            0,
            on_close=_on_close,
            mod_identity=self.mod_identity
        )

        def _on_option_chosen(option_identifier: str, choice: _OutfitPartsBy):
            self.log.debug('Opening Outfit Parts: {}'.format(option_identifier))
            self._open_outfit_parts_by(choice, outfit_parts, on_close=_reopen_dialog)

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

        option_dialog.show(sim_info=self._sim_info)

    def _open_outfit_parts_by(self, outfit_parts_by: _OutfitPartsBy, outfit_parts: Tuple[OCOutfitPart], on_close: Callable[[], None]):
        self.log.format_with_message('Opening outfit parts by', outfit_parts_by=outfit_parts_by)

        def _on_close() -> None:
            on_close()

        option_dialog = CommonChooseObjectOptionDialog(
            OCStringId.OC_CUSTOMIZE_OUTFIT_OC,
            0,
            on_close=_on_close,
            mod_identity=self.mod_identity
        )

        def _reopen_dialog() -> None:
            option_dialog.show(sim_info=self._sim_info, page=option_dialog.current_page)

        def _on_option_chosen(option_identifier: str, chosen: Tuple[OCOutfitPart]):
            self.log.debug('Opening Outfit Parts By: {}'.format(option_identifier))
            self._open_with_outfit_parts(chosen, on_close_callback=_reopen_dialog)

        def _no_outfit_parts_found() -> None:
            CommonOkDialog(
                OCStringId.OC_CUSTOMIZE_OUTFIT_OC,
                OCStringId.OC_NO_OUTFIT_PARTS_FOUND,
                mod_identity=self.mod_identity
            ).show(on_acknowledged=_on_close)

        if outfit_parts_by == _OutfitPartsBy.NONE:
            self.log.debug('outfit_parts_by was NONE')
            _no_outfit_parts_found()
            return

        self.log.format_with_message('Creating outfit parts by', outfit_parts_by=outfit_parts_by)
        if len(outfit_parts) == 0:
            self.log.debug('No outfit parts found!')
            _no_outfit_parts_found()
            return

        sorted_outfit_parts = sorted(outfit_parts, key=lambda op: op.raw_display_name)
        if not sorted_outfit_parts:
            self.log.debug('Failed to sort outfit parts by name')
            _no_outfit_parts_found()
            return

        self.log.format_with_message('Outfit parts sorted.', sorted_outfit_parts=sorted_outfit_parts)

        outfit_parts_by_value_dict = {}
        for outfit_part in sorted_outfit_parts:
            outfit_part: OCOutfitPart = outfit_part
            self.log.format_with_message('Looking at outfit part.', outfit_part=outfit_part)
            if not CommonCASUtils.is_cas_part_loaded(outfit_part.part_id):
                self.log.debug('Outfit part not loaded.')
                continue
            keys = self._get_outfit_part_key(outfit_part, outfit_parts_by=outfit_parts_by)
            if keys is None:
                self.log.debug('No key found.')
                continue
            for key in keys:
                str_key = str(key)
                by_value = outfit_parts_by_value_dict.get(str_key, list())
                by_value.append(outfit_part)
                outfit_parts_by_value_dict[str_key] = by_value
            self.log.debug('Outfit part loaded.')

        if len(outfit_parts_by_value_dict) == 0:
            self.log.format_with_message('No outfit parts found with outfit parts by!', outfit_parts_by=outfit_parts_by, outfit_parts_by_value_dict=outfit_parts_by_value_dict)
            self.log.debug('No outfit parts found!')
            _no_outfit_parts_found()
            return

        self.log.format_with_message('Finished filtering outfit parts.', outfit_parts_by_value_dict=outfit_parts_by_value_dict)

        sorted_keys = sorted(outfit_parts_by_value_dict.keys())
        self.log.format(sorted_keys=sorted_keys)
        for key in sorted_keys:
            self.log.format_with_message('Building key', key=key)
            outfit_parts_by_value: List[OCOutfitPart] = outfit_parts_by_value_dict[key]
            if len(outfit_parts_by_value) == 0:
                self.log.debug('No parts found in key.')
                continue
            outfit_parts_count = str(len(outfit_parts_by_value))
            self.log.format_with_message('Found outfit parts', count=outfit_parts_count)
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
            self.log.debug('No options found in dialog.')
            _no_outfit_parts_found()
            return

        self.log.debug('Showing dialog.')

        option_dialog.show(sim_info=self._sim_info)

    def _get_outfit_part_key(self, outfit_part: OCOutfitPart, outfit_parts_by: _OutfitPartsBy=_OutfitPartsBy.NONE) -> Any:
        if outfit_parts_by == _OutfitPartsBy.NONE:
            return None
        if outfit_parts_by == _OutfitPartsBy.TAG:
            return outfit_part.tags
        elif outfit_parts_by == _OutfitPartsBy.AUTHOR:
            return outfit_part.author,
        return str(CommonCASUtils.get_body_type_of_cas_part(outfit_part.part_id)).replace('BodyType.', ''),

    @CommonExceptionHandler.catch_exceptions(ModInfo.get_identity())
    def _open_with_outfit_parts(self, outfit_parts: Tuple[OCOutfitPart], on_close_callback: Callable[[], None]=None, current_page: int=1):
        self.log.format_with_message('Opening with outfit parts.', outfit_parts=outfit_parts)

        def _on_close() -> None:
            if on_close_callback is not None:
                on_close_callback()

        option_dialog = CommonChooseObjectOptionDialog(
            OCStringId.OC_CUSTOMIZE_OUTFIT_OC,
            0,
            on_close=_on_close,
            mod_identity=self.mod_identity
        )

        def _reopen_dialog() -> None:
            option_dialog.show(sim_info=self._sim_info, picker_type=UiObjectPicker.UiObjectPickerObjectPickerType.OBJECT, page=option_dialog.current_page)

        def _on_option_chosen(option_identifier: str, chosen: str):
            self.log.debug('Chose tag: {}'.format(option_identifier))
            self._open_cas_part_selector(outfit_parts, chosen, on_close_callback=_reopen_dialog)

        def _no_outfit_parts_found() -> None:
            CommonOkDialog(
                OCStringId.OC_CUSTOMIZE_OUTFIT_OC,
                OCStringId.OC_NO_OUTFIT_PARTS_FOUND,
                mod_identity=self.mod_identity
            ).show(on_acknowledged=_on_close)

        if not outfit_parts:
            _no_outfit_parts_found()
            return

        object_categories: List[str] = list()
        for outfit_part in outfit_parts:
            for part_tag in outfit_part.tag_list:
                if str(part_tag) in object_categories:
                    continue
                object_categories.append(str(part_tag))

        sorted_object_categories = sorted(object_categories, key=lambda item: item)
        for object_category in sorted_object_categories:
            option_dialog.add_option(
                CommonDialogSelectOption(
                    object_category,
                    object_category,
                    CommonDialogOptionContext(
                        object_category,
                        0,
                        icon=CommonIconUtils.load_arrow_navigate_into_icon()
                    ),
                    on_chosen=_on_option_chosen
                )
            )

        option_dialog.show(
            sim_info=self._sim_info,
            picker_type=UiObjectPicker.UiObjectPickerObjectPickerType.OBJECT,
            page=current_page
        )

    @CommonExceptionHandler.catch_exceptions(ModInfo.get_identity())
    def _open_cas_part_selector(self, outfit_parts: Tuple[OCOutfitPart], tag: str, on_close_callback: Callable[[], None]=None, current_page: int=1):
        self.log.format_with_message('Opening with outfit parts.', outfit_parts=outfit_parts)

        def _on_close() -> None:
            if on_close_callback is not None:
                on_close_callback()

        def _reopen_dialog() -> None:
            self._open_cas_part_selector(outfit_parts, tag, on_close_callback=on_close_callback, current_page=option_dialog.current_page)

        option_dialog = CommonChooseObjectOptionDialog(
            OCStringId.OC_CUSTOMIZE_OUTFIT_OC,
            0,
            mod_identity=self.mod_identity,
            on_close=_on_close
        )

        outfit_io = CommonSimOutfitIO(self._sim_info, mod_identity=self.mod_identity)

        def _on_option_chosen(option_identifier: str, picked_outfit_part: OCOutfitPart):
            self.log.debug('Chose outfit part: {}'.format(option_identifier))
            self._open_body_type_selection(picked_outfit_part, outfit_io, on_close_callback=_reopen_dialog)

        def _on_remove_chosen() -> None:
            OCOutfitPartUtils.remove_outfit_parts(self._sim_info, outfit_parts)
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
                    tooltip_text_identifier=OCStringId.OC_REMOVE_ALL,
                ),
                on_chosen=_on_remove_chosen,
                always_visible=True
            )
        )

        for outfit_part in sorted_outfit_parts:
            if tag not in outfit_part.tag_list:
                continue
            part_id = outfit_part.part_id
            author = outfit_part.author
            icon = CommonIconUtils._load_icon(outfit_part.icon_id) or CommonIconUtils.load_question_mark_icon()
            outfit_part_name = outfit_part.display_name
            # If outfit part is already equipped
            if outfit_io.is_cas_part_attached(part_id):
                outfit_part_name = CommonLocalizationUtils.create_localized_string(CommonStringId.TEXT_WITH_GREEN_COLOR, tokens=(outfit_part_name,))

            option_dialog.add_option(
                CommonDialogObjectOption(
                    str(part_id),
                    outfit_part,
                    CommonDialogOptionContext(
                        outfit_part_name,
                        OCStringId.OC_AUTHOR,
                        description_tokens=(author,),
                        icon=icon,
                    ),
                    on_chosen=_on_option_chosen
                )
            )

        # noinspection PyTypeChecker
        option_dialog.show(
            sim_info=self._sim_info,
            picker_type=UiObjectPicker.UiObjectPickerObjectPickerType.OBJECT,
            page=current_page
        )

    @CommonExceptionHandler.catch_exceptions(ModInfo.get_identity())
    def _open_body_type_selection(self, outfit_part: OCOutfitPart, outfit_io: CommonSimOutfitIO, on_close_callback: Callable[[], None]=None):
        def _on_close() -> None:
            if on_close_callback is not None:
                on_close_callback()

        def _reopen_dialog() -> None:
            self._open_body_type_selection(outfit_part, outfit_io, on_close_callback=on_close_callback)

        def _on_option_chosen(option_identifier: str, picked_body_type: BodyType):
            self.log.debug('Chose body type: {}'.format(option_identifier))
            if outfit_io.is_cas_part_attached(outfit_part.part_id):
                outfit_io.detach_cas_part(outfit_part.part_id)
            outfit_io.attach_cas_part(outfit_part.part_id, body_type=picked_body_type)
            outfit_io.apply()
            _reopen_dialog()

        def _on_remove_chosen() -> None:
            if outfit_io.is_cas_part_attached(outfit_part.part_id):
                outfit_io.detach_cas_part(outfit_part.part_id)
            outfit_io.apply()
            _reopen_dialog()

        option_dialog = CommonChooseObjectOptionDialog(
            OCStringId.OC_CHOOSE_BODY_LOCATION,
            OCStringId.OC_WHERE_SHOULD_IT_BE_WORN_AT,
            mod_identity=self.mod_identity,
            per_page=25,
            on_close=_on_close
        )

        if CommonCASUtils.has_cas_part_attached(self._sim_info, outfit_part.part_id, body_type=None):
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

            cas_part_id = CommonCASUtils.get_cas_part_id_at_body_type(self._sim_info, body_type)
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

        option_dialog.show(sim_info=self._sim_info)
