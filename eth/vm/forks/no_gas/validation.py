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
    sender_balance = state.get_balance(transaction.sender)
    total_cost = transaction.value

    if sender_balance < total_cost:
        raise ValidationError("Sender account balance cannot afford txn")

    sender_nonce = state.get_nonce(transaction.sender)
    if sender_nonce != transaction.nonce:
        raise ValidationError(
            f"Invalid transaction nonce: Expected {sender_nonce}, but got {transaction.nonce}"
        )
