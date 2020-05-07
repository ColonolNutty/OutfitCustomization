"""
This file is part of the Outfit Customization mod licensed under the Creative Commons Attribution-NonCommercial-NoDerivatives 4.0 International public license (CC BY-NC-ND 4.0).
https://creativecommons.org/licenses/by-nc-nd/4.0/
https://creativecommons.org/licenses/by-nc-nd/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from typing import Any

from cnoutfitcustomization.dialogs.customize_outfit_dialog import OCCustomizeOutfitDialog
from cnoutfitcustomization.modinfo import ModInfo
from cnoutfitcustomization.utils.outfit_customization_setting_utils import OCSettingUtils
from event_testing.results import TestResult
from interactions.context import InteractionContext
from sims.sim import Sim
from sims4communitylib.classes.interactions.common_immediate_super_interaction import CommonImmediateSuperInteraction
from sims4communitylib.mod_support.mod_identity import CommonModIdentity
from sims4communitylib.utils.common_type_utils import CommonTypeUtils
from sims4communitylib.utils.sims.common_sim_utils import CommonSimUtils


class OCCustomizeOutfitInteraction(CommonImmediateSuperInteraction):
    """ Handles the Customize Outfit interaction."""

    def __init__(self, *_, **__) -> None:
        super().__init__(*_, **__)
        self._customize_outfit_dialog = OCCustomizeOutfitDialog()

    # noinspection PyMissingOrEmptyDocstring
    @classmethod
    def get_mod_identity(cls) -> CommonModIdentity:
        return ModInfo.get_identity()

    # noinspection PyMissingOrEmptyDocstring
    @classmethod
    def get_log_identifier(cls) -> str:
        return 'oc_customize_outfit_interaction'

    # noinspection PyMissingOrEmptyDocstring
    @classmethod
    def on_test(cls, interaction_sim: Sim, interaction_target: Any, interaction_context: InteractionContext, **kwargs) -> TestResult:
        cls.get_log().format_with_message('Running \'{}\' on_test.'.format(cls.__name__), interaction_sim=interaction_sim, interaction_target=interaction_target, interaction_context=interaction_context, kwargles=kwargs)
        if interaction_target is None or not CommonTypeUtils.is_sim_instance(interaction_target):
            cls.get_log().debug('Failed, Target is not a Sim.')
            return TestResult.NONE
        sim_info = CommonSimUtils.get_sim_info(interaction_sim)
        if not OCSettingUtils.is_enabled_for_outfit_customization_interactions(sim_info):
            cls.get_log().debug('Failed, Active Sim is not available for Outfit Customization.')
            return TestResult.NONE
        target_sim_info = CommonSimUtils.get_sim_info(interaction_target)
        if not OCSettingUtils.is_enabled_for_outfit_customization_interactions(target_sim_info):
            cls.get_log().debug('Failed, Target Sim is not available for Outfit Customization.')
            return TestResult.NONE
        cls.get_log().debug('Success.')
        return TestResult.TRUE

    # noinspection PyMissingOrEmptyDocstring
    def on_started(self, interaction_sim: Sim, interaction_target: Any) -> bool:
        self.log.format_with_message('Running {} on_started.'.format(self.__class__.__name__), interaction_sim=interaction_sim, interaction_target=interaction_target)
        if interaction_target is None or not CommonTypeUtils.is_sim_or_sim_info(interaction_target):
            self.log.debug('Failed, Target is not a sim.')
            return TestResult.NONE
        target_sim_info = CommonSimUtils.get_sim_info(interaction_target)
        self._customize_outfit_dialog.open(target_sim_info)
        return True
