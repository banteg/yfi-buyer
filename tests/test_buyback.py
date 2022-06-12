import ape
from eth_utils import from_wei


def test_buyback_with_dai(buyer, yfi, dai, bunny, milky, treasury, rune, brk_a, waifu):
    buyer.set_treasury(treasury, sender=milky)
    dai.transfer(buyer, brk_a, sender=rune)
    print("max_amount", from_wei(buyer.max_amount(), "ether"))
    yfi.approve(buyer, waifu, sender=bunny)
    receipt = buyer.buy_dai(waifu, sender=bunny)
    log = next(buyer.Buyback.from_receipt(receipt))
    print(log.event_arguments)
    print(log.dai / log.yfi, "YFI/DAI")

    assert log.buyer == bunny
    assert log.yfi == waifu
    assert yfi.balanceOf(treasury) == waifu
    assert dai.balanceOf(bunny) == log.dai


def test_buyback_stale_oracle(buyer, yfi, dai, bunny, rune, brk_a, waifu, chain):
    dai.transfer(buyer, brk_a, sender=rune)
    yfi.approve(buyer, waifu, sender=bunny)

    chain.provider.set_timestamp(chain.pending_timestamp + 86400)

    with ape.reverts():
        buyer.buy_dai(waifu, sender=bunny)

    assert yfi.balanceOf(bunny) == waifu


def test_price(buyer):
    price = buyer.price()
    print(from_wei(price, "ether"))
    assert 1000e18 < price < 465_000e18


def test_set_admin(buyer, milky, bunny, rune):
    assert buyer.admin() == milky

    with ape.reverts():
        buyer.set_admin(bunny, sender=bunny)

    buyer.set_admin(bunny, sender=milky)
    assert buyer.admin() == bunny


def test_sweep(buyer, yfi, dai, bunny, rune, milky):
    yfi.transfer(buyer, 100, sender=bunny)
    dai.transfer(buyer, 100, sender=rune)

    buyer.sweep(yfi, sender=milky)
    assert yfi.balanceOf(milky) == 100

    buyer.sweep(dai, 50, sender=milky)
    assert dai.balanceOf(milky) == 50


def test_set_treasury(buyer, bunny, milky, treasury):
    with ape.reverts():
        buyer.set_treasury(bunny, sender=bunny)

    buyer.set_treasury(treasury, sender=milky)
    assert buyer.treasury() == treasury
