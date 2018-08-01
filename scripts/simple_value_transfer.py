import logging
import rlp
import base64
from scripts.benchmark.utils.chain_plumbing import (
    get_chain,
    FUNDED_ADDRESS,
    FUNDED_ADDRESS_PRIVATE_KEY,
)

from scripts.benchmark.utils.address import (
    generate_random_address,
)

from scripts.benchmark.utils.tx import (
    new_transaction,
)

from eth_hash.auto import keccak

from eth.vm.forks.byzantium import (
    ByzantiumVM,
)

from eth.chains.base import (
    MiningChain,
)

from eth_utils import (
    encode_hex,
    decode_hex,
    to_int,
    to_hex,
)

def run() -> None:

    # get Byzantium VM
    chain = get_chain(ByzantiumVM)
    apply_transaction(chain)


def apply_transaction(chain: MiningChain) -> None:
    to_address = generate_random_address()

    tx = new_transaction(
        vm=chain.get_vm(),
        private_key=FUNDED_ADDRESS_PRIVATE_KEY,
        from_=FUNDED_ADDRESS,
        to=to_address,
        amount=100,
        data=b''
    )

    # apply transaction
    block, receipt, computation = chain.apply_transaction(tx)
    txhash = to_hex(tx.hash)

    # mine block
    chain.mine_block()

    logging.warning('Applying Transaction {}'.format(txhash))
    logging.warning('Block {}'.format(block))
    logging.warning('Receipt {}'.format(receipt))
    logging.warning('Computation {}'.format(computation))
    logging.warning('Computation {}'.format(gas_used_by(gas_used_by)))

    # get transcation from transaction hash
    txtest = chain.get_canonical_transaction(tx.hash)
    logging.warning(txtest)

    fromBalance = chain.get_vm().state.account_db.get_balance(FUNDED_ADDRESS)
    toBalance = chain.get_vm().state.account_db.get_balance(to_address)
    logging.warning('from balance {}'.format(fromBalance))
    logging.warning('to balance {}'.format(toBalance))


if __name__ == '__main__':
    run()
