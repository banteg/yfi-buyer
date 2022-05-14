# @version 0.3.3
# @author banteg
from vyper.interfaces import ERC20

YFI: constant(address) = 0x0bc529c00C6401aEF6D220BE8C6Ea1667F6Ad93e
DAI: constant(address) = 0x6B175474E89094C44Da98b954EedeAC495271d0F
YFI_USD: constant(address) = 0xA027702dbb89fbd58938e4324ac03B58d812b0E1

STALE_AFTER: constant(uint256) = 2 * 3600

struct ChainlinkRound:
    roundId: uint80
    answer: int256
    startedAt: uint256
    updatedAt: uint256
    answeredInRound: uint80

interface Chainlink:
    def latestRoundData() -> ChainlinkRound: view

event Buyback:
    yfi: uint256
    dai: uint256


@external
def buy_dai(yfi_amount: uint256):
    oracle: ChainlinkRound = Chainlink(YFI_USD).latestRoundData()
    assert oracle.updatedAt + STALE_AFTER > block.timestamp  # dev: stale oracle

    dai_amount: uint256 = convert(oracle.answer, uint256) * yfi_amount / 10 ** 8

    assert ERC20(YFI).transferFrom(msg.sender, self, yfi_amount)  # dev: no allowance
    assert ERC20(DAI).transferFrom(self, msg.sender, dai_amount)  # dev: not enough dai

    log Buyback(yfi_amount, dai_amount)
