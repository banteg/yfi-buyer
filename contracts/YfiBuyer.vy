# @version 0.3.3
# @author banteg
from vyper.interfaces import ERC20

YFI: constant(address) = 0x0bc529c00C6401aEF6D220BE8C6Ea1667F6Ad93e
DAI: constant(address) = 0x6B175474E89094C44Da98b954EedeAC495271d0F
WETH: constant(address) = 0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2
YFI_USD: constant(address) = 0xA027702dbb89fbd58938e4324ac03B58d812b0E1
YFI_ETH: constant(address) = 0x7c5d4F8345e66f68099581Db340cd65B078C41f4

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
    yfi_amount: uint256
    dai_amount: uint256
    eth_amount: uint256


@external
def sell_yfi_for_dai(yfi_amount: uint256):
    oracle: ChainlinkRound = Chainlink(YFI_USD).latestRoundData()
    assert oracle.updatedAt + STALE_AFTER > block.timestamp  # dev: stale oracle

    dai_amount: uint256 = convert(oracle.answer, uint256) * yfi_amount / 10 ** 8

    assert ERC20(YFI).transferFrom(msg.sender, self, yfi_amount)  # dev: no allowance
    assert ERC20(DAI).transferFrom(self, msg.sender, dai_amount)  # dev: not enough dai

    log Buyback(yfi_amount, dai_amount, 0)


@external
def sell_yfi_for_eth(yfi_amount: uint256):
    oracle: ChainlinkRound = Chainlink(YFI_ETH).latestRoundData()
    assert oracle.updatedAt + STALE_AFTER > block.timestamp  # dev: stale oracle

    eth_amount: uint256 = convert(oracle.answer, uint256) * yfi_amount / 10 ** 8

    assert ERC20(YFI).transferFrom(msg.sender, self, yfi_amount)  # dev: no allowance
    assert ERC20(WETH).transferFrom(self, msg.sender, eth_amount)  # dev: not enough weth

    log Buyback(yfi_amount, 0, eth_amount)
