import ape

def test_buyback_with_dai(buyer, yfi, dai, bunny, rune, brk_a, waifu):
    dai.transfer(buyer, brk_a, sender=rune)
    yfi.approve(buyer, waifu, sender=bunny)
    receipt = buyer.sell_yfi_for_dai(waifu, sender=bunny)
    log = next(buyer.Buyback.from_receipt(receipt))
    print(log.event_arguments)
    
    assert log.yfi_amount == waifu
    assert yfi.balanceOf(buyer) == waifu
    assert dai.balanceOf(bunny) == log.dai_amount


def test_buyback_stale_oracle(buyer, yfi, dai, bunny, rune, brk_a, waifu, chain):
    dai.transfer(buyer, brk_a, sender=rune)
    yfi.approve(buyer, waifu, sender=bunny)
    
    chain.mine(deltatime=86400)
    
    with ape.reverts():
        receipt = buyer.sell_yfi_for_dai(waifu, sender=bunny, gas_limit=1000000)
