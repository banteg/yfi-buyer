# @version 0.3.3
# @author banteg
from vyper.interfaces import ERC20

YFI: constant(address) = 0x0bc529c00C6401aEF6D220BE8C6Ea1667F6Ad93e
DAI: constant(address) = 0x6B175474E89094C44Da98b954EedeAC495271d0F
YFI_USD: constant(address) = 0xA027702dbb89fbd58938e4324ac03B58d812b0E1

interface Chainlink:
    def latestAnswer() -> uint256: view

event Buyback:
    yfi_amount: uint256
    dai_amount: uint256

@external
def sell_yfi_for_dai(yfi_amount: uint256):
    price: uint256 = Chainlink(YFI_USD).latestAnswer()
    dai_amount: uint256 = price * yfi_amount / 10 ** 8
    # settle order
    assert ERC20(YFI).transferFrom(msg.sender, self, yfi_amount)  # dev: no allowance
    assert ERC20(DAI).transferFrom(self, msg.sender, dai_amount)  # dev: not enough dai

    log Buyback(yfi_amount, dai_amount)
