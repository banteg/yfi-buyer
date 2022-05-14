import ape

def test_buyback_with_dai(buyer, yfi, dai, bunny, rune, brk_a, waifu):
    dai.transfer(buyer, brk_a, sender=rune)
    yfi.approve(buyer, waifu, sender=bunny)
    receipt = buyer.buy_dai(waifu, sender=bunny)
    log = next(buyer.Buyback.from_receipt(receipt))
    print(log.event_arguments)
    print(log.dai / log.yfi, 'YFI/DAI')

    assert log.yfi == waifu
    assert yfi.balanceOf(buyer) == waifu
    assert dai.balanceOf(bunny) == log.dai


def test_buyback_stale_oracle(buyer, yfi, dai, bunny, rune, brk_a, waifu, chain):
    dai.transfer(buyer, brk_a, sender=rune)
    yfi.approve(buyer, waifu, sender=bunny)
    
    chain.mine(deltatime=86400)
    
    with ape.reverts():
        buyer.buy_dai(waifu, sender=bunny, gas_limit=1000000)

    assert yfi.balanceOf(bunny) == waifu
