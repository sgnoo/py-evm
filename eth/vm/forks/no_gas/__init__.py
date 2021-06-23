from typing import Type

from eth.abc import (
    StateAPI,
)
from eth.vm.forks.frontier import FrontierVM
from .state import NoGasState


class NoGasVM(FrontierVM):
    # fork name
    fork = 'no_gas'

    _state_class: Type[StateAPI] = NoGasState
