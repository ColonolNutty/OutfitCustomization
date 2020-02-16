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
from sims4communitylib.utils.common_log_registry import CommonLogRegistry
from sims4communitylib.utils.common_type_utils import CommonTypeUtils
from sims4communitylib.utils.sims.common_sim_utils import CommonSimUtils

log = CommonLogRegistry.get().register_log(ModInfo.get_identity().name, 'oc_customize_outfit_interaction')


class OCCustomizeOutfitInteraction(CommonImmediateSuperInteraction):
    """ Handles the Customize Outfit interaction."""

    # noinspection PyMissingOrEmptyDocstring
    @classmethod
    def on_test(cls, interaction_sim: Sim, interaction_target: Any, interaction_context: InteractionContext, **kwargs) -> TestResult:
        log.format_with_message('Running \'{}\' on_test.'.format(cls.__name__), interaction_sim=interaction_sim, interaction_target=interaction_target, interaction_context=interaction_context, kwargles=kwargs)
        if interaction_target is None or not CommonTypeUtils.is_sim_instance(interaction_target):
            log.debug('Failed, Target is not a Sim.')
            return TestResult.NONE
        sim_info = CommonSimUtils.get_sim_info(interaction_sim)
        if not OCSettingUtils.is_enabled_for_outfit_customization_interactions(sim_info):
            log.debug('Failed, Active Sim is not available for Outfit Customization.')
            return TestResult.NONE
        target_sim_info = CommonSimUtils.get_sim_info(interaction_target)
        if not OCSettingUtils.is_enabled_for_outfit_customization_interactions(target_sim_info):
            log.debug('Failed, Target Sim is not available for Outfit Customization.')
            return TestResult.NONE
        log.debug('Success.')
        return TestResult.TRUE

    # noinspection PyMissingOrEmptyDocstring
    def on_started(self, interaction_sim: Sim, interaction_target: Any) -> bool:
        log.format_with_message('Running {} on_started.'.format(self.__class__.__name__), interaction_sim=interaction_sim, interaction_target=interaction_target)
        if interaction_target is None or not CommonTypeUtils.is_sim_or_sim_info(interaction_target):
            log.debug('Failed, Target is not a sim.')
            return TestResult.NONE
        target_sim_info = CommonSimUtils.get_sim_info(interaction_target)
        OCCustomizeOutfitDialog.open(target_sim_info)
        return True
