import asyncio

import pytest

from eth.rlp.headers import BlockHeader

from p2p.peer import ETHPeer
from peer_helpers import (
    get_directly_linked_peers,
)


@pytest.mark.asyncio
async def test_eth_peer_get_headers(request, event_loop):
    peer, remote = await get_directly_linked_peers(request, event_loop, peer1_class=ETHPeer, peer2_class=ETHPeer)
    header = BlockHeader(difficulty=100, block_number=0, gas_limit=3000000)

    async def send_headers():
        remote.sub_proto.send_block_headers((header,))
        await asyncio.sleep(0)

    asyncio.ensure_future(send_headers())
    response = await peer.get_block_headers(0, 1, 0, False)

    assert len(response) == 1
    assert response[0] == header
