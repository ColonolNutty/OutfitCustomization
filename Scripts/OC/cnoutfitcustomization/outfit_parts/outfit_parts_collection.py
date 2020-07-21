"""
This file is part of the Outfit Customization mod licensed under the Creative Commons Attribution-NonCommercial-NoDerivatives 4.0 International public license (CC BY-NC-ND 4.0).
https://creativecommons.org/licenses/by-nc-nd/4.0/
https://creativecommons.org/licenses/by-nc-nd/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
import services
from sims.sim_info_types import Gender, Age
from sims4.localization import TunableLocalizedString
from sims4.resources import Types
from sims4.tuning.instances import HashedTunedInstanceMetaclass
from sims4.tuning.tunable import Tunable, TunableList, HasTunableFactory, AutoFactoryInit, TunableSet, TunableEnumSet
from sims4.tuning.tunable_base import GroupNames
from sims4communitylib.enums.common_species import CommonSpecies


class OCOutfitPartData(HasTunableFactory, AutoFactoryInit):
    """ Holds information related to an outfit part. """
    FACTORY_TUNABLES = {
        'part_display_name': TunableLocalizedString(default=None),
        'part_raw_display_name': Tunable(tunable_type=str, default=None),
        'part_author': Tunable(tunable_type=str, default=None),
        'part_icon_id': Tunable(tunable_type=int, default=0),
        'part_id': Tunable(tunable_type=int, default=-1),
        'available_for_genders': TunableEnumSet(enum_type=Gender),
        'available_for_ages': TunableEnumSet(enum_type=Age),
        'available_for_species': TunableEnumSet(enum_type=CommonSpecies),
        'part_tags': TunableSet(tunable=Tunable(tunable_type=str, default=None), tuning_group=GroupNames.TAG),
    }


class OCOutfitPartsCollection(metaclass=HashedTunedInstanceMetaclass, manager=services.get_instance_manager(Types.SNIPPET)):
    """ Holds information related to a collection of outfit parts. """
    INSTANCE_TUNABLES = {
        'outfit_parts_list': TunableList(tunable=OCOutfitPartData.TunableFactory())
    }
