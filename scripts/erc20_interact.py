import logging
import pathlib
from scripts.benchmark.utils.chain_plumbing import (
    get_chain,
    FUNDED_ADDRESS,
    FUNDED_ADDRESS_PRIVATE_KEY,
)

from scripts.benchmark.utils.address import (
    generate_random_address,
)

from scripts.benchmark.utils.compile import (
    get_compiled_contract
)

from scripts.benchmark.utils.tx import (
    new_transaction,
)

from eth.vm.forks.byzantium import (
    ByzantiumVM,
)

from eth.chains.base import (
    MiningChain,
)

from web3 import (
    Web3
)

from eth.constants import (
    CREATE_CONTRACT_ADDRESS
)

from eth_utils import (
    encode_hex,
    decode_hex,
    to_int,
)

FIRST_TX_GAS_LIMIT = 1400000
SECOND_TX_GAS_LIMIT = 60000
TRANSFER_AMOUNT = 1000
TRANSER_FROM_AMOUNT = 1

W3_TX_DEFAULTS = {'gas': 0, 'gasPrice': 0}

CONTRACT_FILE = 'scripts/benchmark/contract_data/erc20.sol'
CONTRACT_NAME = 'SimpleToken'

contract_interface = get_compiled_contract(
    pathlib.Path(CONTRACT_FILE),
    CONTRACT_NAME
)
w3 = Web3()


def run() -> None:

    # get Byzantium VM
    chain = get_chain(ByzantiumVM)
    _deploy_simple_token(chain)


def _deploy_simple_token(chain: MiningChain) -> None:
    # Instantiate the contract
    SimpleToken = w3.eth.contract(
        abi=contract_interface['abi'],
        bytecode=contract_interface['bin']
    )
    # Build transaction to deploy the contract
    w3_tx = SimpleToken.constructor().buildTransaction(W3_TX_DEFAULTS)
    tx = new_transaction(
        vm=chain.get_vm(),
        private_key=FUNDED_ADDRESS_PRIVATE_KEY,
        from_=FUNDED_ADDRESS,
        to=CREATE_CONTRACT_ADDRESS,
        amount=0,
        gas=FIRST_TX_GAS_LIMIT,
        data=decode_hex(w3_tx['data']),
    )
    logging.warning('Applying Transaction {}'.format(tx))
    block, receipt, computation = chain.apply_transaction(tx)
    logging.warning('Block {}'.format(block))
    logging.warning('Receipt {}'.format(receipt))
    logging.warning('Computation {}'.format(computation))

    # Keep track of deployed contract address
    deployed_contract_address = computation.msg.storage_address

    assert computation.is_success
    # Keep track of simple_token object
    simple_token = w3.eth.contract(
        address=Web3.toChecksumAddress(encode_hex(deployed_contract_address)),
        abi=contract_interface['abi'],
    )
    logging.warning(simple_token.address)


if __name__ == '__main__':
    run()
