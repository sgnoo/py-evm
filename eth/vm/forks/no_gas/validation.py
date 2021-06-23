from eth.vm.forks.frontier.state import FrontierTransactionExecutor
from eth.abc import (
    SignedTransactionAPI,
    StateAPI,
)
from eth.vm.forks.frontier.validation import (
    validate_frontier_transaction,
)


def validate_no_gas_transaction(state: StateAPI,
                                transaction: SignedTransactionAPI) -> None:
    transaction.gas_price = 0
    validate_frontier_transaction(state, transaction)
