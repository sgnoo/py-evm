from eth_keys import keys
from eth_utils import decode_hex, to_wei
from eth_typing import Address
from eth.consensus.pow import mine_pow_nonce
from eth import constants, chains

from eth.vm.forks.no_gas import NoGasVM
from eth.vm.forks.frontier import FrontierVM
from eth.vm.forks.no_gas import NoGasVM
from eth.db.atomic import AtomicDB

GENESIS_PARAMS = {
    'parent_hash': constants.GENESIS_PARENT_HASH,
    'uncles_hash': constants.EMPTY_UNCLE_HASH,
    'coinbase': constants.ZERO_ADDRESS,
    'transaction_root': constants.BLANK_ROOT_HASH,
    'receipt_root': constants.BLANK_ROOT_HASH,
    'difficulty': 1,
    'block_number': constants.GENESIS_BLOCK_NUMBER,
    'gas_limit': constants.GENESIS_GAS_LIMIT+500000, #why genesis 5000?,
    'timestamp': 1514764800,
    'extra_data': constants.GENESIS_EXTRA_DATA,
    'nonce': constants.GENESIS_NONCE
}
SENDER_PRIVATE_KEY = keys.PrivateKey(
  decode_hex('0x45a915e4d060149eb4365960e6a7a45f334393093061116b197e3240065ff2d8')
)
SENDER = Address(SENDER_PRIVATE_KEY.public_key.to_canonical_address())
RECEIVER = Address(b'\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\x02')
GENESIS_STATE = {
    SENDER: {
        "balance" : 10**20,
        "nonce" : 0,
        "code" : b"",
        "storage" : {}
    }
}

print("FrontierVM")
klass = chains.base.MiningChain.configure(
    __name__='TestChain',
    vm_configuration=(
        (constants.GENESIS_BLOCK_NUMBER, FrontierVM),
    )
)
chain = klass.from_genesis(AtomicDB(), GENESIS_PARAMS, GENESIS_STATE)
vm = chain.get_vm()
nonce = vm.state.get_nonce(SENDER)

print("- BEFORE SENDER BALANCE : {}".format(chain.get_vm().state.get_balance(SENDER)))
print("- BEFORE RECEIVER BALANCE : {}".format(chain.get_vm().state.get_balance(RECEIVER)))

tx = vm.create_unsigned_transaction(
    nonce=nonce,
    gas_price=100,
    gas=100000,
    to=RECEIVER,
    value=10,
    data=b'',
)
signed_tx = tx.as_signed_transaction(SENDER_PRIVATE_KEY)
chain.apply_transaction(signed_tx)

block_result = chain.get_vm().finalize_block(chain.get_block())
block = block_result.block

nonce, mix_hash = mine_pow_nonce(
    block.number,
    block.header.mining_hash,
    block.header.difficulty
)
block = chain.mine_block(mix_hash=mix_hash, nonce=nonce)

print("- AFTER SENDER BALANCE: {}".format(chain.get_vm().state.get_balance(SENDER)))
print("- AFTER RECEIVER BALANCE: {}".format(chain.get_vm().state.get_balance(RECEIVER)))

print("=================================================")

print("NoGasVM")
klass = chains.base.MiningChain.configure(
    __name__='TestChain',
    vm_configuration=(
        (constants.GENESIS_BLOCK_NUMBER, NoGasVM),
    )
)
chain = klass.from_genesis(AtomicDB(), GENESIS_PARAMS, GENESIS_STATE)
vm = chain.get_vm()
nonce = vm.state.get_nonce(SENDER)

print("- BEFORE SENDER BALANCE: {}".format(chain.get_vm().state.get_balance(SENDER)))
print("- BEFORE RECEIVER BALANCE: {}".format(chain.get_vm().state.get_balance(RECEIVER)))

tx = vm.create_unsigned_transaction(
    nonce=nonce,
    gas_price=100,
    gas=100000,
    to=RECEIVER,
    value=10,
    data=b'',
)
signed_tx = tx.as_signed_transaction(SENDER_PRIVATE_KEY)
chain.apply_transaction(signed_tx)

block_result = chain.get_vm().finalize_block(chain.get_block())
block = block_result.block

nonce, mix_hash = mine_pow_nonce(
    block.number,
    block.header.mining_hash,
    block.header.difficulty
)
block = chain.mine_block(mix_hash=mix_hash, nonce=nonce)

print("- AFTER SENDER BALANCE: {}".format(chain.get_vm().state.get_balance(SENDER)))
print("- AFTER RECEIVER BALANCE: {}".format(chain.get_vm().state.get_balance(RECEIVER)))
