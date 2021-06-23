from eth.vm.forks.frontier.state import FrontierState, FrontierTransactionExecutor

from eth.abc import (
    SignedTransactionAPI,
    MessageAPI,
)

from eth.vm.forks.no_gas.validation import validate_no_gas_transaction


class NoGasTransactionExecutor(FrontierTransactionExecutor):
    def build_evm_message(self, transaction: SignedTransactionAPI) -> MessageAPI:
        transaction.gas_price = 0
        return super().build_evm_message(transaction)

    def finalize_computation(self, transaction: SignedTransactionAPI, computation: ComputationAPI) -> ComputationAPI:
        transaction.gas_price = 0
        return super().finalize_computation(transaction, computation)


class NoGasState(FrontierState):
    def validate_transaction(self, transaction: SignedTransactionAPI) -> None:
        validate_no_gas_transaction(self, transaction)
