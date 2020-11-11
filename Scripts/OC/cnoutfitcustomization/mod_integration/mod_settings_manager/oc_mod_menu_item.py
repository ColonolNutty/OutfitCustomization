"""
This file is part of the Outfit Customization mod licensed under the Creative Commons Attribution-NonCommercial-NoDerivatives 4.0 International public license (CC BY-NC-ND 4.0).
https://creativecommons.org/licenses/by-nc-nd/4.0/
https://creativecommons.org/licenses/by-nc-nd/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""

# noinspection PyBroadException
try:
    from typing import Callable, Any
    from protocolbuffers.Localization_pb2 import LocalizedString
    from sims.sim_info import SimInfo
    from sims4communitylib.mod_support.mod_identity import CommonModIdentity
    from sims4communitylib.utils.common_function_utils import CommonFunctionUtils
    from sims4communitylib.utils.common_type_utils import CommonTypeUtils
    from sims4communitylib.utils.sims.common_sim_name_utils import CommonSimNameUtils
    from sims4communitylib.utils.sims.common_sim_utils import CommonSimUtils
    from sims4modsettingsmenu.registration.mod_settings_menu_item import S4MSMMenuItem
    from sims4modsettingsmenu.registration.mod_settings_registry import S4MSMModSettingsRegistry
    from event_testing.results import TestResult
    from sims4communitylib.utils.common_injection_utils import CommonInjectionUtils
    from sims4communitylib.utils.common_log_registry import CommonLogRegistry
    from cnoutfitcustomization.dialogs.customize_outfit_dialog import OCCustomizeOutfitDialog
    from cnoutfitcustomization.enums.string_identifiers import OCStringId
    from cnoutfitcustomization.interactions.customize_outfit import OCCustomizeOutfitInteraction
    from cnoutfitcustomization.modinfo import ModInfo
    from cnoutfitcustomization.utils.outfit_customization_setting_utils import OCSettingUtils


    class _OCMSMMenuItem(S4MSMMenuItem):
        # noinspection PyMissingOrEmptyDocstring
        @property
        def title(self) -> LocalizedString:
            return OCStringId.OC_CUSTOMIZE_OUTFIT_OC

        # noinspection PyMissingOrEmptyDocstring
        @property
        def mod_identity(self) -> CommonModIdentity:
            return ModInfo.get_identity()

        # noinspection PyMissingOrEmptyDocstring
        @property
        def log_identifier(self) -> str:
            return 'oc_msm_menu_item'

        # noinspection PyMissingOrEmptyDocstring
        def is_available_for(self, source_sim_info: SimInfo, target: Any=None) -> bool:
            self.log.debug('Checking if OC menu is available for \'{}\' and Target \'{}\'.'.format(CommonSimNameUtils.get_full_name(source_sim_info), target))
            if target is None or not CommonTypeUtils.is_sim_or_sim_info(target):
                self.log.debug('Target is not a Sim.')
                return False
            if not OCSettingUtils.is_enabled_for_interactions(source_sim_info):
                log.debug('Failed, Source Sim is not available for Outfit Customization.')
                return False
            target_sim_info = CommonSimUtils.get_sim_info(target)
            if not OCSettingUtils.is_enabled_for_interactions(target_sim_info):
                self.log.debug('Failed, Target Sim is not available for Outfit Customization.')
                return False
            self.log.debug('OC menu is available for Source Sim and Target Sim.')
            return True

        # noinspection PyMissingOrEmptyDocstring
        def show(
            self,
            source_sim_info: SimInfo,
            *args,
            target: Any=None,
            on_close: Callable[..., Any]=CommonFunctionUtils.noop,
            **kwargs
        ):
            self.log.debug('Showing OC Customize Outfit.')
            target_sim_info = CommonSimUtils.get_sim_info(target)
            OCCustomizeOutfitDialog(target_sim_info, on_close=on_close).open()


    S4MSMModSettingsRegistry().register_menu_item(_OCMSMMenuItem())

    log = CommonLogRegistry().register_log(ModInfo.get_identity(), 'oc_customize_outfit_interaction')

    # noinspection PyUnusedLocal
    @CommonInjectionUtils.inject_safely_into(ModInfo.get_identity(), OCCustomizeOutfitInteraction, OCCustomizeOutfitInteraction.on_test.__name__)
    def _oc_hide_settings_interaction(original, cls, *_, **__) -> TestResult:
        log.debug('Hiding the Customize Outfit interaction in favor of the Mod Settings Menu.')
        return TestResult.NONE
except:
    pass
